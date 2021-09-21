from .search import Search
from flask import Flask
from .database import DB
from .mongoDB import MongoDb
from .loadUsers import UserLoader
from flask_socketio import SocketIO
from .socket import Socket

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "#7y321t418"

    Socket.socket = SocketIO(app)

    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")


    DB.createDatabase()
    MongoDb.initDB()

    Search.searchInit()
    UserLoader.loader = UserLoader(Search.tree)
    UserLoader.loader.start()
    return app,Socket.socket
