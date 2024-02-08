from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
from pymavlink import mavutil
from shapely.geometry import Polygon
import numpy as np

# Connect to the drone
vehicle = connect(
    "127.0.0.1:14550", wait_ready=True
)  # May need to tweak when hardware testing

# Define the polygons
polygon = []
with open("boundary_vertices.txt", "r") as f:
    for line in f:
        point = line.split(",")
        polygon.append(point[1], point[0])
    f.close()


# Function to create a MAVLink waypoint command
def create_waypoint(lat, lon, alt):
    return Command(
        0,
        0,
        0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        0,
        0,
        0,
        0,
        0,
        0,
        lat,
        lon,
        alt,
    )


# Function to create a survey path
def create_survey_path(polygon):
    cmds = vehicle.commands
    cmds.clear()

    # Takeoff command
    takeoff_cmd = Command(
        0,
        0,
        0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        10,
    )
    cmds.add(takeoff_cmd)

    # Convert the polygon to a Shapely Polygon object
    shapely_polygon = Polygon(polygon)

    # Generate a grid of waypoints within the polygon
    minx, miny, maxx, maxy = shapely_polygon.bounds
    x_coords = np.arange(minx, maxx, 30 / 111111)  # 30 feet in degrees
    y_coords = np.arange(miny, maxy, 30 / 111111)  # 30 feet in degrees
    waypoints = [
        (x, y)
        for x in x_coords
        for y in y_coords
        if shapely_polygon.contains(Point(x, y))
    ]

    # Waypoint commands
    for waypoint in waypoints:
        waypoint_cmd = create_waypoint(waypoint[0], waypoint[1], 10)
        cmds.add(waypoint_cmd)

    # RTL command
    rtl_cmd = Command(
        0,
        0,
        0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    cmds.add(rtl_cmd)

    cmds.upload()


# Create a survey path for each polygon
for polygon in polygons:
    create_survey_path(polygon)

    # Switch to AUTO mode and start the mission
    vehicle.mode = VehicleMode("AUTO")

    # Wait for the mission to complete
    while vehicle.mode.name == "AUTO" and vehicle.armed:
        print("Mission in progress...")
        time.sleep(1)

    print("Mission complete!")

# Close the connection
vehicle.close()
