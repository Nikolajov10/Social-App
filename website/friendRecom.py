from .user import User
from .friendship import Friendship


class FriendRecommendation:
    users = User.getAllUsers()

    @staticmethod
    def getRecommendation(username):
        """
        return number of mutual friends
        with every user
        """
        friends = Friendship.getFriends(username)
        recomm = []
        # count mutual friends with every friend
        for user in FriendRecommendation.users:
            if user==username or user in friends:
                continue
            user_set = set(friends)
            friend_array = Friendship.getFriends(user)
            cnt = 0
            n = len(user_set) # remeber the len of initial set
            for friend in friend_array:
                user_set.add(friend)
                if len(user_set) != n:
                    n += 1
                else:
                    cnt +=1
            if cnt > 0:
                recomm.append((user,cnt))
        return sorted(recomm,key=lambda x:x[1],reverse=True)

        

