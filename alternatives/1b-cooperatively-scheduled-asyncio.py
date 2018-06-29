import time
import asyncio

start = time.time()


def tic():
    return 'at %1.1f seconds' % (time.time() - start)


@asyncio.coroutine
def gr1():
    # Busy waits for a second, but we don't want to stick around...
    print('gr1 started work: {}'.format(tic()))
    yield from asyncio.sleep(2)
    print('gr1 ended work: {}'.format(tic()))


@asyncio.coroutine
def gr2():
    # Busy waits for a second, but we don't want to stick around...
    print('gr2 started work: {}'.format(tic()))
    yield from asyncio.sleep(2)
    print('gr2 Ended work: {}'.format(tic()))


@asyncio.coroutine
def gr3():
    print("Lets do some stuff while the coroutines are blocked, {}".format(tic()))
    yield from asyncio.sleep(1)
    print("Done!")


ioloop = asyncio.get_event_loop()
tasks = [
    ioloop.create_task(gr1()),
    ioloop.create_task(gr2()),
    ioloop.create_task(gr3())
]
ioloop.run_until_complete(asyncio.wait(tasks))
ioloop.close()
