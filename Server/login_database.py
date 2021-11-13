import sqlite3
import os
from sqlite3 import Error

############################

dbName = "top_secret.db"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, dbName)

os.makedirs(BASE_DIR, exist_ok=True)
db = sqlite3.connect(db_path)
db.execute('CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY, userName TEXT NOT NULL, userPassword TEXT NOT NULL)')
db.close()

"""
CREATE TABLE users (
	userID INTEGER PRIMARY KEY,
	userName TEXT NOT NULL,
	userPassword TEXT NOT NULL
);
"""
############################


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database:
    def __init__(self):
        print(db_path)
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        return

    def getAllUserS(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        if users == []:
            return None
        else:
            return users

    # return User by looking its IDS
    def getUserByID(self, useID):
        data = [useID]
        self.cursor.execute("SELECT * FROM users WHERE userID = ?", data)
        user = self.cursor.fetchone()
        if user == []:
            return None
        else:
            return user

    # in userName, userPassword
    # out None(create more than one users or DON'T create any)
    #      /userID the one just create
    def createUser(self, userName, userPassword):
        old_rowcount = 0

        if self.getUserByUserName(userName) != None:
            return -169  # mean this userName already exist

        data = [userName, userPassword]
        self.cursor.execute(
            "INSERT INTO users (userName, userPassword) VALUES (?,?)", data)
        self.connection.commit()
        new_rowcount = self.cursor.rowcount

        if new_rowcount == old_rowcount + 1:
            return self.cursor.lastrowid
        elif new_rowcount - old_rowcount > 1:
            print(new_rowcount, old_rowcount)
            print(f"Add {new_rowcount-old_rowcount} this time")
            return None
        elif new_rowcount == old_rowcount:
            print("No user create this time")
            return None

    # delete user by its userID
    def deleteUser(self, userID):
        data = [userID]
        self.cursor.execute("DELETE FROM users WHERE userID = ?", data)
        self.connection.commit()

    def updateUserName(self, userID, newName):
        if self.getUserByUserName(newName) == None:
            data = [newName, userID]
            self.cursor.execute(
                "UPDATE users SET userName = ? WHERE userID = ?", data)
            self.connection.commit()
            return self.getUserByID(userID)
        else:
            return -169

    def updateUserPassword(self, userID, newPwd):
        data = [newPwd, userID]
        self.cursor.execute(
            "UPDATE users SET userPassword = ? WHERE userID = ?", data)
        self.connection.commit()
        return self.getUserByID(userID)

    def getUserByUserName(self, name):
        data = [name]
        self.cursor.execute("SELECT * FROM users WHERE userName = ?", data)
        users = self.cursor.fetchall()
        if users == []:
            return None
        else:
            return users

    def getLastUserID(self):
        return self.getUserCount()[0]['count(1)']

    def getUserCount(self):
        self.cursor.execute("SELECT count(1) from users")
        return self.cursor.fetchall()
