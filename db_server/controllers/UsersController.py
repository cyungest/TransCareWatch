from flask import request
from flask import jsonify

import os
from models.usermodel import User
from models.doctormodel import Doctor
from models.statemodel import State

tcw_db_name=f"{os.getcwd()}/models/tcwDB.db"

users = User(tcw_db_name)
doctors = Doctor(tcw_db_name)
states = State(tcw_db_name)


def get_users():
    #Returns all user objects
    # curl "http://127.0.0.1:5000"   

    print(f"request.url={request.url}")
    if request.method == "GET":
        return users.get_users()["message"]
    elif request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
           # or request.is_json:
            data = request.json
            new_user = users.create_user(data)
            print(new_user["message"])
            return new_user["message"]
        else:
            return {}

def get_userdoctors(email):
    user = users.get_user(email = email)
    if user["result"] == "error":
        return []
    doctorIDs = user["message"]["savedDoctorIDs"]
    if doctorIDs == []:
        return []

    doctorList = []
    for id in doctorIDs:
        doctorList.append(doctors.get_doctor(id = id))
    
    
    return doctorList

def userExists(email):
    return users.exists(email = email)

def interact_user(email):
    if request.method == "GET":
        print(email)
        user = users.get_user(email=email)
        print(user["message"])
        if user["result"] == "error":
            return {}
        return user["message"]
    elif request.method == "PUT":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
           # or request.is_json:
            data = request.json
            user_id = users.get_user(email=data["email"])["message"]["id"]
            updated_user = users.update_user(id = user_id, updateList = data)
            if updated_user["result"] == "error":
                return {}
            return updated_user["message"]
        else:
            return {}
    elif request.method == "DELETE":
        return_message = users.remove_user(email=email)
        if return_message["result"] == "success":
            return return_message["message"]
        else:
            return {}