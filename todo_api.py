from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

"""
This file contains the code to run the todo app's API and database. The API is made using flask_restful and database is made
using flask_sqlalchemy.
"""

# Creates the Flask app aobject and the API and Database wrappers.
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app)

# This variable is used as a parameter for the @marshall_with decorator used later.
resource_fields = {'id': fields.Integer,
                   'todo': fields.String,
                  }

# This class is lays out the strucutre of a SQL database table. The is named after the class (in snake casing) and each
# object within the class represends a collumn in the databse.
class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), nullable=False)

# **IMPORTANT** 
# The db.create_all() method creates the database and must be run the first time the API is activated. On all subsequent 
# activations this should be either deleted or commented out, otherwise it will overwrite your previous database
# with a new blank database.
# db.create_all()

# This class is used to parse through the packages received via HTTP and structures them in JSON format
# for easy reading later.
class ArgumentParser():

    def __init__(self):
        self.request_args = reqparse.RequestParser()
        self.request_args.add_argument('id', type=int, help='id not found', required=True)
        self.request_args.add_argument('todo', type=str, help='todo not found', required=True)

        self.update_args = reqparse.RequestParser()
        self.update_args.add_argument('id', type=int, help='id not found')
        self.update_args.add_argument('todo', type=str, help='name not found')


# This is a Resource subclass, which determines how the API will respond to different HTTP methods that are sent to
# the appropriate URI endpoint.
class TodoResource(Resource):
    
    # Responds to get requests by sending back the entire stored database in JSON format. If the database is empty,
    # A blank JSON file will be returned
    @marshal_with(resource_fields)
    def get(self):
        result = ToDoModel.query.all()
        return result, 200

    # Reponds to put requests. Data recieved with the request is added to the database. Will return a
    # 404 code if the provided ID number already exists in the database.
    @marshal_with(resource_fields)
    def put(self):
        parser = ArgumentParser()
        args = parser.request_args.parse_args()
        todo = ToDoModel(id=args['id'], todo=args['todo'])
        result = ToDoModel.query.filter_by(id=args['id']).first()
        if result:
            abort(409, message='ID provided already exists')
        db.session.add(todo)
        db.session.commit()
        return todo, 201

    # Responds to patch requests. This is used to remove to-dos from the database. Will return a 404
    # code if the ID included with the request is not found in the database. 
    @marshal_with(resource_fields)
    def patch(self):
        parser = ArgumentParser()
        args = parser.update_args.parse_args()
        result = ToDoModel.query.filter_by(id=args['id']).first()
        if not result:
            abort(404, message="ID provided does not exist")
        db.session.delete(result)
        db.session.commit()
        return result, 201
    
# Adds the "/todo" endpoint to the URI. This is the endpoint that is serviced by the prior TodoResource class.
api.add_resource(TodoResource, "/todo")

if __name__ == '__main__':

    # Runs the API 
    app.run()