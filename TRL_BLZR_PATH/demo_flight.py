from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time
import math

import argparse

parser = argparse.ArgumentParser(description='Control Copter and send commands in GUIDED mode ')
parser.add_argument('--connect', help="Vehicle connection target string. If not specified, SITL automatically started and used.")
parser.add_argument('--baud_rate', help="Vehicle connection baud rate string. If not specified, none will be used.")
args = parser.parse_args()

connection_string = args.connect
baud_rate = args.baud_rate

sitl = None

if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

print('Connecting to vehicle on: %s' % connection_string)
if not baud_rate:
    vehicle = connect(connection_string, wait_ready=True)
else:
    vehicle = connect(connection_string, wait_ready=True, baud=baud_rate) #, baud=57600)

def arm_and_takeoff(target_altitude):
    print("pre-arm checks")
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialize...")
        time.sleep(1)
    print("arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)
    
    print("Takeoff")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= target_altitude*0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

#vehicle.airspeed = 1 #vehicle speed set to 1m/s


