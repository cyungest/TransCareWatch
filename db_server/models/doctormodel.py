import sqlite3
import random
import re
import datetime
import json


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

