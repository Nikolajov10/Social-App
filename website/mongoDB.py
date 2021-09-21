import pymongo
from pymongo import MongoClient


class MongoDb:
    client = None
    db = None
    collection:pymongo.collection.Collection= None
    collection2:pymongo.collection.Collection= None
    collection3:pymongo.collection.Collection= None
    collection4:pymongo.collection.Collection= None
    @staticmethod
    def initDB():
        if not MongoDb.client:
            MongoDb.client = MongoClient("mongodb+srv://<username>:<password>@cluster0.xnnul.mongodb.net/<db_name>?retryWrites=true&w=majority")
        if not MongoDb.db:
            MongoDb.db = MongoDb.client["App"]
        if not MongoDb.collection:
            MongoDb.collection = MongoDb.db["Posts"] # storing posts
        if not MongoDb.collection2:
            MongoDb.collection2 = MongoDb.db["Comments"] # storing comments
        if not MongoDb.collection3:
            MongoDb.collection3 = MongoDb.db["Friendship"] # storing friendships relation
        if not MongoDb.collection4:
            MongoDb.collection4 = MongoDb.db["Messages"] # storing messages
        

    @staticmethod
    def getPostId() -> int:
        """
        return: biggest post id
        """
        if not MongoDb.collection:
            MongoDb.initDB()
        results= MongoDb.collection.aggregate([
        { "$group": {
      "_id": "null",
      "MaximumValue": { "$max": "$_id" }}}])
        for res in results:
            return res["MaximumValue"]
        return 0

    @staticmethod
    def getCommentID() -> int:
        """
        return: biggest comment id
        """
        if not MongoDb.collection2:
            MongoDb.initDB()
        results= MongoDb.collection2.aggregate([
        { "$group": {
      "_id": "null",
      "MaximumValue": { "$max": "$_id" }}}])
        for res in results:
            return res["MaximumValue"]
        return 0
    
    @staticmethod
    def addPost(post):
        """
        param: post - Post
        adding post into Mongo database
        """
        MongoDb.collection.insert_one(post.__dict__)
    
    @staticmethod
    def getPosts():
        results= MongoDb.collection.find({})
        arr = []
        for result in results:
            arr.append(result)
        return arr

    @staticmethod
    def addLike(post_id,username):
        """
        appending username in likes array 
        where _id = post_id
        """
        MongoDb.collection.update_one({"_id":int(post_id)},{"$push":{"likes":username}})
    
    @staticmethod
    def deleteLike(post_id,username):
        """
        deleting username from likes likes array
        where _id = post_id
        """
        MongoDb.collection.update({"_id":int(post_id)},{"$pull":{"likes":username}})

    @staticmethod
    def addComment(comment):
        """
        param: comment - Comment
        adding comment into Mongo database
        """
        MongoDb.collection2.insert_one(comment.__dict__)
    
    @staticmethod
    def deleteComment(com_id):
        """
        param: com_id - int
        deleting comment from Mongo database
        """
        MongoDb.collection2.delete_one({"_id":int(com_id)})

    @staticmethod
    def getAllComments():
        """
        return: array off all comments
        """
        results = MongoDb.collection2.find({})
        arr = []
        for result in results:
            arr.append(result)
        return arr

    @staticmethod
    def addCommentToPost(post_id,com_id):
        """
        appending com_id in comments array 
        where _id = post_id
        """
        MongoDb.collection.update_one({"_id":int(post_id)},{"$push":{"comments":com_id}})

    @staticmethod
    def deleteCommentFromPost(post_id,com_id):
        """
        removing com_id in comments array 
        where _id = post_id
        """
        MongoDb.collection.update_one({"_id":int(post_id)},{"$pull":{"comments":int(com_id)}})

    @staticmethod
    def insertUserFriendship(username):
        """
        creating user document in 
        friendship collection
        function called when sign up
        """
        if not MongoDb.collection3:
            MongoDb.initDB()
        document = {
            "username":username,
            "friends" : []
        }
        MongoDb.collection3.insert_one(document)

    @staticmethod
    def makeFriendship(username1,username2):
        """
        insert username2 to friends array of username 1
        and vice versa
        """
        MongoDb.collection3.update_one({"username":username1},{"$push":{"friends":username2}})
        MongoDb.collection3.update_one({"username":username2},{"$push":{"friends":username1}})

    @staticmethod
    def getFriends(username):
        """
        return: list of all friends
        """
        results = MongoDb.collection3.find({"username":username})
        for result in results:
            return result["friends"]
        return None

    @staticmethod
    def insertMessage(username,message):
        """
        inserting message to username
        param: message - Message
               username - str
        """
        # if there is no history for username,insert new document
        result = MongoDb.collection4.find({"username":username})
        found=False
        for res in result:
            found=True
            break
        if not found:
            MongoDb.collection4.insert_one({"username":username,"messages":[message.__dict__]})
        else:
            MongoDb.collection4.update_one({"username":username},{"$push":{"messages":message.__dict__}})

    @staticmethod
    def getMessagesHistory(username):
        """
        returns array of messages(dict) for username
        """
        results = MongoDb.collection4.find({"username":username})
        if results:
            for result in results:
                return result["messages"]
        return [] # if user has no history