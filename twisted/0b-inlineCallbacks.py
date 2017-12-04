"""
A Twisted example using inlineCallbacks.

"""

from twisted.internet import reactor, defer
import treq

@defer.inlineCallbacks
def fetch(url='https://google.com'):
    resp = yield treq.get(url)
    print(resp.code)
    reactor.stop()

d = fetch()
reactor.run()
