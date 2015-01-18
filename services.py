#!flask/bin/python
# -*- coding: utf-8 -*-

##  To do:
#   - Delete
#   - Get por ID.

from flask import Flask, jsonify, request, make_response, abort
from flask.ext.mongoengine import MongoEngine
from flask.ext.httpauth import HTTPBasicAuth
from mongoengine import *
import pymongo, os, json, uuid, hashlib, datetime
from models.user import User
from models.patient import Patient
from models.image import Image

app = Flask(__name__)
auth = HTTPBasicAuth()

# Nos conectamos a la base de datos y 
connect('imageApp')

##### ==== USERS ==== ######

# encriptamos la contraseña que está ingresando, para compararla con la del usuario
@auth.verify_password
def verify_password(username, password):
    try:
        user = User.objects.get(email = username)
        resp = user.check_password(password)

    except Exception, e:
        return False

    return resp


# Recordar cambiar el código de error de 403 a 401 (cuando el servicio sea consumido por apps)
@auth.error_handler
def unauthorized():
    return make_response(jsonify({ 'error': 'Unauthorized access' } ), 403) 


@app.route('/api/v1/login', methods = ['POST'])
def login():
    if not request.json or not 'email' in request.json:
        abort(400)
        
    login_user_email = request.json['email']
    login_user_password = request.json['password']
    
    try:
        user = User.objects.get(email=login_user_email)
        resp = user.check_password(login_user_password)
        if resp:
            item = {
                "id"            : user.toString(),
                "name"          : user.name,
                "email"         : user.email,
                "active"        : user.active,
                "registry_date" : user.registry_date
            }
            return jsonify({'resp': True, 'error': 0, 'user': item })

        else:
            return jsonify({'resp': False, 'error': 'Invalid Password' })
    
    except Exception, e:
        return jsonify({'resp': False, 'error': 'Invalid Username' })


@app.route('/api/v1/users', methods = ['GET'])
@auth.login_required
def get_users():
    resp = []
    users = User.objects
    for u in users:
        item = {
            "id"            : u.toString(),
            "name"          : u.name,
            "email"         : u.email,
            "active"        : u.active,
            "registry_date" : u.registry_date,
            "password"      : u.password
        }
        resp.append(item)

    return jsonify({'users': resp, 'resp': True, 'error' : 0 })


@app.route('/api/v1/users/<user_id>', methods = ['GET'])
@auth.login_required
def get_one_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except Exception, e:
        return jsonify({'resp': False, 'error' : 'Invalid User id'})

    item = {
        "id"            : user.toString(),
        "name"          : user.name,
        "email"         : user.email,
        "active"        : user.active,
        "registry_date" : user.registry_date,
        "password"      : user.password
    }

    return jsonify({'users': item, 'resp': True, 'error' : 0})


@app.route('/api/v1/users', methods = ['POST'])
def create_user():
    # print request.json
    if not request.json or not 'email' in request.json:
        abort(400)

    new_user = User()
    new_user.name = request.json['name']
    new_user.email = request.json['email']
    new_user.active = request.json['active']
    new_user.password = request.json['password']
    new_user.hash_password()

    # Acá sacar la fecha y hora actual.
    current_time = datetime.datetime.now()
    new_user.registry_date = request.json.get('registry_date', current_time)
    
    # Controlamos error en caso de que se inserte un usuario que ya existe
    try:
        new_user.save()
    except Exception, e:
        print e
        abort(400)

    return jsonify({'resp': True, 'error' : 0 }), 201


@app.route('/api/v1/users/<user_id>', methods = ['PUT'])
@auth.login_required
def update_user(user_id):
    data = request.json
    
    try:
        to_update = User.objects.get(id = user_id)
        
        if 'name' in data:
            to_update['name'] = data['name']

        if 'email' in data:
            to_update['email'] = data['email']

        if 'password' in data:
            to_update['password'] = data['password']
            to_update.hash_password()
        
        # ** NO EDITABLE **
        # if 'active' in data:
        #     to_update['active'] = data['active']

        # ** NO EDITABLE **
        # if 'registry_date' in data:
        #     to_update['registry_date'] = data['registry_date']

        # En vez de recibir cambio de fecha de registro, es mejor actualizar la fecha, como la fecha en que fue editado el usuario.
        current_time = datetime.datetime.now()
        to_update['registry_date'] = current_time

        # Salvamos usuario
        to_update.save()

    except Exception, e:
        print e
        return jsonify({'resp': False })

    return jsonify({'resp': True })


##### ==== PATIENT ==== ######

@app.route('/api/v1/patients', methods=['GET'])
@auth.login_required
def get_patients():
    user_name = auth.username()
    _user = User.objects.get(email = user_name)

    resp = []
    patients = Patient.objects.filter(user = _user)

    for p in patients:
        item = {
            "id"            : str(p.id),
            "name"          : p.name,
            "phone"         : p.phone,
            "email"         : p.email,
            "description"   : p.description, 
            "groups"        : p.groups,
            "prevision"     : p.prevision, 
            "registry_date" : p.registry_date,
            "active"        : p.active,
            "user"          : p.user.toString()
        }
        resp.append(item)

    return jsonify({'patients': resp })

    
@app.route('/api/v1/patients', methods = ['POST'])
def create_patient():
    # print request.json
    if not request.json or not 'name' in request.json:
        abort(400)

    user_name = auth.username()
    _user = User.objects.get(email = user_name)


    new_patient             = Patient()
    new_patient.name        = request.json['name']
    new_patient.phone       = request.json['phone']
    new_patient.email       = request.json['email']
    new_patient.description = request.json['description']
    new_patient.groups      = request.json['groups']
    new_patient.prevision   = request.json['prevision']
    new_patient.active      = request.json['active']
    new_patient.user        = _user

    # Acá sacar la fecha y hora actual.
    new_patient.registry_date = request.json.get('registry_date', "")
    
    # Controlamos error en caso de que se inserte un usuario que ya existe
    try:
        new_patient.save()
    except Exception, e:
        print e
        abort(400)

    return jsonify({'resp': 'Done' }), 201       


@app.route('/api/v1/patients/<patient_id>', methods = ['PUT'])
def update_patient(patient_id):
    data = request.json
    
    try:
        to_update = Patient.objects.get(id = patient_id)
        
        if 'name' in data:
            to_update['name'] = data['name']

        if 'phone' in data:
            to_update['phone'] = data['phone']
        
        if 'email' in data:
            to_update['email'] = data['email']

        if 'description' in data:
            to_update['description'] = data['description']

        if 'groups' in data:
            to_update['groups'] = data['groups']

        if 'prevision' in data:
            to_update['prevision'] = data['prevision']

        # En vez de recibir cambio de fecha de registro, es mejor actualizar la fecha, como la fecha en que fue editado el usuario.

        to_update.save()

    except Exception, e:
        print e
        return jsonify({'resp': False })

    return jsonify({'resp': True })


if __name__ == '__main__':
    # app.run(debug = True)
    # app.run(debug = True, port=50100)
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080))) # Configuracion para que c9 pueda levantar servicios
