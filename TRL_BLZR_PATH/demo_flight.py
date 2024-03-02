#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan

async def run():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyAMA0:57600")
    print("Waiting for drone to connect...\n")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    print_mission_progress_task = asyncio.ensure_future(print_mission_progress(drone))

    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(
        observe_is_in_air(drone, running_tasks)
    )

    mission_items = []
    mission_items.append(MissionItem())
    

if __name__ == "__main__":
    asyncio.run(run())
