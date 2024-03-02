#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)

print("Imports Successful")

async def run():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyAMA0:57600")


    #arm drone
    print("-- Arming")
    await drone.action.arm()


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
