# pip install adafruit-circuitpython-pca9685
# pip install adafruit-circuitpython-motor


import time
import board
import busio
import adafruit_pca9685
from adafruit_motor import servo
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass
devices = i2c.scan()
print("Devices found: ", devices)
i2c.unlock()

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
    0: 0,
    1: 0,
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
    0: 0,
    1: 0,
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

RIGHT_LEGS_WALK = {
    9: 0,
    10:0,
    11:0
}

LEFT_LEGS_WALK = {
    9: 0,
    10:0,
    11:0
}


def set_servo_angle_slowly(servo_obj, target_angle):
    delay = 0.025
    step = 5

    try:
        current_angle = servo_obj.angle

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

def rightServos(move_list):
    for channel in range(16):
        try:
            target_angle = move_list.get(channel, 0)  # Default angle to 0 if not found
            if channel in move_list:
                set_servo_angle_slowly(right_servos[channel], target_angle)
                limb_name = RIGHT.get(channel, "unknown")
                print(f"Channel {channel} ({limb_name}) set to {target_angle}°")
            else:
                print(f"Channel {channel} has no defined standard position.")
        except ValueError:
            print(f"Channel {channel}: Could not set angle (may not be connected)")

def leftServos(move_list):
    for channel in range(16):
        try:
            target_angle = move_list.get(channel, 0)  # Default angle to 0 if not found
            if channel in move_list:
                set_servo_angle_slowly(left_servos[channel], target_angle)
                limb_name = LEFT.get(channel, "unknown")
                print(f"Channel {channel} ({limb_name}) set to {target_angle}°")
            else:
                print(f"Channel {channel} has no defined standard position.")
        except ValueError:
            print(f"Channel {channel}: Could not set angle (may not be connected)")

def walkLegs():
    rightServos(RIGHT_LEGS_WALK)
    time.sleep(0.25)
    rightServos(RIGHT_STANDARD_POSITION)
    time.sleep(0.25)
    leftServos(LEFT_LEGS_WALK)
    time.sleep(0.25)
    leftServos(LEFT_STANDARD_POSITION)




def main():
    moveServos(RIGHT_STANDARD_POSITION)
    #moveServos(LEFT_STANDARD_POSITION)
    


if __name__ == "__main__":
    main()
