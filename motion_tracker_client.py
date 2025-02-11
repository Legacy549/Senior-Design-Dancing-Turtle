import socket
from adafruit_servokit import ServoKit

# Initialize PCA9685 with 16 channels
kit = ServoKit(channels=16)

# Servo mapping order based on expected data format
servo_order = [
    "Left Shoulder XY", "Left Shoulder YZ",
    "Right Shoulder XY", "Right Shoulder YZ", "Left Elbow", "Right Elbow",
    "Left Hip XY", "Left Hip YZ",
    "Right Hip XY", "Right Hip YZ","Left Knee", "Right Knee"
]

# Map servo names to actual channel numbers
servo_map = {
    "Left Shoulder XY": 0, "Left Shoulder YZ": 1, "Left Elbow": 2,
    "Right Shoulder XY": 3, "Right Shoulder YZ": 4, "Right Elbow": 5,
    "Left Hip XY": 12, "Left Hip YZ": 13, "Left Knee": 14,
    "Right Hip XY": 9, "Right Hip YZ": 10, "Right Knee": 11
}

def set_servo_angle(servo_id, angle):
    """ Move servo to the specified angle if within range. """
    if 0 <= angle <= 180:
        kit.servo[servo_id].angle = angle
        print(f"Servo {servo_id} set to {angle}°")
    else:
        print(f"Angle {angle} out of range for Servo {servo_id}")

def parse_skeleton_data(data):
    """ Extracts only the numerical angle values and maps them to servos. """
    try:
        # Split the data and remove non-numeric tokens
        tokens = data.split()
        angles = []

        for token in tokens:
            try:
                angles.append(float(token))
            except ValueError:
                continue  # Skip non-numeric tokens like "Skeleton ID: 1"

        # Ensure the correct number of angles are received
        if len(angles) != len(servo_order):
            print(f"Warning: Expected {len(servo_order)} angles, got {len(angles)}")
            return {}

        return {servo_order[i]: angles[i] for i in range(len(angles))}
    except ValueError:
        print("Error: Invalid angle data received.")
        return {}

def start_server():
    """ Starts TCP server to receive skeleton angles and control servos. """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 1234))
    server_socket.listen(5)

    print("Server listening on port 1234...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        data = conn.recv(1024).decode("utf-8").strip()
        if not data:
            continue

        print("Received Skeleton Angles:", data)

        parsed_joint_angles = parse_skeleton_data(data)
        if not parsed_joint_angles:
            print("No valid joint angles parsed. Skipping servo updates.")
            continue

        # Set servo positions
        for joint, angle in parsed_joint_angles.items():
            servo_id = servo_map.get(joint)
            if servo_id is not None:
                print(f"Setting {joint} (Servo {servo_id}) to {angle}°")
                set_servo_angle(servo_id, angle)

if __name__ == "__main__":
    start_server()
