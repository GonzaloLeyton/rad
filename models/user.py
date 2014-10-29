#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, make_response, abort
from flask.ext.mongoengine import MongoEngine
from mongoengine import *
import pymongo, os, json, uuid, hashlib

class User(Document):
    name            = StringField(required = True)                  # Editable
    password        = StringField(required = True)                  # Editable
    email           = EmailField(required = True, unique = True)    # Editable
    registry_date   = StringField(required = True)                  # Averiguar tipo de dato fecha
    active          = BooleanField(default = True)

    def toString(self):
        return str(self.id)

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