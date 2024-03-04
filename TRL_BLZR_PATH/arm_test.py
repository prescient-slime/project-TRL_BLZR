#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)

print("Imports Successful")

async def run():
    print("Trying to connect to drone...")
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyAMA0")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break
    #arm drone
    print("-- Arming")
    await drone.action.arm()


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
