import asyncio
import time


def sleep():
    time.sleep(3)
    print("init sleep")

    async def forever():
        while True:
            print(123)
            await asyncio.sleep(5)
    return forever()


async def main():
    await sleep()

asyncio.get_event_loop().run_until_complete(main())