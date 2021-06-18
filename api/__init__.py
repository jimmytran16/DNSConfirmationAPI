from flask import Flask
from flask_restful import Api

# init the flask app
# pass the flask app instance to the Api constructor
app = Flask(__name__)
api = Api(app)

# import all the endpoints 
from .controllers.endpoints import *

