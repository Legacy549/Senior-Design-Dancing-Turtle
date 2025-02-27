from adafruit_servokit import ServoKit
import time
kit = ServoKit(channels=16)
# PWM 'pip install adafruit-circuitpython-servokit'

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

def position_standardzero():
    for channel in range(16):
        time.sleep()
        try:
            angle = RIGHT_STANDARD_POSITION.get(channel, 90)  # Default angle to 90 if not found
            if channel in RIGHT_STANDARD_POSITION:
                kit.servo[channel].angle = angle
                limb_name = RIGHT.get(channel, "unknown")
                print(f"Channel {channel} ({limb_name}) set to {angle}°")
            else:
                print(f"Channel {channel} has no defined standard position.")
        except ValueError:
            print(f"Channel {channel}: Could not set angle (may not be connected)")

def pistols_firing():

    print("Pistols Firing")

def main():
    print("Setting all servos to standard positions...")
    moveServos(RIGHT_STANDARD_POSITION)
    #position_standardzero()
    print("Done.")

if __name__ == "__main__":
    main()
