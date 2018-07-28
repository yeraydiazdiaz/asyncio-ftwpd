import trio

from tracer import Tracer


async def foo():
    print('Running in foo')
    await trio.sleep(0.1)
    print('Explicit context switch to foo again')


async def bar():
    print('Explicit context to bar')
    await trio.sleep(0.1)
    print('Implicit context switch back to bar')


async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(foo)
        nursery.start_soon(bar)

trio.run(main)
