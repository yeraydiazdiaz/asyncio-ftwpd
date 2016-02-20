import gevent.monkey
gevent.monkey.patch_socket()

import gevent
import urllib.request


def fetch(pid):
    response = urllib.request.urlopen(
        'http://jsonplaceholder.typicode.com/users')
    datetime = response.getheader('Date')

    print('Process %s: %s' % (pid, datetime))
    return datetime


def synchronous():
    for i in range(1, 10):
        fetch(i)


def asynchronous():
    threads = []
    for i in range(1, 10):
        threads.append(gevent.spawn(fetch, i))
    gevent.joinall(threads)


print('Synchronous:')
synchronous()

print('Asynchronous:')
asynchronous()
