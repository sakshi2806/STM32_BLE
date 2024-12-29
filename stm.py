import asyncio
from bleak import BleakScanner, BleakClient

def on_data_received(sender: int, data: bytearray):
    """Callback function for receiving data."""
    print(f"Data received from {sender}: {data.decode('utf-8', errors='ignore')}")

async def scan_for_device(retries=3, interval=5):
    """Scan for the STM32 device with a retry mechanism."""
    for attempt in range(retries):
        print(f"Scanning for BLE devices... (Attempt {attempt + 1}/{retries})")
        devices = await BleakScanner.discover()

        stm32_device = next(
            (device for device in devices if device.name and "stm32" in device.name.lower()), None
        )

        if stm32_device:
            print(f"Found STM32 device: {stm32_device.name} ({stm32_device.address})")
            return stm32_device

        print(f"No STM32 device found. Retrying in {interval} seconds...")
        await asyncio.sleep(interval)

    print("Failed to find STM32 device after retries.")
    return None

async def main():
    stm32_device = await scan_for_device()

    if not stm32_device:
        return

    print(f"Connecting to {stm32_device.name} ({stm32_device.address})...")

    try:
        async with BleakClient(stm32_device.address) as client:
            if client.is_connected:
                print(f"Connected to {stm32_device.name} ({stm32_device.address})")

                for service in client.services:
                    print(f"Service: {service.uuid}")
                    for char in service.characteristics:
                        print(f"  Characteristic: {char.uuid}, Properties: {char.properties}")

                        if "notify" in char.properties:
                            print(f"Subscribing to notifications on {char.uuid}")
                            await client.start_notify(char.uuid, on_data_received)

                print("Listening for data. Press Ctrl+C to exit.")
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    print("Exiting...")
                finally:
                    for char in client.services.characteristics:
                        if "notify" in char.properties:
                            await client.stop_notify(char.uuid)

            else:
                print("Failed to connect to the device.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
