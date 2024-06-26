#BY ELLE YUNG 3/24 - 5/24

from flask import Flask
from flask import request
from flask_cors import CORS

import controllers.UsersController as UsersController
import controllers.StatesController as StatesController
import controllers.DoctorsController as DoctorsController
import controllers.StatsController as StatsController

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

app.add_url_rule('/users', view_func=UsersController.get_users, methods = ['POST', 'GET'])
app.add_url_rule('/users/doctors/<email>', view_func=UsersController.get_userdoctors)
app.add_url_rule('/users/<email>', view_func=UsersController.interact_user, methods = ['GET','PUT', 'DELETE'])
app.add_url_rule('/users/exists/<email>', view_func=UsersController.userExists)

app.add_url_rule('/states', view_func=StatesController.get_states, methods = ['POST', 'GET'])
app.add_url_rule('/states/doctors/<name>', view_func=StatesController.getstatedoctors)
app.add_url_rule('/states/<name>', view_func=StatesController.interact_state, methods = ['GET','PUT'])

app.add_url_rule('/doctors', view_func=DoctorsController.get_doctors, methods = ['POST', 'GET'])
app.add_url_rule('/doctors/<name>', view_func=DoctorsController.interact_doctor, methods = ['GET','PUT', 'DELETE'])

app.add_url_rule('/stats', view_func=StatsController.get_stats, methods = ['POST', 'GET'])
app.add_url_rule('/stats/count', view_func=StatsController.get_count)

app.run(debug=True, port=5000)