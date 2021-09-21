from threading import Thread
from .digitalTree import DigitalTree
from .user import User

class UserLoader(Thread):

    loader = None

    def __init__(self,tree:DigitalTree):
        Thread.__init__(self)
        self.__tree = tree

    #override run function
    def run(self):
        usernames = User.getAllUsers()
        for name in usernames:
            self.__tree.addWord(name)
    