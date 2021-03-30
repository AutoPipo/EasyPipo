
import random, datetime, os

class Sessions:
    def __init__(self):
        self.__session_id = self.__makeSession()
        
    def __makeSession(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        session_id = nowTime + str(random.randint(11 , 999999))
        return session_id
        
    def getSession(self):
        return self.__session_id