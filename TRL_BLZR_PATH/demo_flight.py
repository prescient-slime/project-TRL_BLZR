#!/usr/bin/env python3

import asyncio
from mavsdk import System

drone = System()

async def run():
    print("trying to connect to drone...")
    await drone.connect(system_address="serial:///dev/ttyAMA0:57600")

if __name__ == "__main__":
    asyncio.run(run())
