# Flask-restful-swagger

**Overview**

RESTful API stands for _**Representational State Transfer** Application Programming Interface_

**Tech Stack**

* [flask](http://flask.pocoo.org/)
* [flask-restful](https://flask-restful.readthedocs.io/en/0.3.5/index.html)
* [flask-sqlalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
* [PostgreSQL](https://www.postgresql.org/)
* [swagger UI](http://swagger.io/swagger-ui/)

## Setup

#### Requirements

- Python 2.7.x (with pip)
- virtualenv (`sudo easy_install virtualenv`)
- Postgres

#### First-time setup

Clone the project, and `cd` to the folder `cd flask-restful-swagger`:

```shell
git clone <todo: add .git>
```

1. Create a virtual env for Python 

    ```Shell
    virtualenv venv
    ```

2. Activate the virtual env

    ```Shell
    source venv/bin/activate
    ```

3. Install dependencies

    ```Shell
    pip install –r requirements.txt
    ```

4. After Postgres is set up, initialize db migrations for schema management, and make a migration

    ```shell
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```

5. To start the app

    ```Shell
    python run.py
    ```


## Development

After setup, the main command line development workflow consists of:

- Activating the virtualenv
- Running the application
- Making any database migrations when there are changes in the models

**Activate virtualenv**

```Shell
source venv/bin/activate
```

**Deactivate virtualenv**

```Shell
deactivate
```

**Run the app**

```Shell
python run.py
```

**Migrate the database (do both)**

```Shell
python manage.py db migrate
```

```Shell
python manage.py db upgrade
```

**Swagger UI URL**

```http
http://localhost:5000/index.html
```

## Optional

#### Tokens

Access Tokens currently set to expire in 7 days from generation time.

Refresh Tokens currently do not expire.

#### Deleting the database

When the database is deleted, the `migrations` folder needs to be deleted and then 

#### `__init__.py`

[What is the `__init__.py` file for?](https://stackoverflow.com/questions/448271/what-is-init-py-for)

#### `json.dumps` vs `flask.jsonify`

A comparison of json outputs on [stackoverflow](https://stackoverflow.com/questions/7907596/json-dumps-vs-flask-jsonify).

#### API endpoints

A REST API can have parameters in at least two ways:

1. **As part of the URL-path** (i.e. `/api/resource/parametervalue` )
2. **As a query argument** (i.e. `/api/resource?parameter=value` )

## Flask-Restful Tutorial

#### Types of classes

Two resource classes are needed per endpoint. One resource class will handle endpoints that do not have url path arguments, the other will. 

```python
api.add_resource(Pets, '/v1/pets')
api.add_resource(Pets_method, '/v1/pets/<pet_arg>')
```

`Pets` is a class found in `pets_resource.py`, `Pets_method` is a class also found in `pets_resource.py`, and `Pet` is a class found in `models.py` for the database model/table. *It is important to have unique class names.*

#### Creating a class

**Simple Class**

```Python
class SimpleClass(Resource):
    """This is the SimpleClass class"""
    def get(self):
        """GET method"""
        # Do something
        return 200

    def post(self):
        """POST method"""
        # Do something
        return 201
```

#### Creating a GET method

**GET (all) method**

* If a user needs a token to access this endpoint, add `method_decorators = [authorized]`. To read more about decorators, click [here for official python docs](https://wiki.python.org/moin/PythonDecorators#What_is_a_Decorator), [here for flask docs](http://flask.pocoo.org/docs/0.12/views/#decorating-views), [and here for flask-restful docs](https://flask-restful.readthedocs.io/en/0.3.5/extending.html).
* Create the GET method
* Query the database for `all()`
* To create nested JSON, write a for loop that loops through every key + value pair
* `output` automatically gets jsonified

```python
class Pets(Resource):
    method_decorators = [authorized]

    def get(self):
        """Pets' GET method

        Queries for all pets

        Returns:
            401 -- Object not found or Unauthorized
            200 -- pets successfully queried
        """
        pets = Pet.query.all()
        for pet in pets:
            output = {"name": pet.name,
                      "age": pet.age,
                      "sex": pet.sex,
                      "breed": pet.breed
                     }

            return output, 200
```

#### Creating a POST method

**POST method**

* If there are URL parameters as a query argument, get them with `request.args.get()`
* If there is a JSON object, use `request.get_json(force=True)`
* JSON object = python dictionary
* `pet = Pet()` creates an instance of Pet class. aka, creates a new row in the table `pets_owned`
* `db.session.add(pet)` adds the row into the database, however, `db.session.commit()` is what completes the database transaction.
* `user.add_pet(pet)` calls a User class method `add_pet()` and populates the association table between user and pet.

```python
class Pets(Resource):
    method_decorators = [authorized]

    def post(self):
        """Pets' POST method

        Adds a new Pet Model from JSON.

        Returns:
            200 -- JSON object of pet
            401 -- pet already exists
            500 -- Error
        """
        json_data = request.get_json(force=True)
        name = json_data['name']
        username = json_data['username']
        password = json_data['password']
        user = Users.query.filter_by(username=username).first()

        pet = Pet.query.filter_by(name=name).first()

        if pet is not None:
            return {"Error": "Unauthorized to query or could not be found"}, 401
        else:
            pet = Pet()
            pet.name = name
            pet.age = age
            pet.sex = sex
            pet.breed = breed
            db.session.add(pet)
            user.add_pet(pet)
            db.session.commit()

            output = {"name": pet.name,
                      "age": pet.age,
                      "sex": pet.sex,
                      "breed": pet.breed
                     }

            return output, 200

        return {"Error": "Data store not configured or unreachable"}, 500
```

#### Creating a GET method

* Get parameters as part of the URL path by accepting an argument in the method.

* In order the get a URL path, a parser is needed.

  ​ In `views.py` :

  ```python
  parser = reqparse.RequestParser()
  parser.add_argument('pet_arg', type=str, required=True, help='pet_argument')
  ```

**GET (one) method**

```python
class Pets_method(Resource):
    method_decorators = [authorized]

    def get(self, pet_arg):
        """Pets' GET method

        Queries for a single pet

        Parameters:
            pet_arg
        Returns:
            401 -- Unauthorized to query or could not be found
            404 -- Object not found
            500 -- Data store not configured or unreachable
        """
        if pet is not None:
            pet = Pet.query.filter_by(
                name=pet_arg).first_or_404()
            if pet is None:
                return {"Error": "Object not found"}, 404
            else:
              output = {"name": pet.name,
                      "age": pet.age,
                      "sex": pet.sex,
                      "breed": pet.breed
                     }

            return output, 200

        return {"Error": "Data store not configured or unreachable"}, 500
```

#### Creating a PATCH method

PATCH is similar to POST except you have to query it first. Using `first_or_404()` returns 404 if it can't find the parameter passed in the URL path or the first object.

**PATCH method**

```python
class Pets_method(Resource):
    method_decorators = [authorized]
    def patch(self, pet_arg):
            """Pets_method's PATCH method

            Updates a single pet

            Returns:
                401 -- Unauthorized to query or could not be found
                404 -- Object not found
                500 -- Data store not configured or unreachable
            """
            json_data = request.get_json(force=True)
            if json_data:
                json_data = request.get_json(force=True)
                name = json_data['name']
                username = json_data['username']
                password = json_data['password']
                user = Users.query.filter_by(username=username).first_or_404()

                pet = Pet.query.filter_by(name=name).first()

                pet.name = name
                pet.age = age
                pet.sex = sex
                pet.breed = breed

                db.session.add(pet)
                user.add_pet(pet)
                db.session.commit()

              output = {"name": pet.name,
                      "age": pet.age,
                      "sex": pet.sex,
                      "breed": pet.breed
                     }

                return output, 200

            return {"Error": "Data store not configured or unreachable"}, 500
```

#### Creating a DELETE method

DELETE is similar to GET (one) except you have to call `db.session.delete()` to delete an object and `db.session.commit()` to complete the transaction.

**DELETE method**

```python
class Pets_method(Resource):
    method_decorators = [authorized]

    def delete(self, pet_args):
        """Pets_method's DELETE method

        Deletes a single pet

        Returns:
            204 -- Deletes pet
            401 -- Unauthorized to query or could not be found
            404 -- Object not found
            500 -- Data store not configured or unreachable
        """
        if pet_args:
            pet = Pet.query.filter_by(
                name=pet_arg).first()

            if pet:
                db.session.delete(pet)
                db.session.commit()
                return {"Success": "Successfully removed pet"}, 204

            if pet is None:
                return {"Error": "Object not found"}, 404
        return {"Error": "Data store not configured or unreachable"}, 500
```

## Flask-SQLAlchemy Tutorial

#### What is SQLAlchemy?

SQLAlchemy is a powerful Python-based ORM. Flask-SQLAlchemy is a flask wrapper for it. 

SQLAlchemy cheat sheet from a codementor [here](https://www.codementor.io/sheena/understanding-sqlalchemy-cheat-sheet-du107lawl).

#### Creating db models

**Creating a table and db model**

*SQL:*

```SQL
CREATE TABLE tokens (
  token_id SERIAL PRIMARY KEY,
  grant_type VARCHAR(80),
  access_token VARCHAR(255),
  refresh_token VARCHAR(255),
  expires_at DATETIME,
  token_type VARCHAR(80)
)
```

*SQLAlchemy:*

```python
class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    grant_type = db.Column(db.String(80))
    access_token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    expires_at = db.Column(db.DateTime)
    token_type = db.Column(db.String(80))
```

Creating a class in SQLAlchemy= creating a table in SQL. SQLAlchemy allows relationship and foreign key declarations

#### Relationships between tables 

Official docs [here](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html), [simple explanation of relationship types here with graphics](https://support.airtable.com/hc/en-us/articles/218734758-A-beginner-s-guide-to-many-to-many-relationships)

Information about `backref` [here](http://docs.sqlalchemy.org/en/latest/orm/backref.html), and [here](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref)

Information about `back_populates` [here](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates)

**1:1** (using back_populates creates a bi-directional 1:1 relationship)

```python
class Users(db.Model):
  ...
  ...
  token = db.relationship('Token', back_populates='users')

class Token(db.Model):
  ...
  ...
  users = db.relationship('Users', back_populates='token')
```

**1:many** 

```python
class Users(db.Model):
  ...
  ...
  groups = db.relationship('Group', backref='group', lazy='dynamic')

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

**many:many**

```python
cat_toe_to_leg_association_table = db.Table('cat_toe_to_leg_association_table', db.Column('cat_toe_id', db.Integer, db.ForeignKey('cat_toe.id')),db.Column('cat_leg_id', db.Integer, db.ForeignKey('cat_leg.id')))

class CatToe(db.Model):
    __tablename__ = 'cat_toe'
    id = db.Column(db.Integer, primary_key=True)
    
class CatLeg(db.Model):
    __tablename__ = 'cat_leg'
    id = db.Column(db.Integer, primary_key=True)

    toes_to_legs = db.relationship(
        'CatToe', secondary=cat_toe_to_leg_association_table, backref="cat_leg", lazy='dynamic')
```

#### Association tables

Many to many relationships adds association tables to link the two together. It is possible to have bi-directional relationships and query into another table entirely using the defined many to many relationship. For example, you can query a single library book and be able to query all of the genres in one single statement because of the bi-directional relationship.

```python
group_association_table = db.Table('group_association_table',
                                   db.Column('group_id', db.Integer,
                                             db.ForeignKey('group.id')),
                                   db.Column('user_id', db.Integer,
                                             db.ForeignKey('users.id'))
                                   )
```

#### Foreign keys

Official docs [here](http://docs.sqlalchemy.org/en/latest/core/constraints.html)

#### Using db model

Create a new row in the db by calling the class name. Since everything in our `Token` table is optional we can skip several columns and leave it `null`. (_Example in shell_)

```shell
>>> token = Token(grant_type='admin', access_token='123', refresh_token='abc', token_type='string')
>>> token.access_token
123
>>> db.session.add(token)
>>> db.session.commit()
```

The the `db.session.add()` and `db.session.commit()` are required when making additions or changes to the database with POST and PATCH methods.

#### Querying

Official docs and all methods [here](http://docs.sqlalchemy.org/en/latest/orm/query.html)

**Query every single token by calling `all()`.**

*SQL:*

```sql
SELECT * FROM token
```

*SQLAlchemy:*

```python
Token.query.all()
```

**Filtering**

There are two ways to filter:  `filter` and `filter_by`. [`filter` vs `filter_by`](https://stackoverflow.com/questions/2128505/whats-the-difference-between-filter-and-filter-by-in-sqlalchemy)

*SQL:*

```SQL
SELECT * FROM token WHERE grant_type = "admin"
```

*SQLAlchemy with `filter_by`:*

```python
Token.query.filter_by(grant_type='admin').all()
```

*SQLAlchemy with `filter`:*

```python
Token.query.filter(Token.token_type == 'string').all()
```

*SQL:*

```sql
SELECT * FROM token WHERE token_type = "string" AND grant_type = "admin"
```

*SQLAlchemy:*

```python
Token.query.filter(Token.token_type == 'string', Token.grant_type == 'admin').all()
```

**Fetching Records** 

Official docs [here](http://flask-sqlalchemy.pocoo.org/2.1/queries/#querying-records)

`all()`

- Get all records

`first()`

* Get first record or _None_

`first_or_404()`

* Get first record or return 404

`one()`

- Get first record, error if 0 or if > 1

#### Querying multiple tables

Documentation for Join [here](http://docs.sqlalchemy.org/en/latest/orm/join_conditions.html)

### Development Tools:

**Endpoint testing**

[Paw](https://paw.cloud/) — paid, mac only

[Postman](https://www.getpostman.com/) — free, mac, windows, linux, chrome extension

**Prettify code**

[PEP 8 styling](https://www.python.org/dev/peps/pep-0008/) (extension available on [Atom](https://atom.io/packages/pep8) and [Sublime](https://packagecontrol.io/packages/Python%20PEP8%20Autoformat))

JSON: Sublime — [HTML, CSS, JS Prettify (JSON included)](https://packagecontrol.io/packages/HTML-CSS-JS%20Prettify) Atom — [Pretty JSON](https://atom.io/packages/pretty-json)

**Database**

[Postico](https://eggerapps.at/postico/) — free, mac only [Alternatives](https://alternativeto.net/software/postico/)

**What are the limitations of the free trial?**

* At most 5 connection favorites

- Only a single window per connection
- Table filters are disabled
- There is no time limit — use the trial as long as you want!)

## Testing an endpoint

**Method 1:** curl

**Method 2:** [requests](http://docs.python-requests.org/en/master/) Library

The requests library is capable of support GET, PUT, POST, and DELETE methods

1. Start up a venv

2. Install requests library `pip install requests`

   **Simple Example in Shell**

   ```shell
   >>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
   >>> r.status_code
   200
   >>> r.headers['content-type']
   'application/json; charset=utf8'
   >>> r.encoding
   'utf-8'
   >>> r.text
   u'{"type":"User"...'
   >>> r.json()
   {u'private_gists': 419, u'total_private_repos': 77, ...}
   ```

**Method 3:** Paw or Postman

## Virtual Environment

- [virtualenv](https://virtualenv.pypa.io/en/stable/#introduction)

  - A tool that allows the user to create multiple isolated Python environments on one machine. _(e.g. system uses v2.6, one app uses v3.5 and another v2.7.)_

  - Keeps different project environments isolated and contained

    - _Note: Make sure if you create a `.gitignore` file by using the command `touch .gitignore`, and adding **venv** and **secret** (for your secret key(s)) to avoid checking in your virtualenv and secret key(s) into the repo by adding these two lines to `.gitignore`._ 

      ```basic
      *venv*
      *secret*
      ```

  **For installation instructions and setting up virtualenv:** http://flask.pocoo.org/docs/0.12/installation/#installation 

1. Create a new virtual environment for your copy of the Highlands API. Most of the time, the python that comes with this is 2.7. You can designate what version of Python you want to develop in and more information about virtual environments using [this](http://docs.python-guide.org/en/latest/dev/virtualenvs/). 

2. Activate your virtual environment.

   ```basic
   source venv/bin/activate
   ```


3. Perform a git clone of the boilerplate/base here.

   ```basic
   git clone <todo: insert .git here>
   ```

4. `cd` into the directory and find `requirements.txt` and install the requirements for this project into your virtual environment using the line below. For a guide on installing `pip`, click [here](https://pip.pypa.io/en/stable/installing/).

   ```basic
   pip install -r requirements.txt
   ```

5. Make sure that the current working directory is on your `PYTHONPATH`

   ```basic
   export PYTHONPATH=.:$PYTHONPATH
   ```

6. Start the app

   ```basic
   python run.py
   ```


## PostgreSQL

Cheatsheet [here](https://gist.github.com/apolloclark/ea5466d5929e63043dcf)

## Testing

#### _Testing Libraries and Examples:_

[Flask-Testing](https://pythonhosted.org/Flask-Testing/): unit testing utilities for Flask

[unittest](https://docs.python.org/2/library/unittest.html): unit testing framework

[unittest2](https://pypi.python.org/pypi/unittest2): unit testing framework

[nose](https://nose.readthedocs.io/en/latest/): extends unittest

[doctest](https://docs.python.org/2/library/doctest.html): writes tests in docstrings of a function

[Example of TDD of a flask API with nose, flask-restful, flask-sqlalchemy](http://mkelsey.com/2013/05/15/test-driven-development-of-a-flask-api/)

[test client](http://werkzeug.pocoo.org/docs/0.10/test/): pass a WSGI application (and response wrapper) to app for testing

[Selenium](http://www.seleniumhq.org/): browser automation, "end to end" testing _[Alternatives to Selenium](https://alternativeto.net/software/selenium/)_

[Flask's own documentation on testing](http://flask.pocoo.org/docs/0.12/testing/)

[coverage](https://coverage.readthedocs.io/en/coverage-4.3.4/): measure code coverage

## Extra Reading 

[Types of Software Testing](http://www.buzzle.com/articles/types-of-software-testing.html) _Credit Buzzle_

[HTTP Protocol Definitions](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html) _Credit w3_