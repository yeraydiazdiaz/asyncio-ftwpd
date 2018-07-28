import random
import concurrent
from time import sleep
import asyncio

executor = concurrent.futures.ThreadPoolExecutor(8)


def task(pid):
    """Some non-deterministic task

    """
    sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


@asyncio.coroutine
def task_coro(pid):
    """Some non-deterministic task

    """
    yield from asyncio.sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


def synchronous():
    for i in range(1, 10):
        task(i)


@asyncio.coroutine
def asynchronous_threads():
    # asyncio.ensure_future is named asyncio.async in Python < 3.4.4
    tasks = [
        asyncio.ensure_future(ioloop.run_in_executor(executor, task, i))
        for i in range(1, 10)
    ]
    yield from asyncio.wait(tasks)


@asyncio.coroutine
def asynchronous_coro():
    tasks = [asyncio.ensure_future(task_coro(i)) for i in range(1, 10)]
    yield from asyncio.wait(tasks)


print('Synchronous:')
synchronous()

ioloop = asyncio.get_event_loop()

print('Asynchronous threads:')
ioloop.run_until_complete(asynchronous_threads())

print('Asynchronous using coroutines:')
ioloop.run_until_complete(asynchronous_coro())

ioloop.close()
