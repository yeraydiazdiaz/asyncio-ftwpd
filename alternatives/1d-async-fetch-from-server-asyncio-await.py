import time
import urllib.request
import asyncio
import aiohttp

URL = 'https://api.github.com/events'
MAX_CLIENTS = 3


def fetch_sync(pid):
    print('Fetch sync process {} started'.format(pid))
    start = time.time()
    response = urllib.request.urlopen(URL)
    datetime = response.getheader('Date')

    print('Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start))

    return datetime


async def aiohttp_get(url):
    """Nothing to see here, carry on ..."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response


async def fetch_async(pid):
    print('Fetch async process {} started'.format(pid))
    start = time.time()
    response = await aiohttp_get(URL)
    datetime = response.headers.get('Date')

    print('Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start))

    response.close()
    return datetime


def synchronous():
    start = time.time()
    for i in range(1, MAX_CLIENTS + 1):
        fetch_sync(i)
    print("Process took: {:.2f} seconds".format(time.time() - start))


async def asynchronous():
    start = time.time()
    tasks = [asyncio.ensure_future(
        fetch_async(i)) for i in range(1, MAX_CLIENTS + 1)]
    await asyncio.wait(tasks)
    print("Process took: {:.2f} seconds".format(time.time() - start))


print('Synchronous:')
synchronous()

print('Asynchronous:')
ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
