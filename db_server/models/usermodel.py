import sqlite3
import random
import re
import json

def to_dict(user_tuple):
        dictionary = {}

        dictionary["id"] = user_tuple[0]
        dictionary["email"] = user_tuple[1]
        dictionary["location"] = user_tuple[2]
        dictionary["savedDoctorIDs"] = user_tuple[3]
        
        return dictionary

class User:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "users"

    
    def initialize_users_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    location TEXT,
                    savedDoctorIDs TEXT
                );
                """
        
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def get_users(self):
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

    def get_user(self, id = None, email = None):
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
            elif email:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.email = '{email}';"
                results = cursor.execute(query)
                results = results.fetchone()
                if results:
                    return {"result": "success",
                            "message": to_dict(results)
                            }
            return {"result": "error",
            "message": "There is no user with this email/id."
            }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def create_user(self, user_details):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            print(user_details)

            if not "@" in user_details["email"]:
                return {"result":"error","message":"EMAIL DORNT HAVE A @"}
            elif not "." in user_details["email"].split("@")[1]:
                return {"result":"error","message":"IMPROBER EMAIL FORMOT"}
            

            user_data = (user_details["email"])
            #are you sure you have all data in the correct format?
            print(user_data)


            cursor.execute(f"INSERT INTO {self.table_name}(email,location,savedDoctorIDs) VALUES ('{user_data}', '', '');")
            db_connection.commit()
            return {"result": "success",
                    "message": self.get_user(email = user_details["email"])["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    

    def exists(self, id = None, email = None):
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
            
            
            elif email:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.email = '{email}';"
                results = cursor.execute(query)
                if results.fetchone():
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

        
    
    def update_user(self, id = None, updateList = {}):
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
                    "message": self.get_user(id=id)
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def remove_user(self, email = ''):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            deleted_user = self.get_user(email = email)["message"]

            if self.get_user(email = email)["result"] == "error":
                return {"result":"error",
                    "message":"User doesn't exist"}
            
            query = f"DELETE FROM {self.table_name} WHERE {self.table_name}.email = '{email}';"
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