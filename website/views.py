import re
from .coment import Comment
from flask.helpers import flash
from website.user import User
from flask import Blueprint,url_for,render_template,redirect,request
from .post import Post
from .friendship import Friendship
from .search import Search
from .friendRecom import FriendRecommendation
from flask_socketio import SocketIO, send
from .socket import Socket
from .message import Message

views = Blueprint("views",__name__)

# decorator for checking if user is logged in
def check_login():
    if not User.current_user:
        return False
    return True


@views.route("/feed",methods=["POST","GET"])
def feed():
    if not check_login():
        return redirect(url_for("auth.login"))
    if request.method=="POST":
        comment_text = request.form.get("comment")
        value = request.form.get("hidden")
        value = value.split(',')
        username = value[0]
        post_id = value[1]
        comment = Comment(comment_text,username)
        Post.addComment(post_id,comment.getId())
    posts = Post.getAllPosts()
    comments = Comment.getComments() # dict type
    recomm = FriendRecommendation.getRecommendation(User.current_user.getName())
    friends = Friendship.getFriends(User.current_user.getName())
    return render_template("feed.html",user=User.current_user,posts=posts[::-1],comments=comments,recomm=recomm,friends=friends)

@views.route("/create-post",methods=["POST","GET"])
def createPost():
    if not check_login():
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        post_text  = request.form.get("post")
        post = Post(post_text,User.current_user.getName())
        flash("Post successfully aded","success")

    return render_template("create_post.html",user=User.current_user)


@views.route("/show-<user>",methods=["POST","GET"])
def showUser(user):
    if not check_login():
        return redirect(url_for("auth.login"))
    if request.method=="POST":
        comment_text = request.form.get("comment")
        value = request.form.get("hidden")
        value = value.split(',')
        username = value[0]
        post_id = value[1]
        comment = Comment(comment_text,username)
        Post.addComment(post_id,comment.getId())
    posts = Post.getAllPosts()
    comments = Comment.getComments() # dict type
    friends = Friendship.getFriends(user)
    return render_template("show_user.html",username=user,user=User.current_user,posts=posts[::-1],comments=comments,friends=friends)

@views.route("/show-friends/<username>")
def show_friends(username):
    return render_template("show_friends.html",username=username,user=User.current_user,friends=sorted(Friendship.getFriends(username),key=lambda x:x.lower()))


@views.route("/make-friends/<username1>/<username2>")
def make_friends(username1,username2):
    Friendship.makeFriendship(username1,username2)
    return redirect(url_for("views.showUser",user=username1))

@views.route("/add-like/<user_name>/<post_id>")
def add_like(user_name,post_id):
    Post.addLike(post_id,user_name)
    posts = Post.getAllPosts()
    return redirect(url_for("views.feed",user=User.current_user,posts=posts))

@views.route("/delete-like/<user_name>/<post_id>")
def delete_like(user_name,post_id):
    Post.deleteLike(post_id,user_name)
    posts = Post.getAllPosts()
    return redirect(url_for("views.feed",user=User.current_user,posts=posts))

@views.route("/delete-comment/<com_id>/<post_id>")
def delete_comment(com_id,post_id):
    Post.deleteComment(post_id,com_id)
    Comment.deleteComment(com_id)
    return redirect(url_for("views.feed"))

@views.route("/search",methods=["POST","GET"])
def search():
    if not check_login():
        return redirect(url_for("auth.login"))
    search_result = None
    if request.method == "POST":
        username = request.form.get("search")
        search_result = Search.search(username)
    return render_template("search.html",user=User.current_user,
    search=search_result)


@Socket.socket.on("send")
def handleMessage(msg):
    if msg["receiver"] != "None" and len(msg["text"]) > 0:
        Message.insertMessage(msg["sender"],msg)
        Message.insertMessage(msg["receiver"],msg)

@views.route("/chat/<username>",methods=["POST","GET"])
@views.route("/chat",methods=["POST","GET"])
def chat(username=None):
    if not check_login():
        return redirect(url_for("auth.login"))
    messages = []
    if username:
        msgs = Message.getMessageHistory(User.current_user.getName())
        messages = []
        for msg in msgs:
            if msg.receiver == username or msg.sender == username:
                messages.append(msg)
        
    friend = username
    return render_template("chat.html",user=User.current_user,friends=sorted(Friendship.getFriends(User.current_user.getName()),key=lambda x:x.lower()),friend = friend,messages=messages)