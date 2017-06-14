import os
from flask import Flask
from flask_restful import fields, marshal_with, reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager
from config import _basedir

# App
app = Flask(__name__, static_folder='static/swagger', static_url_path='')
app.config.from_object('app.config')
# app.config['SQLALCHEMY_ECHO'] = True
api = Api(app)

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

from app import models, views

