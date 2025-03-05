from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import cv2
import base64
import time
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Initialize video capture (0 is the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")


def video_stream():
    while True:
        ret, frame = cap.read()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            if buffer is not None:
                frame_bytes = buffer.tobytes()
                frame_b64 = base64.b64encode(frame_bytes).decode('utf-8')
                socketio.emit('video_frame', {'data': frame_b64})
        time.sleep(0.03)


# Start video streaming in a separate thread
thread = threading.Thread(target=video_stream)
thread.daemon = True
thread.start()

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
