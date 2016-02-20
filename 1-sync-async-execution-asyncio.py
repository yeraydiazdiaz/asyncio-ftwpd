import asyncio


@asyncio.coroutine
def foo():
    print('Running in foo')
    yield from asyncio.sleep(0)
    print('Explicit context switch to foo again')


@asyncio.coroutine
def bar():
    print('Explicit context to bar')
    yield from asyncio.sleep(0)
    print('Implicit context switch back to bar')


ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(foo()), ioloop.create_task(bar())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()
