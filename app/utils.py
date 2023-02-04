import asyncio
import time

from teslapy import Vehicle, VehicleError


class Utils:
    @staticmethod
    async def wake_up_vehicle_async(vehicle: Vehicle, timeout=60, interval=2, backoff=1.15):
        if not vehicle.available():
            # Send wake up command
            vehicle.api("WAKE_UP")
            start_time = time.time()

            while True:
                await asyncio.sleep(int(interval))
                if vehicle.available(0):
                    break

                if start_time + timeout - interval < time.time():
                    raise VehicleError(f"{vehicle['vin']} not woken up within ${timeout} seconds")

                interval *= backoff
