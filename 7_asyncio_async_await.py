import asyncio


# async now is equivalent of grandfathered @asyncio.coroutine before def
async def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        # this is equivalent of grandfathered yield from
        await asyncio.sleep(0.1)


async def print_time():
    count = 0
    while True:
        if not count % 3:
            print(f'{count} seconds have passed')

        count += 1
        await asyncio.sleep(1)


async def main():
    # this used to be .ensure_future()
    task1 = asyncio.create_task(print_nums())
    task2 = asyncio.create_task(print_time())

    await asyncio.gather(task2, task1)

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
    # all of the above is now this:
    asyncio.run(main())