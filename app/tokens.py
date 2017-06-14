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


class Tokens(Resource):
  '''
    This is the Tokens Resource. 

    Methods:
        POST - creates access and/or refresh tokens for a user
  '''
  # TODO implement JWT/ itsdangerous
  # https://pythonhosted.org/itsdangerous/#itsdangerous.TimedSerializer
  
  def post(self):
    '''Token's POST method

    Creates access and refresh tokens for a user

    Returns:
    200 -- Successful token generation
    401 -- Unauthorized
    500 -- ERROR
    '''
    output = []
    json_data = request.get_json(force=True)
    password = json_data['password']
    username = json_data['username']
    grant_type = ''
    user = Users.query.filter_by(username=username).first()

    if user:
        if user.valid_password(password):
            token = Token.query.filter_by(user_id=user.id).first()
            if token is None:
                token = Token()
                token.user_id = user.id

            if 'grant-type' in json_data:
                grant_type = json_data['grant-type']

                if grant_type == 'access_token':
                    refresh_token = json_data['refresh-token']
                    if token.refresh_token == refresh_token:
                        token.access_token = token.create_token()
                        token.expires_at = datetime.datetime.now() + datetime.timedelta(days=7)
                    else:
                        return UNAUTHORIZED, 401

                if grant_type == 'refresh_token':
                    refresh_token = json_data['refresh-token']
                    if token.refresh_token == refresh_token:
                        token.refresh_token = token.create_token()
                        token.access_token = token.create_token()
                        token.expires_at = datetime.datetime.now() + datetime.timedelta(days=7)
                    else:
                        return UNAUTHORIZED, 401

            else:
                token.access_token = token.create_token()
                token.refresh_token = token.create_token()
                token.expires_at = datetime.datetime.now() + datetime.timedelta(days=7)

            db.session.add(token)
            db.session.commit()

            output = {"access-token": token.access_token,
                      "admin": user.admin,
                      "display-name": user.display_name,
                      "email": user.email,
                      "expires-at": str(token.expires_at),
                      "expires-in": 0,
                      "groups": [group.group_name for group in user.groups],
                      "local": user.local,
                      "password": user.password,
                      "refresh-token": token.refresh_token,
                      "token-in": "string",
                      "token-type": grant_type,
                      "username": user.username
                      }

            return output, 200
        else:
            return UNAUTHORIZED, 401

    return DEFAULT, 500
