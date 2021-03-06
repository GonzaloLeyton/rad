#!flask/bin/python
# -*- coding: utf-8 -*-

from flask.ext.mongoengine import MongoEngine
from mongoengine import *
from patient import Patient
import pymongo, os, json, uuid, hashlib

class Image(Document):
    image       = StringField(required = True)
    title       = StringField(required = True)
    description = StringField(required = True)
    tags        = StringField(required = True)
    diagnosis   = StringField(required = True)
    create_date = DateTimeField(required = True)
    groups      = StringField(required = True)
    patient     = ReferenceField(Patient)