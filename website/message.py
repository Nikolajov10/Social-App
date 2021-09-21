from datetime import datetime
from typing import List
from website.mongoDB import MongoDb
import pytz

class Message:
    def __init__(self,msg,sender_name,receiver,time=None):
        self.text = msg
        self.sender = sender_name
        self.receiver = receiver
        self.time = time
        if not self.time:
            self.time = (datetime.now(pytz.timezone('Europe/Belgrade'))).strftime("%H:%M:%S")
        
    
    @staticmethod
    def messageToDocument(msg) -> dict:
        """
        Parser for MongoDB to convert message to Document Object
        :return: dict {"Text":self.text,"Sender"self.sender}
        """
        return msg.__dict__
    
    @staticmethod
    def documentToMessage(doc:dict):
        """

        :param doc: dict - MongoDB document
        :return: Message
        """
        return Message(doc["text"],doc["sender"],doc["receiver"],doc["time"])

    @staticmethod
    def insertMessage(username,doc:dict):
        MongoDb.insertMessage(username,Message.documentToMessage(doc))

    @staticmethod
    def getMessageHistory(username) -> list:
        """
        return: list of Message
        """
        messages = MongoDb.getMessagesHistory(username)
        for index,msg in enumerate(messages):
            messages[index] = Message.documentToMessage(msg)
        return messages