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

from twisted.internet import task, reactor
from twisted.internet.defer import Deferred, inlineCallbacks
from twisted.trial.unittest import TestCase

def success():
    print('Done')
    return 42

def fail():
    raise Exception('BOOM!')


@inlineCallbacks
def inline_success():
    yield task.deferLater(reactor, 0.1, success)
    print('Done inline')


class DemoTest(TestCase):
    """Run with `trial <this_file>`"""
    def setUp(self):
        self.clock = task.Clock()

    def test_success_manual(self):
        d = Deferred()
        d.addCallback(lambda x: print('done'))
        d.callback(None)

    def test_success(self):
        return task.deferLater(reactor, 0.1, success)

    def test_success_clock(self):
        d = task.deferLater(self.clock, 0.1, success)
        self.clock.advance(1)
        self.successResultOf(d)

    def test_success_inline(self):
        return inline_success()

    def test_fail(self):
        d = task.deferLater(reactor, 0.1, fail)
        return self.assertFailure(d, Exception)

    def test_fail_clock(self):
        d = task.deferLater(self.clock, 0.1, fail)
        self.clock.advance(1)
        self.failureResultOf(d).trap(Exception)
