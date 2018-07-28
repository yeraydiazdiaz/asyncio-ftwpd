from collections import namedtuple
import time
import trio
import asks

asks.init('trio')

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
        response = await asks.get(service.url)
        json_response = response.json()
    except:
        print('{} is unresponsive'.format(service.name))
    else:
        ip = json_response[service.ip_attr]
        print('{} finished with result: {}, took: {:.2f} seconds'.format(
            service.name, ip, time.time() - start))


async def main():
    """
    Another subtlety, exceptions in Trio bubble up to the parent, and are
    raised *by the nursery* on exiting the context manager. This example would
    not work if the `try..except` was only wrapping the `start_soon`.
    """
    try:
        async with trio.open_nursery() as nursery:
            for service in SERVICES:
                nursery.start_soon(fetch_ip, service)
    except Exception as e:
        print('Unexpected error {}'.format(e))


trio.run(main)
