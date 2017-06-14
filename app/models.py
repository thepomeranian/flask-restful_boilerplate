from app import db
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import random
import hashlib
import base64


class Users(db.Model):
    '''
    This is the User model.
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    _password = db.Column('password', db.String(120), nullable=False)
    created_on = db.Column(db.DateTime)
    last_logged_in = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    email = db.Column(db.String(150))
    display_name = db.Column(db.String(120))
    admin = db.Column(db.Boolean, default=False)
    local = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(120))

    token = db.relationship('Token', back_populates='users')

    def __repr__(self):
        return '<User %r>' % (self.username)

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    def _get_password(self):
        return self._password

    password = db.synonym('_password', descriptor=property(
        _get_password, _set_password))

    def valid_password(self, password):
        return check_password_hash(self._password, password)

    def is_authenticated(self):
        return True

    def user_status(self):
        return "Active" if self.active else "Deactivated"

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def is_administrator(self):
        return True if self.role == 2 else False

class Token(db.Model):
    '''
    This is the Token model.
    '''
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    expires_at = db.Column(db.DateTime)
    disabled = db.Column(db.Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    users = db.relationship('Users', back_populates='token')

    def create_token(self):
        token = base64.b64encode(hashlib.sha256(str(random.getrandbits(256))).digest(
        ), random.choice(['rA', 'aZ', 'gQ', 'hH', 'hG', 'aR', 'DD'])).rstrip('==')
        return token

    def disable(self):
        self.disabled = True
        return self
