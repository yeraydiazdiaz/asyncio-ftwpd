import time
import random
import trio
import asks

asks.init('trio')

URL = 'https://api.github.com/events'
MAX_CLIENTS = 3


async def fetch_async(pid):
    start = time.time()
    sleepy_time = random.randint(2, 5)
    print('Fetch async process {} started, sleeping for {} seconds'.format(
        pid, sleepy_time))

    await trio.sleep(sleepy_time)

    response = await asks.get(URL)
    datetime = response.headers.get('Date')

    return 'Process {}: {}, took: {:.2f} seconds'.format(
        pid, datetime, time.time() - start)


async def main():
    """
    This example showcases `as_completed` which is not available in trio
    however we can mimic its behaviour using a trio.Queue storing the results
    of each coroutine. Then reading indefinitely from it until no more tasks
    are scheduled.
    """
    start = time.time()
    q = trio.Queue(MAX_CLIENTS)

    async def jockey(coro, i):
        r = await coro(i)
        await q.put(r)

    async with trio.open_nursery() as nursery:
        """
        Note important aspect of Trio, this parent block is itself a task.
        It may not have any code after the `start_soon` calls, which means
        the parent task won't do any work and simply wait for child tasks.
        But if it does include a checkpoint (the await q.get() in this case)
        the code will run like any other task interleaving with the child ones.
        """
        for i in range(1, MAX_CLIENTS + 1):
            nursery.start_soon(jockey, fetch_async, i)

        count = 0
        while True:
            print('* Parent: Checking for results on queue')
            r = await q.get()
            print('{} {}'.format(">>" * (count + 1), r))
            count += 1
            if not nursery.child_tasks:
                break

    print("Process took: {:.2f} seconds".format(time.time() - start))


trio.run(main)
