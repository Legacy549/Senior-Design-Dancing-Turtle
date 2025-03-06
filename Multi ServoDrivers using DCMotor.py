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
    9: "hip_FB",
    10: "hip_OI",
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
    9: "hip_FB",
    10: "hip_OI",
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

def set_servo_angle_slowly(servo_obj, target_angle):
    delay = 0.025
    step = 5

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

def alternate_servo_movement(servo1, target1, servo2, target2):
    delay = 0.07
    step = 8
    
    current1 = servo1.angle if servo1.angle is not None else 0
    current2 = servo2.angle if servo2.angle is not None else 0
    
    step1 = step if target1 > current1 else -step
    step2 = step if target2 > current2 else -step
    
    while current1 != target1 or current2 != target2:
        if current1 != target1:
            next_angle1 = min(target1, current1 + step1) if step1 > 0 else max(target1, current1 + step1)
            servo1.angle = next_angle1
            current1 = next_angle1
            time.sleep(delay)
        
        if current2 != target2:
            next_angle2 = min(target2, current2 + step2) if step2 > 0 else max(target2, current2 + step2)
            servo2.angle = next_angle2
            current2 = next_angle2
            time.sleep(delay)

def walkLegs():
   #Legs--> 9 is FB & 11 is knee
   for x in range(3):
    alternate_servo_movement(right_servos[11], 90, right_servos[9], 90)
    alternate_servo_movement(right_servos[11], 0, right_servos[9], 0)
    alternate_servo_movement(left_servos[11], 90, left_servos[9], 90)
    alternate_servo_movement(left_servos[11], 0, left_servos[9], 0)

def lineDance():
    #two taps forward -> FB up and down
    alternate_servo_movement(right_servos[9], 55, right_servos[11, 10])
    alternate_servo_movement(right_servos[9], 45, right_servos[11, 0])
    alternate_servo_movement(right_servos[9], 55, right_servos[11, 10])
    alternate_servo_movement(right_servos[9], 45, right_servos[11, 0])
    alternate_servo_movement(right_servos[9], 0, right_servos[11, 0])
    #two taps back
    alternate_servo_movement(right_servos[9], 0, right_servos[11, 30])
    alternate_servo_movement(right_servos[9], 0, right_servos[11, 15])
    alternate_servo_movement(right_servos[9], 0, right_servos[11, 30])
    alternate_servo_movement(right_servos[9], 0, right_servos[11, 15])
    alternate_servo_movement(right_servos[9], 0, right_servos[11, 0])
    


        
def main():
    walkLegs()
    time.sleep(0.5)
    lineDance()
    rightServos(RIGHT_STANDARD_POSITION)
    leftServos(LEFT_STANDARD_POSITION)
    


if __name__ == "__main__":
    main()
