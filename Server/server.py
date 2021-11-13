from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import parse_qs
import json
from login_database import *
from passlib.hash import bcrypt
from http import cookies
from SessionStore import *
from erikaChatBot import *


##################################
"""

APIs list:

need login first
- deleteUser (localhost:8080/users/(userID) method delete)
- updateUserName (localhost:8080/users/(userID)/updateName method PUT)
- updateUserPassword (localhost:8080/users/(userID)/updatePassword method PUT)

- auth (localhost:8080/sessions method POST)
- logout (localhost:8080/logout method GET)
- createUser (localhost:8080/users method POST)
- getAllUser (localhost:8080/users GET)
- getOneUser (localhost:8080/users/(userID) GET)


"""
##################################

gSessionStore = SessionStore()

# robot = Robot()


class MyRequestHandler(BaseHTTPRequestHandler):
    def loadCookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def sendCookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def loadSession(self):
        self.loadCookie()

        if "sessionID" in self.cookie:
            sessionID = self.cookie["sessionID"].value
            self.sessionData = gSessionStore.getSessionData(sessionID)
            if self.sessionData == None:
                sessionID = gSessionStore.createSession()
                self.sessionData = gSessionStore.getSessionData(sessionID)
                self.cookie["sessionID"] = sessionID

        else:
            sessionID = gSessionStore.createSession()
            self.sessionData = gSessionStore.getSessionData(sessionID)
            self.cookie["sessionID"] = sessionID

    ####

    def isLogin(self):
        if "userID" not in self.sessionData:
            self.handle401()
            return False
        else:
            return True

    def end_headers(self):
        self.sendCookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-COntrol-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def handle422(self):
        self.send_response(422)
        self.end_headers()

    def handle401(self):
        self.send_response(401)
        self.end_headers()

    def handle444(self):
        self.send_response(444)
        self.end_headers()

    def handle200(self):
        self.send_response(200)
        self.end_headers()

    def handle400(self):
        self.send_response(400)
        self.end_headers()

    def handle201(self):
        self.send_response(201)
        self.end_headers()

    def handle204(self):
        print("Ok but not content")
        self.send_response(204)
        self.end_headers()
    

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found!", "utf-8"))
    
    ######################################################
    #
    # Auth API
    #

    def logOut(self):
        self.loadCookie()

        if "sessionID" in self.cookie:
            sessionID = self.cookie['sessionID'].value
            self.sessionData = gSessionStore.getSessionData(sessionID)
            if self.sessionData != None:
                self.sessionData = gSessionStore.deleteSessionData(sessionID)
                self.handle200()

    def handleAuthenticateUser(self):
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(request_body)

        if "userName" not in parsed_body:
            print("missing userName")
            self.handle400()
            return
        name = parsed_body["userName"][0]

        if "userPassword" not in parsed_body:
            print("missing userPassword")
            self.handle400()
            return
        password = parsed_body["userPassword"][0]

        db = Database()
        checkExist = db.getUserByUserName(name)
        
        if checkExist != None and bcrypt.verify(password, checkExist[0]["userPassword"]):
            self.sessionData["userID"] = checkExist[0]["userID"]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        else:
            self.handle401()

    #########################################################
    #
    # User APIs:
    # 
    def getUserS(self):
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(request_body)

        if "userID" not in parsed_body:
            self.handle400()
            return
        userID = parsed_body["userID"][0]

        if userID == "*":
            self.send_response(200)
            self.send_header("Content-type", "appliction/json")
            self.end_headers()

            db = Database()
            allUserS = db.getAllUserS()
            self.wfile.write(bytes(json.dumps(allUserS), "utf-8"))

        try:
            userID = int(userID)
        except ValueError:
            # Handle the exception
            self.handle400
            return
        
        self.getOneUser(userID)

    def createUser(self):
        length = int(self.headers["Content-Length"])

        request_body = self.rfile.read(length).decode("utf-8")
        # print("The request body: ", request_body)

        parsed_body = parse_qs(request_body)
        print("the parsed body:", parsed_body)

        if "userName" not in parsed_body:
            print("need userName")
            self.handle400()
            return
        userName = parsed_body['userName'][0]

        if "userPassword" not in parsed_body:
            print("need userPassword")
            self.handle400()
            return
        userPassword = parsed_body['userPassword'][0]

        hashed = bcrypt.hash(userPassword)

        db = Database()
        userID = db.createUser(userName, hashed)
        if userID != None:
            if userID == -169:
                print("userName {userName} is existed try a new one")
                self.handle400()
            else:
                self.handle201()
        else:
            self.handle444()

    def getOneUser(self, userID):
        db = Database()
        userRecord = db.getUserByID(userID)
        if userRecord != None:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(bytes(json.dumps(userRecord), "utf-8"))
        else:
            print("User not found")
            self.handleNotFound()

    def deleteUser(self):
        if self.isLogin():
            length = int(self.headers["Content-Length"])
            request_body = self.rfile.read(length).decode("utf-8")
            parsed_body = parse_qs(request_body)

            if "userID" not in parsed_body:
                print("need userID")
                self.handle400()
                return
            userID = parsed_body["userID"][0]  

            try:
                userID = int(userID)
            except ValueError:
                # Handle the exception
                self.handle400
                return

            db = Database()
            userRecord = db.getUserByID(userID)
            if userRecord != None:
                db.deleteUser(userID)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(bytes(json.dumps(userRecord), "utf-8"))
            else:
                print("User not found")
                self.handleNotFound()
        else:
            self.handle401()

    def updateUserName(self, userID):
        if self.isLogin():
            db = Database()
            userRecord = db.getUserByID(userID)
            if userRecord != None:
                length = int(self.headers["Content-Length"])
                request_body = self.rfile.read(length).decode("utf-8")
                parsed_body = parse_qs(request_body)

                if "updateName" not in parsed_body:
                    print("need updateName")
                    self.handle400()
                    return
                newName = parsed_body["updateName"][0]

                user = db.updateUserName(userID, newName)
                if user != -169:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                else:
                    print("updateName: name is existed")
                    self.handle400()
            else:
                print("User not found")
                self.handleNotFound()
        else:
            self.handle401()

    def updateUserPwd(self, userID):
        if self.isLogin():
            db = Database()
            userRecord = db.getUserByID(userID)
            if userRecord != None:
                length = int(self.headers["Content-Length"])
                request_body = self.rfile.read(length).decode("utf-8")
                parsed_body = parse_qs(request_body)

                if "updatePassword" not in parsed_body:
                    print("need updatePassword")
                    self.handle400()
                    return
                newPwd = parsed_body["updatePassword"][0]

                hashed = bcrypt.hash(newPwd)

                user = db.updateUserPassword(userID, hashed)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

            else:
                print("User not found")
                self.handleNotFound()
        else:
            self.handle401()

    def update(self):
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(request_body)

        if "userID" not in parsed_body:
            print("need userID")
            self.handle400()
            return
        userID = parsed_body["userID"][0]

        try:
            userID = int(userID)
        except ValueError:
            # Handle the exception
            self.handle400
            print("there is not id")
            return
        
        if "type" not in parsed_body:
            print("need type")
            self.handle400()
            return
        type = parsed_body["type"][0]

        if type == "updateName":
            self.updateUserName(userID)
        elif type == "updatePassword":
            self.updateUserPwd(userID)
        else:
            print("wrong type name")
            self.handle400

    #######################################################
    #
    # Chat APIs:
    #

    def chatConversation(self):
        if self.isLogin():
            length = int(self.headers["Content-Length"])

            request_body = self.rfile.read(length).decode("utf-8")
            # print("The request body: ", request_body)

            parsed_body = parse_qs(request_body)
            print("the parsed body:", parsed_body)

            if "userInput" not in parsed_body:
                print("need userInput")
                self.handle400()
                return
            userInput = parsed_body["userInput"][0]

            if "userID" not in parsed_body:
                print("need userID")
                self.handle400()
                return
            userID = parsed_body["userID"][0]

            # robot = Robot() 
            response = test(userInput)
            print(response)

            db = Database()
            response = db.storeChat(userID, userInput, response)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), "utf-8"))

        else:
            self.handle401()

    def getChatHistory(self):
        if self.isLogin():
            length = int(self.headers["Content-Length"])

            request_body = self.rfile.read(length).decode("utf-8")
            # print("The request body: ", request_body)

            parsed_body = parse_qs(request_body)
            print("the parsed body:", parsed_body)

            if "userID" not in parsed_body:
                print("need userID")
                self.handle400()
                return
            userID = parsed_body["userID"][0]

            db = Database()
            history = db.getChatHistory(userID)
            if history == None:
                self.handle204()
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(json.dumps(history), "utf-8"))

        else:
            self.handle401()


    ##################################################

    def do_OPTIONS(self):
        self.loadSession()

        # 204: OK, not body
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Context-type")
        self.end_headers()

    def do_GET(self):
        self.loadSession()
        print("the request path is :", self.path)
        path_parts = self.path.split("/")
        collection = path_parts[1]

        if collection == "users":
                self.getUserS()
        elif collection == "chat":
            self.getChatHistory()
        elif self.path == "/logout":
            self.logOut()
        else:
            print("do_GET not found")
            self.handleNotFound()

    def do_POST(self):
        self.loadSession()

        print("the request path is :", self.path)
        if self.path == "/sessions":
            self.handleAuthenticateUser()
        elif self.path == "/users":
            self.createUser()
        elif self.path == "/chat":
            self.chatConversation() 

        else:
            print("do_POST not found")
            self.handleNotFound()

    def do_DELETE(self):
        self.loadSession()

        print("the request path is :", self.path)
        path_parts = self.path.split("/")
        collection = path_parts[1]

        if collection == "user":
            self.deleteUser()
        else:
            self.handleNotFound()

    def do_PUT(self):
        self.loadSession()

        print("the request path is :", self.path)
        path_parts = self.path.split("/")
        collection = path_parts[1]

        if collection == "users":
            self.update()
        else:
            print('No collection')
            self.handleNotFound()


        #####


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass  # nothing to see here


def run():
    # the main funciton
    listen = ("127.0.0.1", 8080)
    server = ThreadedHTTPServer(listen, MyRequestHandler)
    print("The server is running!")
    server.serve_forever()
    print("This will never, ever excute.")


run()
