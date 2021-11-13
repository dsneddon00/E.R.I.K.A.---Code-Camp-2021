from login_database import *


##############################
#
# TEST CASES SETTING
#
# test_getUserByID
getUserID = 1

# test_getUserByName
name = "test"

# test_createUser
userName = "test"
userPassword = "test"

# test_deleteUser
deleteUserID = -1

##############################


def test_getAllUserS():
    db = Database()
    print("------\ntest_getAllUserS")
    print(db.getAllUserS())
    print("------\n")


def test_getUserByID(uID):
    db = Database()
    print("------\ntest_getUserByID")
    print("if not id supply then use id = 1")
    print(db.getUserByID(uID))
    print("------\n")


def test_getUserByName(n):
    db = Database()
    print("------\ntest_getUserByName")
    print("if not id supply then use userName = test")
    print(db.getUserByUserName(n))
    print("------\n")


def test_createUser(uName, uPassword):
    db = Database()
    print("------\ntest_createUser")
    print("name: test pwd: test")
    userID = db.createUser(uName, uPassword)
    if userID == None:
        print("crateUser() return None it can be NO user created or create more than one users")
    elif userID == -169:
        print("This userName already exist")
    else:
        print(f"UserID : {userID} created")
        print(db.getUserByID(userID))
    print("------\n")


def test_deleteUser(uID):
    db = Database()
    print("------\ntest_deleteUser")
    print("if no userID suppply will deleter the last id in the database")
    if uID == -1:
        uID = db.getLastUserID()
    print(f"Will deleter UserID {uID}")
    db.deleteUser(uID)
    print(f"deleted UseID {uID}")
    user = db.getUserByID(uID)
    print(f"getUserByID ID: {uID} User: {user}")
    print(db.getAllUserS())
    print("------\n")


def test_ALL():
    test_getAllUserS()
    test_createUser(userName, userPassword)
    test_getUserByID(getUserID)
    test_getUserByName(userName)
    test_deleteUser(deleteUserID)


test_ALL()
