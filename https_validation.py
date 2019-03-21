import asyncio
import aiohttp
from time import time
import argparse
import os
import sys

VALID_FILENAME = 'Valid'
INVALID_FILENAME = 'Unvalid'


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        dest='path',
        required=True,
        help='Path to urls file'
    )
    return parser.parse_args()


def get_url_list_from_file(filename):
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
                ssl=True,
                verify_ssl=True,
        ) as response:
            data = await response.read()
            
            write_result(url, VALID_FILENAME)

    except (aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.InvalidURL):

        write_result(url, INVALID_FILENAME)


async def main(url_list):
    tasks = []

    async with aiohttp.ClientSession() as session:
        for url in url_list:
            task = asyncio.ensure_future(fetch_content(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    args = parse_arguments()
    
    if not os.path.exists(args.path):
        sys.exit('File not found')
    
    url_list = get_url_list_from_file(args.path)

    t0 = time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url_list))
    loop.close()

    print('Elapsed time: {}'.format(time() - t0))
