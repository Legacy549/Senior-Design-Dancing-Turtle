# pip install adafruit-circuitpython-pca9685
# pip install adafruit-circuitpython-motor


import time
import board
import busio
import adafruit_pca9685
from adafruit_motor import servo

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize PCA9685 boards
pca1 = adafruit_pca9685.PCA9685(i2c, address=0x40)  # Left Servo Driver
pca2 = adafruit_pca9685.PCA9685(i2c, address=0x41)  # Right Servo Driver

# Set PWM frequency for both PCA9685 boards
pca1.frequency = 50
pca2.frequency = 50

# Create servo objects for each channel
right_servos = {i: servo.Servo(pca1.channels[i]) for i in range(16)}
left_servos = {i: servo.Servo(pca2.channels[i]) for i in range(16)}

# Servo Dictionary
RIGHT = {
    0: "shoulder_FB",
    1: "shoulder_OI",
    2: "elbow",
    3: "wrist",
    4: "thumb",
    5: "pointer",
    6: "middle",
    7: "ring",
    8: "little",
    9: "hip_OI",
    10: "hip_FB",
    11: "knee"
}

LEFT = {
    0: "shoulder_FB",
    1: "shoulder_OI",
    2: "elbow",
    3: "wrist",
    4: "thumb",
    5: "pointer",
    6: "middle",
    7: "ring",
    8: "little",
     9: "hip_OI",
    10: "hip_FB",
    11: "knee"
}

RIGHT_STANDARD_POSITION = {
    0: 180,
    1: 180,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10:0,
    11:0
}

LEFT_STANDARD_POSITION = {
    0: 180,
    1: 180,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10:0,
    11:0
}


def set_servo_angle_slowly(servo_obj, target_angle):
    delay = 0.07
    step = 8

    try:
        current_angle = servo_obj.angle
        if current_angle is None:  # If no previous angle, start from 0
            current_angle = 0

        # Determine the direction of movement
        step = step if target_angle > current_angle else -step

        # Gradually move the servo to the target angle
        for angle in range(int(current_angle), int(target_angle), step):
            servo_obj.angle = angle
            time.sleep(delay)

        # Ensure the final position is set
        servo_obj.angle = target_angle
    except Exception as e:
        print(f"Error moving servo: {e}")


def moveServos(move_list):
    for channel in range(16):
        time.sleep(0.5)
        try:
            angle = move_list.get(channel, 90)  # Default angle to 90 if not found
            if channel in move_list:
                kit.servo[channel].angle = angle
                limb_name = RIGHT.get(channel, "unknown")
                print(f"Channel {channel} ({limb_name}) set to {angle}°")
            else:
                print(f"Channel {channel} has no defined standard position.")
        except ValueError:
            print(f"Channel {channel}: Could not set angle (may not be connected)")
    

def pistols_firing():
    """Moves the RIGHT servos to the PISTOLS FIRING position."""
    for channel, target_angle in RIGHT_PISTOLS_FIRING.items():
        set_servo_angle_slowly(right_servos[channel], target_angle)

    print("Pistols Firing pose set.")


def main():
    moveServos(RIGHT_STANDARD_POSITION)
    


if __name__ == "__main__":
    main()
