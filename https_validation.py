import asyncio
import aiohttp
from time import time
import argparse
import os
import sys


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--valid',
        dest='valid',
        required=True,
        help='Path valid urls file'
    )

    parser.add_argument(
        '--invalid',
        dest='invalid',
        required=True,
        help='Path to invalid urls file'
    )

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
        return set(urls_list)


def write_result(data, name_pattern):
    with open(name_pattern, 'a') as file:
        file.write('\n'.join(data))


async def fetch_content(url, session):

    try:
        async with session.get(
                url,
                allow_redirects=False,
                ssl=True,
                verify_ssl=True,
        ) as response:
            data = await response.read()

        return {'valid': url}

    except (aiohttp.client_exceptions.ClientConnectorError,
            aiohttp.client_exceptions.InvalidURL):

        return {'invalid': url}


async def main(url_list):
    tasks = []

    async with aiohttp.ClientSession() as session:
        for url in url_list:
            task = asyncio.ensure_future(fetch_content(url, session))
            tasks.append(task)

        sites_statistics = await asyncio.gather(*tasks)
        return sites_statistics

        # Here is the same but shorter
        # sites_statistics = await asyncio.gather(*[fetch_content(url, session) for url in url_list])
        # return sites_statistics


if __name__ == '__main__':
    args = parse_arguments()

    if not any([os.path.exists(args.path),
                os.path.exists(args.valid),
                os.path.exists(args.invalid)]
               ):
        sys.exit('File not found')

    url_list = get_url_list_from_file(args.path)

    t0 = time()
    loop = asyncio.get_event_loop()
    statistics = loop.run_until_complete(main(url_list))

    valid_data_to_write = []
    invalid_data_to_write = []

    for dic in statistics:
        for key, value in dic.items():
            if key == 'invalid':
                invalid_data_to_write.append(value)
            else:
                valid_data_to_write.append(value)
    try:
        write_result(valid_data_to_write, args.valid)
        write_result(invalid_data_to_write, args.invalid)
    except Exception as e:
        print('Can not write file {}'.format(e))
    loop.close()

    print('Elapsed time: {}'.format(time() - t0))
