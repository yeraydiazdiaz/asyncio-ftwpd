from twisted.internet import reactor, defer

@defer.inlineCallbacks
def sleep(n=0):
    d = defer.Deferred()
    reactor.callLater(n, d.callback, 0)
    yield d

@defer.inlineCallbacks
def foo():
    print('Running in foo')
    yield sleep()
    print('Explicit context switch to foo again')


@defer.inlineCallbacks
def bar():
    print('Explicit context to bar')
    yield sleep()
    print('Implicit context switch back to bar')


foo_deferred = foo()
bar_deferred = bar()
deferred_list = defer.gatherResults([foo_deferred, bar_deferred])
deferred_list.addCallback(lambda _: reactor.stop())
reactor.run()
