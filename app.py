from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import os

# Specify the path to the directory where your HTML files are now located
# '.' is the current directory
app = Flask(__name__, template_folder=os.path.abspath('.'))

app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

PASSWORD = 'turtle'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Invalid password, please try again.'

    return render_template('login.html')


@app.route('/dashboard')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('client.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

# New SocketIO handler for button press events


@socketio.on('button_press')
def handle_button_press(data):
    button_name = data['button']
    print(f"Button pressed: {button_name}")
    # You can perform specific actions depending on the button pressed
    # For example, you could trigger specific functionality here


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
