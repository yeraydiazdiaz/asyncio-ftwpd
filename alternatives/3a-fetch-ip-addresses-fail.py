from collections import namedtuple
import time
import asyncio
import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query'),
    Service('borken', 'http://no-way-this-is-going-to-work.com/json', 'ip')
)


@asyncio.coroutine
def fetch_ip(service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    try:
        response = yield from aiohttp.request('GET', service.url)
    except:
        return '{} is unresponsive'.format(service.name)

    json_response = yield from response.json()
    ip = json_response[service.ip_attr]

    response.close()
    return '{} finished with result: {}, took: {:.2f} seconds'.format(
        service.name, ip, time.time() - start)


@asyncio.coroutine
def asynchronous():
    futures = [fetch_ip(service) for service in SERVICES]
    done, _ = yield from asyncio.wait(futures)

    for future in done:
        print(future.result())


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
