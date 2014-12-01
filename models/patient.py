#!flask/bin/python
# -*- coding: utf-8 -*-

from flask.ext.mongoengine import MongoEngine
from mongoengine import *
from user import User
import pymongo, os, json, uuid, hashlib

class Patient(Document):
    name            = StringField(required = True) 					# Editable
    phone           = StringField(required = True)					# Editable
    email           = EmailField(required = True, unique = True)	# Editable
    description     = StringField(required = True)					# Editable
    groups          = ListField(required = True)					# Editable
    prevision       = StringField(required = True)					# Editable
    registry_date   = DateTimeField(required = True)					
    active          = BooleanField(default = True)
    user            = ReferenceField(User, dbref = False)

    def toString(self):
        return str(self.id)

Patient.register_delete_rule(User, 'patient', CASCADE)