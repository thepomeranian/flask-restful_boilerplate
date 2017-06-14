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


class User(Resource):
    '''
    This is the User Resource. 

    Methods:
        GET - queries for a single user or returns all users
        POST - creates a new user
    '''
    method_decorators = [authorized]

    def get(self):
        '''User's GET method

        Queries for a single user or returns all users

        Parameters:
            username (optional)
            q (optional)
        Returns:
            404 -- Object not found
            200 -- User(s) successfully queried
        '''
        output = {}
        username = request.args.get('username')
        q = request.args.get('q')

        if q is not None:
            fuzzy_search = Users.query.filter(
                Users.username.like('%' + q + '%')).all()
            print fuzzy_search
            if not fuzzy_search:
                return NOT_FOUND, 404
            user_lst = []
            for user in fuzzy_search:
                user_lst.append({'admin': user.admin,
                                 'display-name': user.display_name,
                                 'email': user.email,
                                 'local': user.local,
                                 'password': user.password,
                                 'username': user.username
                                 })
            output = user_lst

        if username is not None:
            user = Users.query.filter_by(username=username).first()
            if user is None:
                return NOT_FOUND, 404
            else:
                output = {'admin': user.admin,
                          'display-name': user.display_name,
                          'email': user.email,
                          'local': user.local,
                          'password': user.password,
                          'username': user.username
                          }

        if q is None and username is None:
            users = Users.query.all()
            user_lst = []
            for user in users:
                user_lst.append({'admin': user.admin,
                                 'display-name': user.display_name,
                                 'email': user.email,
                                 'local': user.local,
                                 'password': user.password,
                                 'username': user.username
                                 })
            output = user_lst

        return output, 200

    def post(self):
        '''User's POST method

        Creates a single User Model from a JSON.

        Returns:
            201 -- JSON object of User
            200 -- User already created
            500 -- Error
        '''
        json_data = request.get_json(force=True)

        admin = json_data['admin']
        display_name = json_data['display-name']
        email = json_data['email']
        local = json_data['local']
        password = json_data['password']
        username = json_data['username']

        exist = self.exists(username)

        if exist:
            return ALREADY_CREATED, 500
        else:
            self.create_user(admin, display_name, email,
                             local, password, username)

            user = Users.query.filter_by(username=username).first()

            output = {'admin': admin,
                      'display-name': display_name,
                      'email': email,
                      'local': local,
                      'password': password,
                      'username': username
                      }

            return output, 201

        return DEFAULT, 500

    def exists(self, username):
        user = Users.query.filter_by(username=username).first()
        if user:
            return True
        return False

    def create_user(self, admin, display_name, email, local, password, username):
        user = Users()
        user.created_on = datetime.datetime.now()
        user.updated_on = datetime.datetime.now()
        user.admin = admin
        user.display_name = display_name
        user.email = email
        user.local = local
        user.password = password
        user.username = username
        db.session.add(user)
        db.session.commit()


class User_method(Resource):
    '''
    This is the User_method Resource. 

    Methods:
        GET - queries for a single user
        PATCH - updates a single user
        DELETE - deletes a single user
    '''
    method_decorators = [authorized]

    def get(self, username):
        '''User_method's GET method

        Queries for a single user

        Returns:
            404 -- Object not found
            200 -- User(s) successfully queried
        '''
        if username is not None:
            user = Users.query.filter_by(username=username).first()
            print user
            if user is None:
                return NOT_FOUND, 404
            else:
                output = {"admin": user.admin,
                          "display-name": user.display_name,
                          "email": user.email,
                          "local": user.local,
                          "password": user.password,
                          "username": user.username
                          }

            return output, 200
        return DEFAULT, 500

    def delete(self, username):
        '''User_method's DELETE method

        Deletes a single user

        Returns:
            204 -- Deletes user
            404 -- Object not found
            500 -- Error
        '''
        if username:
            user = Users.query.filter_by(username=username).first()

            if user:
                db.session.delete(user)
                db.session.commit()
                return DELETED, 204

            if user is None:
                return NOT_FOUND, 404
        return DEFAULT, 500

    def patch(self, username):
        '''User_method's PATCH method

        Updates a single user

        Returns:
            200 -- User updated
            404 -- Query not successful
            500 -- Error
        '''
        json_data = request.get_json(force=True)
        if json_data:
            username_given = username

            admin = json_data['admin']
            display_name = json_data['display-name']
            email = json_data['email']
            local = json_data['local']
            password = json_data['password']
            username_json = json_data['username']

            if username_given == username_json:
                username = username_given
                user = Users.query.filter_by(username=username).first()
                if user:
                    user.updated_on = datetime.datetime.now()
                    user.admin = admin
                    user.display_name = display_name
                    user.email = email
                    user.local = local
                    user.password = password

                    db.session.add(user)
                    db.session.commit()

                    return UPDATED, 200
                else:
                    return NOT_FOUND, 404
            else:
                return NOT_FOUND, 404
        return DEFAULT, 500
