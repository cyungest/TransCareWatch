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

def get_states():
    #Returns all user objects
    # curl "http://127.0.0.1:5000"   

    print(f"request.url={request.url}")
    if request.method == "GET":
        return states.get_states()
    elif request.method == "POST":
            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
            # or request.is_json:
                data = request.json
                print(data)
                new_state = states.create_state(data = data)
                return new_state["message"]
            else:
                return {}

def getstatedoctors(name): 
    print(f"request.url={request.url}")
    stateID = states.get_state(name = name)["message"]["id"]
    return doctors.get_doctors_by_location(stateID=stateID)

def interact_state(name):
    if request.method == "GET":
        print(name)
        state = states.get_state(name=name)
        print(state["message"])
        if state["result"] == "error":
            return {}
        return state["message"]
    elif request.method == "PUT":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
           # or request.is_json:
            data = request.json
            updated_user = states.update_state(name = name, updateList=data)
            if updated_user["result"] == "error":
                return {}
            return updated_user["message"]
        else:
            return {}

