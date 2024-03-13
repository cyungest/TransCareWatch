import sqlite3
import random
import re
import datetime
import json

def to_dict(user_tuple):
        dictionary = {}

        dictionary["id"] = user_tuple[0]
        dictionary["name"] = user_tuple[1]
        dictionary["stateID"] = user_tuple[2]
        dictionary["overview"] = user_tuple[3]
        dictionary["contactInfo"] = json.loads(user_tuple[4])
        
        return dictionary

class Doctors:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "doctors"

    
    def initialize_doctors_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    stateID INT,
                    overview TEXT,
                    contactInfo TEXT
                );
                """
        
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def get_doctors(self):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            query = f"SELECT * from {self.table_name}"
            results=cursor.execute(query)
            list = results.fetchall()
            returnlist = []
            for users in list:
                returnlist.append(to_dict(users))


            return {"result": "success",
                    "message": returnlist
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
            
        finally:
            db_connection.close()
    
    def get_doctor(self, name = "", id = ""):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if id:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {id};"
                results = cursor.execute(query)
                results = results.fetchone()
                if results:
                    return {"result": "success",
                            "message": to_dict(results)
                            }
            elif name:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.name = '{name}';"
                results = cursor.execute(query)
                results = results.fetchone()
                if results:
                    return {"result": "success",
                            "message": to_dict(results)
                            }
            return {"result": "error",
            "message": "There is no user with this username/id."
            }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    

    def get_doctor_by_location(self, stateID = ""):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            query = f"SELECT * from {self.table_name} WHERE {self.table_name}.stateID = {stateID};"
            results = cursor.execute(query)
            results = results.fetchall()
            returnlist = []
            for users in results:
                returnlist.append(to_dict(users))
            if results:
                return {"result": "success",
                        "message": returnlist
                        }

        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def create_doctor(self, doc_details):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            doc_data = (doc_details["name"], doc_details["stateID"], doc_details["overview"], doc_details["contactInfo"])
            #are you sure you have all data in the correct format?

            cursor.execute(f"INSERT INTO {self.table_name}(name,stateID,overview,contactInfo) VALUES (?, ?, ?, ?);", doc_data)
            db_connection.commit()
            return {"result": "success",
                    "message": self.get_user(name = doc_details["name"])["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def exists(self, name = None, id = None):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if id:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {id};"
                results = cursor.execute(query)
                if results.fetchone():
                    return {"result": "success",
                    "message": True
                    }
            
            elif name:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.name = '{name}';"
                results = cursor.execute(query)
                list = results.fetchall()
                if list:
                    return {"result": "success",
                    "message": True
                    }
            
            return {"result": "success",
                    "message": False
                    }
            

        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def update_doctor(self, id = None, updateList = {}):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            if not self.exists(id)["message"]:
                return {"result":"error",
                    "message":"User doesn't exist"}
            
            for key in updateList:
                cursor.exectute(f"UPDATE {self.table_name} SET {key} = {updateList[key]} WHERE id = {id}")
            db_connection.commit()
            return {"result": "success",
                    "message": self.get_doctor(id = id)
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def remove_user(self, name = ''):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            deleted_user = self.get_doctor(name = name)["message"]

            if self.get_doctor(name = name)["result"] == "error":
                return {"result":"error",
                    "message":"User doesn't exist"}
            
            query = f"DELETE FROM {self.table_name} WHERE {self.table_name}.name = '{name}';"
            results = cursor.execute(query)

            db_connection.commit()
            return {"result": "success",
                    "message": deleted_user
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
