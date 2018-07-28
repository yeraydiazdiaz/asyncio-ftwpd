import random
from time import sleep
import trio


def task(pid):
    """Synchronous non-deterministic task."""
    sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


async def task_coro(pid):
    """Coroutine non-deterministic task"""
    await trio.sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


def synchronous():
    for i in range(1, 10):
        task(i)


async def asynchronous():
    async with trio.open_nursery() as nursery:
        for i in range(1, 10):
            nursery.start_soon(task_coro, i)


print('Synchronous:')
synchronous()

print('Asynchronous:')
trio.run(asynchronous)
