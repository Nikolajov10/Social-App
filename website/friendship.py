from .mongoDB import MongoDb

class Friendship:

    @staticmethod
    def makeFriendship(username1,username2):
        MongoDb.makeFriendship(username1,username2)

    @staticmethod
    def getFriends(username):
        return MongoDb.getFriends(username)