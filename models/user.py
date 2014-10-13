#!flask/bin/python
# -*- coding: utf-8 -*-

from flask.ext.mongoengine import MongoEngine
from mongoengine import *
import pymongo, os, json, uuid, hashlib

class User(Document):
    # id = IntegerField(required = True, unique = True)   # Solo por ahora
    name            = StringField(required = True)
    password        = StringField(required = True)             # Averiguar tipo de dato password
    email           = StringField(required = True, unique = True)                # Averiguar tipo de dato email
    registry_date   = StringField(required = True)        # Averiguar tipo de dato fecha
    active          = BooleanField(default = True)

# TO DO:
# - User: Funciones para validar contraseña. Deberían ser parte de la clase usuario, y no del main