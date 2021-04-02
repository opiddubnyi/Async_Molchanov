import requests
from time import time


def get_file(url):
    r = requests.get(url)
    return r


def write_file(response):
    filename = response.url.split('/')[-1]

    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    t0 = time()
    url = 'https://loremflickr.com/320/240'

    for i in range(10):
        write_file(get_file((url)))

    print(time() - t0)


# if __name__ == '__main__':
#     main()

###################

import asyncio
import aiohttp
from asyncio import WindowsSelectorEventLoopPolicy
from asyncio import SelectorEventLoop


def write_image(data):
    filename = f'file-{(int(time()) * 1000)}.jpeg'
    with open(filename, 'wb') as file:
        file.write(data)


async def fetch_content(url, session):
    async with session.get(url) as response:
        data = await response.read()
        write_image(data)


async def main2():
    url = 'https://loremflickr.com/320/240'
    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            # creating a task to add to the queue
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time()
    # asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    asyncio.set_event_loop(SelectorEventLoop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main2())

    asyncio.run(main2())
    print(time() - t0)
