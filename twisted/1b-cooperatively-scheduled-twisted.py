import time
from twisted.internet import reactor, defer

start = time.time()


def tic():
    return 'at %1.1f seconds' % (time.time() - start)


@defer.inlineCallbacks
def sleep(n=0):
    d = defer.Deferred()
    reactor.callLater(n, d.callback, 0)
    yield d


@defer.inlineCallbacks
def gr1():
    # Busy waits for a second, but we don't want to stick around...
    print('gr1 started work: {}'.format(tic()))
    yield sleep(2)
    print('gr1 ended work: {}'.format(tic()))


@defer.inlineCallbacks
def gr2():
    # Busy waits for a second, but we don't want to stick around...
    print('gr2 started work: {}'.format(tic()))
    yield sleep(2)
    print('gr2 Ended work: {}'.format(tic()))


@defer.inlineCallbacks
def gr3():
    print("Lets do some stuff while the coroutines are blocked, {}".format(tic()))
    yield sleep(1)
    print("Done!")

deferred_list = defer.gatherResults(
    [gr1(), gr2(), gr3()])
deferred_list.addCallback(lambda _: reactor.stop())
reactor.run()
