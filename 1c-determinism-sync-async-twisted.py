import random
from time import sleep
from twisted.internet import reactor, defer


@defer.inlineCallbacks
def async_sleep(n=0):
    d = defer.Deferred()
    reactor.callLater(n, d.callback, 0)
    yield d


def task(pid):
    """Synchronous non-deterministic task.

    """
    sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


async def task_coro(pid):
    """Coroutine non-deterministic task

    """
    await async_sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


def synchronous():
    for i in range(1, 10):
        task(i)


async def asynchronous():
    tasks = [defer.ensureDeferred(task_coro(i)) for i in range(1, 10)]
    await defer.gatherResults(tasks)


print('Synchronous:')
synchronous()


print('Asynchronous:')
d = defer.ensureDeferred(asynchronous())
d.addCallback(lambda _: reactor.stop())
d.addErrback(lambda result: print(result))
reactor.run()
