import time
import urllib.request
from twisted.internet import reactor, defer
import treq

URL = 'https://api.github.com/events'
MAX_CLIENTS = 3


async def fetch_async(pid):
    print('Fetch async process {} started'.format(pid))
    start = time.time()
    response = await treq.get(URL)
    # unfortunately Twisted's Agent which treq is base on does not expose
    # connection headers so we cannot get the Date header in the same way
    # https://github.com/twisted/treq/issues/56#issuecomment-36573795
    datetime = response.headers.getRawHeaders('Date', '<MISSING>')

    print('Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start))

    return datetime


async def asynchronous():
    start = time.time()
    tasks = [defer.ensureDeferred(
        fetch_async(i)) for i in range(1, MAX_CLIENTS + 1)]
    # in Twisted there is no as_completed, you can however add a callback to
    # each of the deferreds
    await defer.gatherResults(tasks)
    print("Process took: {:.2f} seconds".format(time.time() - start))

async def asynchronous():
    start = time.time()
    futures = [fetch_async(i) for i in range(1, MAX_CLIENTS + 1)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        print('{} {}'.format(">>" * (i + 1), result))

    print("Process took: {:.2f} seconds".format(time.time() - start))


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
