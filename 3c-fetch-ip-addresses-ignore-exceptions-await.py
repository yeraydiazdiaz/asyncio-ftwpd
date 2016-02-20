from collections import namedtuple
import time
import asyncio
import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'this-is-not-an-attr'),
    Service('borken', 'http://no-way-this-is-going-to-work.com/json', 'ip')
)


async def fetch_ip(service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    try:
        response = await aiohttp.request('GET', service.url)
    except:
        print('{} is unresponsive'.format(service.name))
    else:
        json_response = await response.json()
        ip = json_response[service.ip_attr]

        response.close()
        print('{} finished with result: {}, took: {:.2f} seconds'.format(
            service.name, ip, time.time() - start))


async def asynchronous():
    futures = [fetch_ip(service) for service in SERVICES]
    await asyncio.wait(futures)  # intentionally ignore results


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
