import os
import base64


class SessionStore:
    def __init__(self):
        self.sessions = {}

    def createSession(self):
        sessionID = self.createSessionID()
        self.sessions[sessionID] = {}
        return sessionID

    def createSessionID(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    def getSessionData(self, sessionID):
        if sessionID in self.sessions:
            return self.sessions[sessionID]
        else:
            return None

    def deleteSessionData(self, sessionID):
        if sessionID in self.sessions:
            self.sessions[sessionID] = None
        return self.sessions[sessionID]
