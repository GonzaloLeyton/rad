#!flask/bin/python
# -*- coding: utf-8 -*-

##  To do:
#   - Delete
#   - Get por ID.

from flask import Flask, jsonify, request, make_response, abort
from flask.ext.mongoengine import MongoEngine
from flask.ext.httpauth import HTTPBasicAuth
from mongoengine import *
import pymongo, os, json, uuid, hashlib
from models.user import *
from models.patient import *
from models.image import *

app = Flask(__name__)
auth = HTTPBasicAuth()

# Nos conectamos a la base de datos y 
connect('imageApp')


##### ==== USERS ==== ######

# encriptamos la contraseña que está ingresando, para compararla con la del usuario
@auth.verify_password
def verify_password(username, password):
    try:
        user = User.objects.get(name = username)

        resp = user.check_password(password)

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
            "id" : str(u.id),
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
    # print request.json
    if not request.json or not 'name' in request.json:
        abort(400)

    new_user = User()
    new_user.name = request.json['name']
    new_user.email = request.json['email']
    new_user.active = request.json['active']
    new_user.password = request.json['password']
    new_user.hash_password()

    # Acá sacar la fecha y hora actual.
    new_user.registry_date = request.json.get('registry_date', "")
    
    # Controlamos error en caso de que se inserte un usuario que ya existe
    try:
        new_user.save()
    except Exception, e:
        print e
        abort(400)

    return jsonify({'resp': 'Done' }), 201



@app.route('/api/v1/users/<user_id>', methods = ['PUT'])
def update_user(user_id):
    data = request.json
    
    try:
        to_update = User.objects.get(id = user_id)
        
        if 'name' in data:
            to_update['name'] = data['name']

        if 'email' in data:
            to_update['email'] = data['email']

        if 'active' in data:
            to_update['active'] = data['active']

        if 'password' in data:
            to_update['password'] = data['password']
            to_update.hash_password()

        if 'registry_date' in data:
            to_update['registry_date'] = data['registry_date']


        to_update.save()

    except Exception, e:
        print e
        return jsonify({'resp': False })

    return jsonify({'resp': True })




##### ==== PATIENT ==== ######







    


if __name__ == '__main__':
    app.run(debug = True)
    # app.run(debug = True, port=50100)
