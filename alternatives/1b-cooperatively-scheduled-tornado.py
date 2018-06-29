import time
from tornado import ioloop
from tornado import gen

start = time.time()


def tic():
    return 'at %1.1f seconds' % (time.time() - start)


@gen.coroutine
def gr1():
    # Busy waits for a second, but we don't want to stick around...
    print('Started Polling: %s' % tic())
    yield gen.sleep(2)
    print('Ended Polling: %s' % tic())


@gen.coroutine
def gr2():
    # Busy waits for a second, but we don't want to stick around...
    print('Started Polling: %s' % tic())
    yield gen.sleep(2)
    print('Ended Polling: %s' % tic())


@gen.coroutine
def gr3():
    print("Hey lets do some stuff while the coroutines poll, %s" % tic())
    yield gen.sleep(1)


@gen.coroutine
def main():
    yield [gr1(), gr2(), gr3()]

ioloop = ioloop.IOLoop.current()
ioloop.run_sync(main)
