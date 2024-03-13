#BY ELLE YUNG 10/31/23

from flask import Flask
from flask import request
from flask_cors import CORS

import controllers.UsersController as UsersController
import controllers.StatesController as StatesController
import controllers.DoctorsController as DoctorsController

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)