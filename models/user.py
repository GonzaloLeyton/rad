#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, make_response, abort
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


    def hash_password(self, new_salt = False):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        if new_salt:
            salt = new_salt

        passwd = self.password
        self.password = hashlib.sha256(salt.encode() + passwd.encode()).hexdigest() + ':' + salt
        # return hashlib.sha256(salt.encode() + passwd.encode()).hexdigest() + ':' + salt


    def check_password(self, user_password):
        passd, salt = self.password.split(':')
        return passd == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
     
# TO DO:
# - User: Funciones para validar contraseña. Deberían ser parte de la clase usuario, y no del main