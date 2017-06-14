import os
DEBUG =  True
_basedir = os.path.abspath(os.path.dirname(__file__))

# Forms and cookies
# CSRF_ENABLED = True
# CSRF_SESSION_KEY = "somethingimpossibletoguess" #needs new value
SECRET_KEY = 'values' #needs new value

# Database
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# MySQL
# SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", 'mysql://root@localhost:3306/flask-restful-swagger')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')

# Postgres
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", 'postgresql://localhost:5432/flask-restful-swagger')
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')