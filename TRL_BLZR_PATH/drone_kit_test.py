from dronekit import connect, VehicleMode

print("connecting to drone")
drone = connect('/dev/ttyAMA0',baud=57600)
print("Last Heartbeat %s" % drone.last_heartbeat)
print("Is armable? %s" % drone.is_armable)
print("Arming...")
drone.armed = True

