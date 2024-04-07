from flask import request
from flask import jsonify

import os
from models.usermodel import User
from models.doctormodel import Doctor
from models.statemodel import State
from models.statsmodel import Stats

tcw_db_name=f"{os.getcwd()}/models/tcwDB.db"

users = User(tcw_db_name)
doctors = Doctor(tcw_db_name)
states = State(tcw_db_name)
stats = Stats(tcw_db_name)

def get_stats():
    print(f"request.url={request.url}")
    if request.method == "GET":
        return stats.get_stats()["message"]
    elif request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
           # or request.is_json:
            data = request.json
            new_user = stats.create_entry(data)
            return new_user["message"]
        else:
            return {}

def get_count():
    return stats.get_count()