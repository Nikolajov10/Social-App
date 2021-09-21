from website import create_app
from flask_socketio import socketio

if __name__ == "__main__":
    app,socket = create_app()
    socket.run(app,debug=True)