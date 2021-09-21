import sqlite3
from datetime import datetime

class DB:

    DB_NAME="users.db"
    
    @staticmethod
    def createDatabase():
        """
        creating Users table 
        """
        db = sqlite3.connect(DB.DB_NAME)
        cursor = db.cursor()
        query_create = "CREATE TABLE IF NOT EXISTS Users(\
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    name VARCHAR(40) UNIQUE,\
                    email VARCHAR(100) UNIQUE,\
                    password VARCHAR(500))"
        cursor.execute(query_create)
        db.commit()
        db.close()

    @staticmethod
    def getUsers():
        db = sqlite3.connect(DB.DB_NAME)
        cursor = db.cursor()
        query = "SELECT name from Users"
        results = cursor.execute(query)
        names= []
        for result in results:
            names.append(result[0])
        db.close()
        return names

    @staticmethod
    def checkUser(name):
        """
        checking if user is in database and check is password good
        return: boolean
        """
        db = sqlite3.connect(DB.DB_NAME)
        cursor = db.cursor()
        query = "SELECT password FROM Users WHERE name = ?" 
        res =  cursor.execute(query,(name,))
        for r in res:
            db.close()
            return r[0]
        db.close()
        return None

    @staticmethod
    def insertUser(name,email,password):
        """
        inserting user data into database
        params: name : string, email : string, password : string
        return: True if is successfully inserted,otherwise False
        """
        db = sqlite3.connect(DB.DB_NAME)
        cursor = db.cursor()
        query = "INSERT INTO Users(name,email,password)\
                    VALUES (?,?,?);"
        values = (name,email,password)
        try:
            cursor.execute(query,values)
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            db.commit()
            db.close()
