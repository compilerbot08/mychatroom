from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'secret!'
socketio = SocketIO(app)

# Store users in a dictionary
users = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chatroom')
def chatroom():
    username = request.args.get('username')
    if not username:
        return redirect(url_for('home'))
    return render_template('chatroom.html', username=username)

@socketio.on('connect')
def handle_connect():
    emit('response', {'msg': 'A new user has joined the chatroom.'}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    emit('response', {'msg': 'A user has left the chatroom.'}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = data.get('username', 'Anonymous')
    message = data['msg']
    emit('response', {'msg': f'{username}: {message}'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
