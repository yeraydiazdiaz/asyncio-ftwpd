"""
Basic Twisted example with unit tests using twisted.trial.

The snippet below is a most basic Twisted example runnable in an interpreter:

```
from twisted.internet import task, reactor
d = task.deferLater(reactor, 0.1, lambda: print('foo'))  # creates and schedules a Deferred
d.addCallback(lambda x: reactor.stop())  # add a callback to stop when completed
reactor.run()  # run the event loop
```

Run this file using `trial` to execute Twisted built-in test runner.
"""

import asyncio

from twisted.internet import task, reactor
from twisted.internet.defer import Deferred, inlineCallbacks, ensureDeferred
from twisted.trial.unittest import TestCase

async def ticker(delay, to):
    for i in range(to):
        yield i
        await asyncio.sleep(delay)


async def run_():
    async for i in ticker(1, 10):
        print(i)


async def run():
    async for i in ticker(1, 10):
        print(i)


@inlineCallbacks
def inline_success():
    coro = run()
    print(coro)
    yield ensureDeferred(coro)
    print('Done inline')


d = task.deferLater(reactor, 0.1, inline_success)
d.addCallback(lambda x: reactor.stop())
reactor.run()
