from .database import DB
from .mongoDB import MongoDb
from .search import Search

class User:
    current_user = None
    def __init__(self,name):
        self.__name = name
    
    def getName(self):
        return self.__name

    @staticmethod
    def getAllUsers() -> list[str]:
        return DB.getUsers()

    @staticmethod
    def logUser(name,password):
        if not User.current_user:
            password = DB.checkUser(name)
            if password:
                User.current_user = User(name)
                return password
        return None
    
    @staticmethod
    def signUpUser(name,email,password):
        if not User.current_user:
            # sign up check 
            success = DB.insertUser(name,email,password)
            if success:
                User.current_user = User(name)
                MongoDb.insertUserFriendship(name)
                Search.tree.addWord(name)

    @staticmethod
    def logoutUser():
        User.current_user = None