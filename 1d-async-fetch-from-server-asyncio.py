import time
import urllib.request
import asyncio
import aiohttp

URL = 'https://api.github.com/events'
MAX_CLIENTS = 10


def fetch_sync(pid):
    print('Fetch sync process {} started'.format(pid))
    start = time.time()
    response = urllib.request.urlopen(URL)
    datetime = response.getheader('Date')

    print('Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start))

    return datetime


@asyncio.coroutine
def fetch_async(pid):
    print('Fetch async process {} started'.format(pid))
    start = time.time()
    response = yield from aiohttp.request('GET', URL)
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


@asyncio.coroutine
def asynchronous():
    start = time.time()
    tasks = [asyncio.ensure_future(
        fetch_async(i)) for i in range(1, MAX_CLIENTS + 1)]
    yield from asyncio.wait(tasks)
    print("Process took: {:.2f} seconds".format(time.time() - start))


print('Synchronous:')
synchronous()

print('Asynchronous:')
ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
