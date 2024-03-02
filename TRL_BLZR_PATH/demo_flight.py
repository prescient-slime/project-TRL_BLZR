#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)

print("Imports Successful")

async def run():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyAMA0")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    print_mission_progress_task = asyncio.ensure_future(
        print_mission_progress(drone))

    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(
        observe_is_in_air(drone, running_tasks))

    #waypoint array
    mission_items = []
    mission_items.append(MissionItem(34.98102529395546,
                                     -101.91514572067254,
                                     9,
                                     5,
                                     False,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float(5.0),
                                     float('nan'),
                                     float(2),
                                     float('nan'),
                                     float('nan'),
                                     0))
    #assemble waypoint array into MissionPlan object
    mission_plan = MissionPlan(mission_items)

    #Return to launch point after flying to waypoint
    await drone.mission.set_return_to_launch_after_mission(True)

    #Upload mission to drone
    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan)

    #Receive drone telemetry
    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break
    
    #arm drone
    print("-- Arming")
    await drone.action.arm()

    #begin drone mission from mission_plan
    print("-- Starting mission")
    await drone.mission.start_mission()
    
    #wait for drone to stop
    await termination_task


async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")


async def observe_is_in_air(drone, running_tasks):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())

