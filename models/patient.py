#!flask/bin/python
# -*- coding: utf-8 -*-

from flask.ext.mongoengine import MongoEngine
from mongoengine import *
import user
import pymongo, os, json, uuid, hashlib

class Patient(Document):
    name            = StringField(required = True) 
    phone           = StringField(required = True)
    email           = StringField(required = True, unique = True)
    description     = StringField(required = True)
    groups          = StringField(required = True)
    prevision       = StringField(required = True)
    registry_date   = StringField(required = True)
    active          = BooleanField(default = True)
    # user            = ReferenceField(User)
