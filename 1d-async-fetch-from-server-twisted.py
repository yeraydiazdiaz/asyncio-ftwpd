import time
import urllib.request
from twisted.internet import reactor, defer
from twisted.web.client import Agent


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


async def fetch_async(pid):
    print('Fetch async process {} started'.format(pid))
    start = time.time()
    agent = Agent(reactor)
    # method, url, headers, body
    response = await agent.request(b'GET', URL.encode(), None, None)
    datetime = response.headers.headers.getRawHeaders('Date')

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
    tasks = [defer.ensureDeferred(
        fetch_async(i)) for i in range(1, MAX_CLIENTS + 1)]
    await defer.gatherResults(tasks)
    print("Process took: {:.2f} seconds".format(time.time() - start))


print('Synchronous:')
synchronous()

print('Asynchronous:')
d = defer.ensureDeferred(asynchronous())
d.addCallback(lambda _: reactor.stop())
d.addErrback(lambda failure: print(failure))
reactor.run()
