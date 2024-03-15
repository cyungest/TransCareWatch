#BY ELLE YUNG 3/24 - 5/24

from flask import Flask
from flask import request
from flask_cors import CORS

import controllers.UsersController as UsersController
import controllers.StatesController as StatesController
import controllers.DoctorsController as DoctorsController

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

app.add_url_rule('/users', view_func=UsersController.get_users, methods = ['POST', 'GET'])
app.add_url_rule('/users/doctors/<user_name>', view_func=UsersController.get_userdoctors)
app.add_url_rule('/users/<user_name>', view_func=UsersController.interact_user, methods = ['GET','PUT', 'DELETE'])

app.add_url_rule('/states', view_func=StatesController.get_states)
app.add_url_rule('/states/doctors/<name>', view_func=StatesController.getstatedoctors)
app.add_url_rule('/states/<name>', view_func=StatesController.interact_state, methods = ['GET','PUT'])

