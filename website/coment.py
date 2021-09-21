from .mongoDB import MongoDb


class Comment:
    ID = MongoDb.getCommentID()
    def __init__(self,text,user_name):
        self._id = Comment.ID + 1
        self.text = text
        self.user_name = user_name
        Comment.ID += 1

        MongoDb.addComment(self)
    
    def getId(self):
        return self._id

    @staticmethod
    def getComments():
        """
        maps comment_id to text and entry
        return: dict(dict())
        """
        arr = MongoDb.getAllComments()
        comments_dict  = dict()
        for entry in arr:
            comments_dict[entry["_id"]] = {"text":entry["text"],"username":entry["user_name"]}
        return comments_dict

    @staticmethod
    def deleteComment(com_id):
        MongoDb.deleteComment(com_id)

    