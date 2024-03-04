from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

vehicle = connect("/dev/ttyAMA0", wait_ready=True, baud=57600)

vehicle.mode = VehicleMode("GUIDED")

vehicle.armed = True

vehicle.simple_takeoff(3)

while float(vehicle.location.global_relative_frame.alt) < (3 * 0.95):
    print(f"Altitude = {vehicle.location.global_relative_frame.alt}")
    if vehicle.location.global_relative_frame.alt == (3 * 0.95):
        print("Target altitude reached")
    time.sleep(1)

print("Landing")
vehicle.mode = VehicleMode("LAND")

vehicle.close()
