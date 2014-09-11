#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, make_response, abort
from flask.ext.mongoengine import MongoEngine
from flask.ext.httpauth import HTTPBasicAuth
from mongoengine import *
import pymongo, os, json, uuid, hashlib

app = Flask(__name__)
auth = HTTPBasicAuth()


# Nos conectamos a la base de datos y 
# creamos los documentos que utilizaremos 

connect('imageApp')

class User(Document):
    # id = IntegerField(required = True, unique = True)   # Solo por ahora
    name = StringField(required = True)
    password = StringField(required = True)             # Averiguar tipo de dato password
    email = StringField(required = True, unique=True)                # Averiguar tipo de dato email
    registry_date = StringField(required = True)        # Averiguar tipo de dato fecha
    active = BooleanField(default = False)


# encriptamos la contraseña que está ingresando, para compararla con la del usuario
@auth.verify_password
def verify_password(username, password):
    try:
        user = User.objects.get(name = username)

        resp = check_password(user.password, password)

    except Exception, e:
        return False

    return resp



# Recordar cambiar el código de error de 403 a 401 (cuando el servicio sea consumido por apps)
@auth.error_handler
def unauthorized():
    return make_response(jsonify({ 'error': 'Unauthorized access' } ), 403) 



@app.route('/api/v1/users', methods = ['GET'])
# @auth.login_required
def get_users():
    resp = []
    users = User.objects
    for u in users:
        item = {
            # "id" : u.id,
            "name" : u.name,
            "email" : u.email,
            "active" : u.active,
            "registry_date" : u.registry_date,
            "password" : u.password
        }
        resp.append(item)

    return jsonify({'users': resp })



@app.route('/api/v1/users', methods = ['POST'])
def create_user():
    print request.json
    if not request.json or not 'name' in request.json:
        abort(400)

    new_user = User()
    new_user.name = request.json['name']
    new_user.email = request.json['email']
    new_user.active = request.json['active']
    new_user.password = hash_password(request.json['password'])

    # Acá sacar la fecha y hora actual.
    new_user.registry_date = request.json.get('registry_date', "")
    
    # Controlamos error en caso de que se inserte un usuario que ya existe
    try:
        new_user.save()
    except Exception, e:
        print e
        abort(400)

    return jsonify({'resp': 'Done' }), 201



@app.route('/api/v1/users/<int:user_id>', methods = ['PUT'])
def update_user(user_id):
    print request.json
    
    try:
        to_update = user.objects.get(_id = user_id)
        print to_update.name
    except Exception, e:
        print e
        


    return jsonify({'resp': False })



####### Funciones para manipulas contraseñas #############

def hash_password(password, new_salt = False):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    if new_salt:
        salt = new_salt

    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
 

if __name__ == '__main__':
    app.run(debug = True)
