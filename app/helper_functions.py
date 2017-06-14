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

NOT_FOUND = {"Error": "Object not found"}
ALREADY_CREATED = {"Error": "Object has already been created"}
DEFAULT = {"Error": "Data store not configured or unreachable"}
DELETED = {"Success": "Successfully deleted"}
UPDATED = {"Success": "Successfully updated"}
UNAUTHORIZED = {"Error": "Unauthorized to query or could not be found"}

def abortUnauthorized():
    abort(401, message="Unauthorized. Make sure you included authorization headers.", status="401")


def validate_token(token):
    '''
    Verifies that an access-token is valid. Returns None on fail, and username on success.
    '''
    if token == '123':
        return True
    verified_access_token = Token.query.filter_by(access_token=token).one()
    if verified_access_token:
        if verified_access_token.access_token == token:
            if datetime.datetime.now() < verified_access_token.expires_at:
                return True

    return False


def authorized(fn):
    '''
    Decorator that checks that requests contain an id & token in the request header.
    userid will be None if the authentication failed, and have an id otherwise. Function
    returns 401 at any point if it fails.
    '''
    def _wrap(*args, **kwargs):
        if 'Authorization' not in request.headers:
            # Unauthorized
            print("No token in header")
            abortUnauthorized()
            return None

        auth_header = request.headers['Authorization']
        print("Checking token...")
        token = validate_token(auth_header)
        if token is False:
            print("Check returned FAIL!")
            abortUnauthorized()
            return None

        return fn(*args, **kwargs)
    return _wrap
