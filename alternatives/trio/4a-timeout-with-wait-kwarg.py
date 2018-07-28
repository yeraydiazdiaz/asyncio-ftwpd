import time
import random
import trio
import asks
import argparse
from collections import namedtuple
from concurrent.futures import FIRST_COMPLETED

asks.init('trio')

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query'),
)

DEFAULT_TIMEOUT = 0.01


async def fetch_ip(service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    await trio.sleep(random.randint(1, 3) * 0.1)
    print('Done sleeping...')
    try:
        response = await asks.get(service.url)
        json_response = response.json()
    except Exception as e:
        print('Got exception', e)
        return '{} is unresponsive'.format(service.name)
    else:
        ip = json_response[service.ip_attr]
        print('{} finished with result: {}, took: {:.2f} seconds'.format(
            service.name, ip, time.time() - start))
        return ip


async def main(timeout):
    response = {
        "message": "Result from asynchronous.",
        "ip": "not available"
    }
    q = trio.Queue(1)

    async def jockey(coro, service, timeout):
        with trio.move_on_after(timeout) as cs:
            await q.put(await coro(service))
        await q.put(None)

    async with trio.open_nursery() as nursery:
        for service in SERVICES:
            nursery.start_soon(jockey, fetch_ip, service, timeout)

        r = await q.get()
        if r is not None:
            response["ip"] = r
        nursery.cancel_scope.cancel()

    print(response)


parser = argparse.ArgumentParser()
parser.add_argument(
    '-t', '--timeout',
    help='Timeout to use, defaults to {}'.format(DEFAULT_TIMEOUT),
    default=DEFAULT_TIMEOUT, type=float)
args = parser.parse_args()

print("Using a {} timeout".format(args.timeout))
trio.run(main, args.timeout)
