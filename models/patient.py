#!flask/bin/python
# -*- coding: utf-8 -*-

from flask.ext.mongoengine import MongoEngine
from mongoengine import *
from user import User
import pymongo, os, json, uuid, hashlib

class Patient(Document):
    name            = StringField(required = True) 
    phone           = StringField(required = True)
    email           = StringField(required = True, unique = True)
    description     = StringField(required = True)
    groups          = ListField(required = True)
    prevision       = StringField(required = True)
    registry_date   = StringField(required = True)
    active          = BooleanField(default = True)
    user            = ReferenceField(User, dbref = False)

Patient.register_delete_rule(User, 'patient', CASCADE)