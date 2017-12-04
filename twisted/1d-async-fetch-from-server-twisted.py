import time
import urllib.request
from twisted.internet import reactor, defer
import treq
# Note: treq uses cryptography for TLS, if you encounter errors on TLS
# related to OpenSSL check the cryptography installation docs
# https://cryptography.io/en/latest/installation/


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
    response = await treq.get(URL)
    # unfortunately Twisted's Agent which treq is base on does not expose
    # connection headers so we cannot get the Date header in the same way
    # https://github.com/twisted/treq/issues/56#issuecomment-36573795
    datetime = response.headers.getRawHeaders('Date', '<MISSING>')

    print('Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start))

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
