import sqlite3
import random
import re
import json

def to_dict(user_tuple):
        dictionary = {}

        dictionary["id"] = user_tuple[0]
        dictionary["username"] = user_tuple[1]
        dictionary["password"] = user_tuple[2]
        dictionary["email"] = user_tuple[3]
        dictionary["location"] = user_tuple[4]
        dictionary["savedDoctorIDs"] = user_tuple[5]
        
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
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
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

    def get_user(self, id = None, username = None):
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
            elif username:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.username = '{username}';"
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

    def create_user(self, user_details):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if not "@" in user_details["email"]:
                return {"result":"error","message":"EMAIL DORNT HAVE A @"}
            elif not "." in user_details["email"].split("@")[1]:
                return {"result":"error","message":"IMPROBER EMAIL FORMOT"}
            
            if not user_details["username"].isalnum():
                return {"result":"error","message":"Username can only contain letters and numbers"}

            if len(user_details["password"]) < 8:
                return {"result":"error","message":"Password not long enough"}
            elif not re.search("[a-z]", user_details["password"]):
                return {"result":"error","message":"Password doesn't have a lower case letter."}
            elif not re.search("[A-Z]", user_details["password"]):
                return {"result":"error","message":"Password doesn't have a upper case letter."}
            elif not re.search("[0-9]", user_details["password"]):
                return {"result":"error","message":"Password doesn't have a number."}

            user_data = (user_details["username"], user_details["password"], user_details["email"], user_details["location"])
            #are you sure you have all data in the correct format?


            cursor.execute(f"INSERT INTO {self.table_name}(username,password,email,location,savedDoctorIDs) VALUES (?, ?, ?, ?, '');", user_data)
            db_connection.commit()
            return {"result": "success",
                    "message": self.get_user(username = user_details["username"])["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    

    def exists(self, username = None, id = None, email = None):
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
            
            elif username:
                query = f"SELECT * from {self.table_name} WHERE {self.table_name}.username = '{username}';"
                results = cursor.execute(query)
                list = results.fetchall()
                if list:
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
    
    def remove_user(self, username = ''):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            deleted_user = self.get_user(username = username)["message"]

            if self.get_user(username = username)["result"] == "error":
                return {"result":"error",
                    "message":"User doesn't exist"}
            
            query = f"DELETE FROM {self.table_name} WHERE {self.table_name}.username = '{username}';"
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