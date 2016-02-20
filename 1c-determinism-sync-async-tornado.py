import random
import concurrent
from time import sleep
from tornado import ioloop
from tornado import gen

# ThreadPoolExecutor is only available in Python3
executor = concurrent.futures.ThreadPoolExecutor(8)


def task(pid):
    """Some non-deterministic task

    """
    sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


def task_async(pid):
    """Same task but non blocking.

    We could just use a coroutine here but I went for a quick test for Futures.
    Before finding that gevent 1.1a2 was compatible with Python3.
    """
    task_future = gen.Future()
    sleep_future = gen.sleep(random.randint(0, 2)*0.001)

    def callback(f):
        task_future.set_result(f.set_result)
        print('Task %s done' % pid)

    sleep_future.add_done_callback(callback)
    return task_future


def synchronous():
    for i in range(1, 10):
        task(i)


@gen.coroutine
def asynchronous():
    yield [executor.submit(task, i) for i in range(10)]


@gen.coroutine
def asynchronous_python2():
    yield [task_async(i) for i in range(10)]


print('Synchronous:')
synchronous()


print('Asynchronous:')
ioloop = ioloop.IOLoop.current()
ioloop.run_sync(asynchronous)

print('Asynchronous Python2-compatible:')
ioloop.run_sync(asynchronous_python2)
