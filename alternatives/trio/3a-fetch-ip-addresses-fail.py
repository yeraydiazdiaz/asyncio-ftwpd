from collections import namedtuple
import time
import trio
import asks

asks.init('trio')

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query'),
    Service('borken', 'http://no-way-this-is-going-to-work.com/json', 'ip')
)


async def fetch_ip(service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))
    try:
        response = await asks.get(service.url)
        json_response = response.json()
    except:
        print('{} is unresponsive'.format(service.name))
    else:
        ip = json_response[service.ip_attr]
        print('{} finished with result: {}, took: {:.2f} seconds'.format(
            service.name, ip, time.time() - start))


async def main():
    async with trio.open_nursery() as nursery:
        for service in SERVICES:
            """
            A slight subtlety here, Trio requires an async function to start
            a nursery, but start_soon is not asynchronous itself, it schedules
            the task to be ran and there's no way us to retrieve the result
            as we're used to with asyncio since Trio does not have the concept
            of Futures.

            Within this block however as the parent of the nursery
            """
            nursery.start_soon(fetch_ip, service)


trio.run(main)
