from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
from pymavlink import mavutil
from shapely.geometry import Polygon, Point
from geopy.distance import distance
import numpy as np

# Define the polygon
polygon = []
with open("boundary_vertices.txt", "r") as f:
    for line in f:
        point = line.split(",")
        polygon.append((float(point[1]), float(point[0])))
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
        9,
    )
    cmds.add(takeoff_cmd)
