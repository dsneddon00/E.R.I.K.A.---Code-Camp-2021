# E.R.I.K.A.---Code-Camp-2021
E.R.I.K.A (Empathicly Reciprocating Intelligent Konnection Agent) is a web based mental health chat bot.


APIs list:
# userName has to be UNIQUE

need login first
- deleteUser (localhost:8080/users/(userID) method delete) 

- updateUserName (localhost:8080/users/(userID)/updateName method PUT)
> send: URL encoded utf-8 updateName:(the new name)
> resp: 400(updateName: name is existed) | 401 (not found) | 200 (OK)

- updateUserPassword (localhost:8080/users/(userID)/updatePassword method PUT)
> send: URL encoded utf-8 updatePassword:(the new pwd)
> resp: 400(updateName: name is existed) | 401 (not found) | 200 (OK)

- auth (localhost:8080/sessions method POST)
> send: URL encoded utf-8     userName:(name) userPassword:(pwd)
> resp: 400(missing userName or pwd) | 401 (not found) | 200 (OK)

- logout (localhost:8080/logout method GET)

- createUser (localhost:8080/users method POST)
> send: URL encoded utf-8     userName:(name) userPassword:(pwd)
> resp: 400(name is existed try a new one) | 401 (not found) | 201 (OK)

- getAllUser (localhost:8080/users GET)

- getOneUser (localhost:8080/users/(userID) GET)
