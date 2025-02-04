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
pca1 = adafruit_pca9685.PCA9685(i2c, address=0x40)  # First Servo Driver
pca2 = adafruit_pca9685.PCA9685(i2c, address=0x41)  # Second Servo Driver

# Set PWM frequency for both PCA9685 boards
pca1.frequency = 50
pca2.frequency = 50

# Create servo objects for each channel
right_servos = {i: servo.Servo(pca1.channels[i]) for i in range(16)}
left_servos = {i: servo.Servo(pca2.channels[i]) for i in range(16)}

# Servo Positions for Right Hand
RIGHT_STANDARD_POSITION = {
    0: 102,
    1: 110,
    2: 100,
    3: 100,
    4: 90,
    5: 90,
    6: 90,
    7: 90,
    8: 90
}

RIGHT_PISTOLS_FIRING = {
    0: 180,
    1: 200,
    2: 70,
    3: 86,
    4: 45,
    5: 180,
    6: 0,
    7: 0,
    8: 0
}

# Servo Positions for Left Hand
LEFT_STANDARD_POSITION = {
    0: 80,
    1: 95,
    2: 110,
    3: 90,
    4: 75,
    5: 100,
    6: 85,
    7: 95,
    8: 80
}


def set_servo_angle_slowly(servo_obj, target_angle):
    """
    Moves a servo gradually to the target angle.
    """
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


def position_standardzero():
    """Moves the RIGHT servos (PCA9685-1) and LEFT servos (PCA9685-2) to their standard positions."""
    for channel, target_angle in RIGHT_STANDARD_POSITION.items():
        set_servo_angle_slowly(right_servos[channel], target_angle)

    for channel, target_angle in LEFT_STANDARD_POSITION.items():
        set_servo_angle_slowly(left_servos[channel], target_angle)

    print("Position Zero (Standard) set.")


def pistols_firing():
    """Moves the RIGHT servos to the PISTOLS FIRING position."""
    for channel, target_angle in RIGHT_PISTOLS_FIRING.items():
        set_servo_angle_slowly(right_servos[channel], target_angle)

    print("Pistols Firing pose set.")


def main():
    position_standardzero()
    pistols_firing()


if __name__ == "__main__":
    main()
