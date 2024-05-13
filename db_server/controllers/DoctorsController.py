from flask import request
from flask import jsonify

import os
from models.usermodel import User
from models.doctormodel import Doctor
from models.statemodel import State
from models.statsmodel import Stat

tcw_db_name=f"{os.getcwd()}/models/tcwDB.db"

users = User(tcw_db_name)
doctors = Doctor(tcw_db_name)
states = State(tcw_db_name)
stats = Stat(tcw_db_name)


def get_doctors():
    #Returns all user objects
    # curl "http://127.0.0.1:5000"   

    print(f"request.url={request.url}")
    if request.method == "GET":
        return doctors.get_doctors()["message"]
    elif request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
           # or request.is_json:
            data = request.json
            new_doctor = doctors.create_doctor(doc_details = data)
            print(new_doctor["message"])
            return new_doctor["message"]
        else:
            return {}

def interact_doctor(name):
    if request.method == "GET":
        print(name)
        doctor = doctors.get_doctor(name=name)
        if doctor["result"] == "error":
            return {}
        return doctor["message"]
    elif request.method == "PUT":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
           # or request.is_json:
            data = request.json
            updated_doctor = doctors.update_doctor(name = name, updateList = data)
            print(updated_doctor["message"])
            if updated_doctor["result"] == "error":
                return {}
            return updated_doctor["message"]
        else:
            return {}
    elif request.method == "DELETE":
        return_message = doctors.remove_doctor(name=name)
        if return_message["result"] == "success":
            return return_message["message"]
        else:
            return {}