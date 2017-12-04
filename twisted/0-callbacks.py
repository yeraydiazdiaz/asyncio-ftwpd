"""
This is the most basic Twisted example. Raw callback style.

"""

from twisted.internet import task, reactor
import treq

def callback(resp):
    print(resp.code)
    reactor.stop()  # this idiom is common, there's no run_until_complete

# invoking a function that returns a Deferred schedules it
# this is different in asyncio where you need to schedule the task
d = treq.get(url='https://google.com')
d.addCallback(callback)  # callbacks *must* have a result arg
d.addErrback(lambda failure: print(failure))  # same with errbacks
reactor.run()
