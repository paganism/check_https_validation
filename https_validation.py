import asyncio
import aiohttp
from time import time

VALID_FILENAME = 'valid'
INVALID_FILENAME = 'invalid'


def file_read(filename):
    with open(filename, 'r') as file:
        urls_list = file.read().split('\n')
        return urls_list


def write_result(data, name_pattern):
    with open(name_pattern, 'a') as file:
        file.write(data + '\n')


async def fetch_content(url, session):
    try:
        async with session.get(
                url,
                allow_redirects=False,
                verify_ssl=True
        ) as response:
            data = await response.read()
            
            write_result(url, VALID_FILENAME)

    except (aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.InvalidURL):

        write_result(url, INVALID_FILENAME)


async def main2(url_list):
    tasks = []

    async with aiohttp.ClientSession() as session:
        for url in url_list:
            task = asyncio.ensure_future(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    url_list = file_read('hosts.txt')
    t0 = time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main2(url_list))
    loop.close()
    print(time() - t0)
