from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import os

# path to html files
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
            # to admin_dash if correct
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid password, please try again.'
    return render_template('login.html')


@app.route('/interactive')
def interactive():
    # client3 if click interactive
    return render_template('client3.html')


@app.route('/admin_dash')
def admin_dashboard():
    if not session.get('logged_in'):
        # start at login page
        return redirect(url_for('login'))
    # to admin_dash if correct
    return render_template('admin_dash.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

# handle buttons


@socketio.on('button_press')
def handle_button_press(data):
    button_name = data['button']
    print(f"Button pressed: {button_name}")
    # Button action


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
