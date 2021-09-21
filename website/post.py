from datetime import datetime
from os import stat
from .mongoDB import MongoDb

class _Post:
    def __init__(self,**entries) :
        self.__dict__.update(entries)
    def __str__(self) -> str:
        return str(self.__dict__)

class Post:
    ID = MongoDb.getPostId()


    def __init__(self,text,user_name):
        self._id = Post.ID + 1
        self.text = text
        self.user_name = user_name
        self.likes = []
        self.comments = []
        today = datetime.utcnow()
        self.date = str(today)[:len(str(today))-7]
        Post.ID += 1
        # adding post to mongo database
        MongoDb.addPost(self)

    @staticmethod
    def addComment(post_id,comm_id):
        """
        adding comment to post
        storing only comment id
        """
        MongoDb.addCommentToPost(post_id,comm_id)      

    @staticmethod
    def deleteComment(post_id,com_id):
        """
        deleting comment from comments array
        """
        MongoDb.deleteCommentFromPost(post_id,com_id)

    @staticmethod
    def addLike(post_id,user_name):
        """
        adding user_name to array likes 
        """
        MongoDb.addLike(post_id,user_name)
    
    @staticmethod
    def deleteLike(post_id,user_name):
        """
        removing like from likes array
        """
        MongoDb.deleteLike(post_id,user_name)
    
    @staticmethod
    def getAllPosts():
        arr = MongoDb.getPosts()
        for index,entry in enumerate(arr):
            arr[index] = _Post(**entry)
        return arr
