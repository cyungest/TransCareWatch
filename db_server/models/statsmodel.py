import sqlite3
import random
import re
import datetime
import json

def to_dict(input):
    dict = {}

    dict["id"] = input[0]
    dict["route"] = input[1]
    dict["email"] = input[2]

    return dict


class Stat:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "stats"

    
    def initialize_stats_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY,
                    route TEXT,
                    email TEXT
                );
                """
        
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()

    def get_stats(self):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            query = f"SELECT * from {self.table_name}"
            results=cursor.execute(query)
            list = results.fetchall()
            returnlist = []
            for requests in list:
                returnlist.append(to_dict(requests))


            return {"result": "success",
                    "message": returnlist
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
            
        finally:
            db_connection.close()

    def get_stat(self, id = ""):
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
                
            return {"result": "error",
            "message": "ONCE AGAIN I HAVE NO IDEA HOW U GOT THIS ERROR."
            }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def create_entry(self, details):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            data = (details["route"], details["email"])
            #are you sure you have all data in the correct format?

            cursor.execute(f"INSERT INTO {self.table_name}(route, email) VALUES (?, ?);", data)
            db_connection.commit()
            return {"result": "success",
                    "message": "created"
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_count(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if id:
                query = f"SELECT COUNT(*) from {self.table_name};"
                results = cursor.execute(query)
                return results
                
            return {"result": "error",
            "message": "ONCE AGAIN I HAVE NO IDEA HOW U GOT THIS ERROR."
            }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()