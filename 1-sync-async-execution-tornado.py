from tornado import gen
from tornado import ioloop


@gen.coroutine
def foo():
    print('Running in foo')
    yield gen.sleep(0)
    print('Explicit context switch to foo again')


@gen.coroutine
def bar():
    print('Explicit context to bar')
    yield gen.sleep(0)
    print('Implicit context switch back to bar')


@gen.coroutine
def main():
    yield [foo(), bar()]


ioloop = ioloop.IOLoop.current()
ioloop.run_sync(main)
