import time
import urllib.request
from tornado import ioloop
from tornado import gen
from tornado import httpclient

MAX_CLIENTS = 3
URL = 'https://api.github.com/events'


def fetch_sync(pid):
    print('Fetch sync process {} started'.format(pid))
    start = time.time()
    response = urllib.request.urlopen(URL)
    datetime = response.getheader('Date')

    print('Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start))
    return datetime


@gen.coroutine
def fetch_async(pid):
    print('Fetch async process {} started'.format(pid))
    start = time.time()
    http_client = httpclient.AsyncHTTPClient()
    response = yield http_client.fetch(URL)
    datetime = response.headers.get('Date')

    print('Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start))
    return datetime


def synchronous():
    start = time.time()
    for i in range(1, MAX_CLIENTS + 1):
        fetch_sync(i)
    print("Process took: {:.2f} seconds".format(time.time() - start))


@gen.coroutine
def asynchronous():
    start = time.time()
    yield [fetch_async(i) for i in range(1, MAX_CLIENTS + 1)]
    print("Process took: {:.2f} seconds".format(time.time() - start))


print('Synchronous:')
synchronous()

print('Asynchronous:')
ioloop = ioloop.IOLoop.current()
ioloop.run_sync(asynchronous)
