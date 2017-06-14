from app import app, api, db
from flask import Flask, request, jsonify
from flask_restful import fields, marshal_with, reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from models import *
import os
import random
import hashlib
import base64
import json
from helper_functions import *
from tokens import *
from users import *

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Username')

api.add_resource(Tokens, '/v1/tokens')
api.add_resource(User, '/v1/users')
api.add_resource(User_method, '/v1/users/<username>')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,PATCH')
    return response


@app.route('/')
def index():
    """Returns the Swagger UI"""
    return app.send_static_file('index.html')
    
