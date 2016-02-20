import random
from time import sleep
import asyncio


def task(pid):
    """Synchronous non-deterministic task.

    """
    sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


@asyncio.coroutine
def task_coro(pid):
    """Coroutine non-deterministic task

    """
    yield from asyncio.sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


def synchronous():
    for i in range(1, 10):
        task(i)


@asyncio.coroutine
def asynchronous():
    tasks = [asyncio.async(task_coro(i)) for i in range(1, 10)]
    yield from asyncio.wait(tasks)


print('Synchronous:')
synchronous()

ioloop = asyncio.get_event_loop()
print('Asynchronous:')
ioloop.run_until_complete(asynchronous())

ioloop.close()
