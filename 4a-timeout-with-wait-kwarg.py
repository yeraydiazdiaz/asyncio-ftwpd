import time
import random
import asyncio
import aiohttp
import argparse
from collections import namedtuple
from concurrent.futures import FIRST_COMPLETED

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query'),
)

DEFAULT_TIMEOUT = 0.01


async def aiohttp_get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_ip(service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    await asyncio.sleep(random.randint(1, 3) * 0.1)
    try:
        json_response = await aiohttp_get_json(service.url)
    except:
        return '{} is unresponsive'.format(service.name)

    ip = json_response[service.ip_attr]

    print('{} finished with result: {}, took: {:.2f} seconds'.format(
        service.name, ip, time.time() - start))
    return ip


async def main(timeout):
    response = {
        "message": "Result from asynchronous.",
        "ip": "not available"
    }

    futures = [asyncio.create_task(fetch_ip(service)) for service in SERVICES]
    done, pending = await asyncio.wait(
        futures, timeout=timeout, return_when=FIRST_COMPLETED)

    for future in pending:
        future.cancel()

    for future in done:
        response["ip"] = future.result()

    print(response)


parser = argparse.ArgumentParser()
parser.add_argument(
    '-t', '--timeout',
    help='Timeout to use, defaults to {}'.format(DEFAULT_TIMEOUT),
    default=DEFAULT_TIMEOUT, type=float)
args = parser.parse_args()

print("Using a {} timeout".format(args.timeout))
asyncio.run(main(args.timeout))
