import requests
import asyncio
import csv
from datetime import date, timedelta
from dateutil import parser
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


async def get_all_transactions():
    response = requests.get('https://explorer.roninchain.com/_next/data/agwuR1HgqJ1TmwK1-7hel/index.json')
    max_block = response.json()['pageProps']['latestBlocks']['total']
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        with requests.Session() as session:
            retries = Retry(total=10, status=10, backoff_factor=0.1)
            session.mount('https://', HTTPAdapter(max_retries=retries))
            loop = asyncio.get_event_loop()

            tasks = [
                loop.run_in_executor(
                    executor,
                    get_transactions,
                    *(session, i, max_block) # Allows us to pass in multiple arguments to `fetch`
                )
                for i in range(1, max_block)
            ]
            csv_data = {}
            for response in await asyncio.gather(*tasks):
                if response == None:
                    continue
                key, count = response
                if key in csv_data:
                    csv_data[key] += count
                else:
                    csv_data[key] = count

            return csv_data

def get_transactions(session, block: int, max_block: int):
    url = f'https://explorer.roninchain.com/_next/data/agwuR1HgqJ1TmwK1-7hel/block/{block}.json'
    with session.get(url) as response:
        if response.status_code != 200:
            print("FAILURE::{0}".format(url))
            print(response.status_code)
            print(response)
            return None
        block_data = response.json()
        time = date.fromtimestamp(block_data['pageProps']['block']['timestamp'])
        count = block_data['pageProps']['block']['transactions']
        key = f'{time.month}/{time.day}/{time.year}'
        print(f'{block}/{max_block}', end="\r")
        return key, count


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_all_transactions())
    csv_content = loop.run_until_complete(future)
    with open('dict-ronin.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in csv_content.items():
            writer.writerow([key, value])

main()
# print(get_transactions(20663))
# print(get_all_transactions())
# block_list = get_all_blocks()

# csv = {}

# for block in block_list:
#     time = block.verified_at
#     csv[f'{time.month}/{time.day}/{time.day}'] += block.


# print(len(block_list))