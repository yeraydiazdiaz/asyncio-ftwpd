from collections import namedtuple
import time
import trio
from concurrent.futures import FIRST_COMPLETED
import asks

asks.init('trio')

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query')
)


async def fetch_ip(service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    response = await asks.get(service.url)
    ip = response.json()[service.ip_attr]

    return '{} finished with result: {}, took: {:.2f} seconds'.format(
        service.name, ip, time.time() - start)


async def main():
    """
    This example showcases `FIRST_COMPLETED` which is not available in trio
    however we can mimic its behaviour using a trio.Queue storing only one result
    from the first coroutine to finish, then cancelling the other tasks.
    """
    q = trio.Queue(1)

    async def jockey(coro, service):
        r = await coro(service)
        await q.put(r)

    async with trio.open_nursery() as nursery:
        for service in SERVICES:
            nursery.start_soon(jockey, fetch_ip, service)

        print(await q.get())
        nursery.cancel_scope.cancel()


trio.run(main)
