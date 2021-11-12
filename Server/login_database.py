import sqlite3
import os
from sqlite3 import Error

############################

dbName = "top_secret.db"

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
        self.connection = sqlite3.connect(dbName)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        return

    def getAllUserS(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        return users

    def getUserByID(self, useID):
        data = [useID]
        self.cursor.execute("SELECT * FROM users WHERE userID = ?", data)
        user = self.cursor.fetchone()
        return user

    def createUser(self, userName, userPassword):
        old_rowcount = 0

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

    def deleteUser(self, userID):
        data = [userID]
        self.cursor.execute("DELETE FROM users WHERE userID = ?", data)
        self.connection.commit()

    def getUserByUserName(self, name):
        data = [name]
        self.cursor.execute("SELECT * FROM users WHERE userName = ?", data)
        users = self.cursor.fetchall()
        return users

    def getLastUserID(self):
        return self.getUserCount()[0]['count(1)']

    def getUserCount(self):
        self.cursor.execute("SELECT count(1) from users")
        return self.cursor.fetchall()
