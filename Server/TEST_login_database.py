from login_database import *


def test_getAllUserS():
    db = Database()
    print("------\ntest_getAllUserS")
    print(db.getAllUserS())
    print("------\n")


def test_getUserByID(userID=0):
    db = Database()
    print("------\ntest_getUserByID")
    print("if not id supply then use id = 0")
    print(db.getUserByID(userID))
    print("------\n")


def test_getUserByName(name="test"):
    db = Database()
    print("------\ntest_getUserByName")
    print("if not id supply then use userName = test")
    print(db.getUserByUserName(name))
    print("------\n")


def test_createUser(userName, userPassword):
    db = Database()
    print("------\ntest_createUser")
    print("name: test pwd: test")
    userID = db.createUser("TEST", "TEST")
    if userID == None:
        print("crateUser() return None it can be NO user created or create more than one users")
    else:
        print(f"UserID : {userID} created")
    print("------\n")


def test_deleteUser(self, userID=-1):
    db = Database()
    print("------\ntest_deleteUser")
    print("if no userID suppply will deleter the last id in the database")
    userID = db.deleteUser()
    if userID == None:
        print("crateUser() return None it can be NO user created or create more than one users")
    else:
        print(f"UserID : {userID} created")
    print("------\n")
