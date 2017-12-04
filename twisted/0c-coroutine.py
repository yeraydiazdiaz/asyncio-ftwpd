"""
A Twisted example using coroutines.

"""

from twisted.internet import reactor, defer
import treq

async def fetch(url='https://google.com'):
    resp = await treq.get(url)
    print(resp.code)

# in order to use coroutines you *must* use ensureDeferred which will
# produce a Deferred from the coroutine object
# which is similar to what you'd do in asyncio
d = defer.ensureDeferred(fetch())
# still, you need to add callbacks manually
d.addCallback(lambda _: reactor.stop())
d.addErrback(lambda failure: print(failure))
reactor.run()
