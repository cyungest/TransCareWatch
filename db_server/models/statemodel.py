import sqlite3
import random
import re
import datetime
import json

def to_dict(state_tuple):
        dictionary = {}

        dictionary["id"] = state_tuple[0]
        dictionary["name"] = state_tuple[1]
        dictionary["overview"] = json.loads(state_tuple[2])
        dictionary["doctorList"] = state_tuple[3]
        dictionary["visits"] = state_tuple[4]
        
        return dictionary

class State:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "states"

    
    def initialize_states_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    overview TEXT,
                    doctorList TEXT,
                    visits INT
                );
                """
        
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()

    def get_states(self):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            query = f"SELECT * from {self.table_name}"
            results=cursor.execute(query)
            list = results.fetchall()
            returnlist = []
            for states in list:
                returnlist.append(to_dict(states))


            return {"result": "success",
                    "message": returnlist
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
            
        finally:
            db_connection.close()

    def get_state(self, name = ""):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            print("Here is the state" + name)
            if name:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.name = '{name}';"
                results = cursor.execute(query)
                results = results.fetchone()
                
                cursor.execute(f"UPDATE {self.table_name} SET visits = visits + 1 WHERE name = '{name}';")
                db_connection.commit()
                print(results)
                if results:
                    return {"result": "success",
                            "message": to_dict(results)
                            }
                
            return {"result": "error",
            "message": "ONCE AGAIN I HAVE NO IDEA HOW U GOT THIS ERROR."
            }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def create_state(self, data):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            tupleData = (data["name"], json.dumps(data["overview"]), "", 0)
            print(data)
            #are you sure you have all data in the correct format?

            cursor.execute(f"INSERT INTO {self.table_name}(name,overview,doctorList,visits) VALUES (?, ?,?,?);", tupleData)
            db_connection.commit()
            return {"result": "success",
                    "message": self.get_state(name = data["name"])["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()


    def update_state(self, name = "", updateList = {}):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            state_name = name 

            if self.get_state(name = state_name)["result"] == "error":
                return {"result":"error",
                    "message":"I don't even know how you got this error. The names of the states are in the embed of the svg!"}
            updateList['overview'] = json.dumps(updateList['overview'])
            for key in updateList:
                cursor.execute(f"UPDATE {self.table_name} SET {key} = '{updateList[key]}' WHERE name = '{name}'")
                db_connection.commit()
            return {"result": "success",
                    "message": self.get_state(name = state_name)["message"]
                    }

        except sqlite3.Error as error:
            print(error)
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    
