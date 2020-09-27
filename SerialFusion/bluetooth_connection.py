import asyncio
import constants

from bleak import BleakClient


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print(data.decode())


async def run(address):
    async with BleakClient(address) as client:
        await client.start_notify(constants.CHARACTERISTIC_UUID, notification_handler)
        await asyncio.sleep(2000)



if __name__ == "__main__":

    address = (
        constants.IMU_ADDRESS
    )
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(address))
