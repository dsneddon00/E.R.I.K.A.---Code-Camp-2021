# E.R.I.K.A.---Code-Camp-2021
E.R.I.K.A (Empathicly Reciprocating Intelligent Konnection Agent) is a web based mental health chat bot.

# let say you are at root dir of the repo
# haveing
```
Client    README.md Server
```

# Start up the Server
```
python3 Server/Server.py
```

# sqlite Database
```
sqlite3 Server/top_secret.db


select * from users;

select * from chats;
```

# for API testing:
```
userID: 12
userName: test1
userPassword: test1
```

APIs list:
# userName has to be UNIQUE

## Users related API
need login first
- deleteUser (method delete)
* localhost:8080/users
* send URL encoded utf-8 
* userID : (userID)

---

- updateUserName (method PUT)
* localhost:8080/users
* send: URL encoded utf-8
* userID : (userID)
* type : updateName (HAVE TO HARD CODE)
* updateName:(the new name)
* resp: 400(updateName: name is existed) | 401 (not found) | 200 (OK)

---

- updateUserPassword (method PUT)
* localhost:8080/users 
* send: URL encoded utf-8 
* userID : (userID)
* type : updatePassword (HAVE TO HARD CODE)
* updatePassword : (the new pwd)
* resp: 400(updateName: name is existed) | 401 (not found) | 200 (OK)

---

- auth ( method POST)
* localhost:8080/sessions
* send: URL encoded utf-8     
* userName : (name) 
* userPassword : (pwd)
* resp: 400(missing userName or pwd) | 401 (not found) | 200 (OK)

---

- logout (localhost:8080/logout method GET)

---

- createUser ( method POST)
* localhost:8080/users
* send URL encoded utf-8     
* userName : (name) 
* userPassword : (pwd)
* resp: 400(name is existed try a new one) | 401 (not found) | 201 (OK)

---

- getAllUser (GET method)
* localhost:8080/users
* send with URL encoded utf-8 
* userID : (userID or "*")  * mean getALL else get the matched userID one
* resp: 400(userID can't covert to int or bad)

---


## Chat related API

- getChatHistory (GET method)
* localhost:8080/chat
* send with URL encoded utf-8 
* userID : (userID)
* resp: 400(userID can't covert to int or bad or can't find it) 204 (OK but not history found)

----

- chatConversation (POST method)
* localhost:8080/chat
* send with URL encoded utf-8 
* userID : (userID)
* userInput : (userInput)
* resp: 400(userID can't covert to int or bad or can't find it) 200 (OK)