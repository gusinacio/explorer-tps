import requests
import asyncio
import csv
from dataclasses import dataclass
from datetime import date, timedelta
from dateutil import parser
from concurrent.futures import ThreadPoolExecutor

STEP = 100

@dataclass
class Block:
    block_number: int
    new_state_root: str
    block_size: int
    commit_tx_hash: str
    verify_tx_hash: str
    committed_at: date
    verified_at: date

    def __post_init__(self):
        self.committed_at = parser.parse(self.committed_at)
        self.verified_at = parser.parse(self.verified_at)

@dataclass
class Transaction:
    block_number: int
    created_at: date
    fail_reason: str
    op: dict
    success: bool
    tx_hash: str

    def __post_init__(self):
        self.created_at = parser.parse(self.created_at)

def convert_to_block(blockstr):
    return Block(**blockstr)

def convert_to_transaction(transactionstr):
    return Transaction(**transactionstr)

def get_all_blocks():
    response = requests.get('https://api.zksync.io/api/v0.1/status')
    max_block = response.json()['last_verified']
    max_block = max_block + (STEP - max_block % STEP)
    all_blocks = []
    print(f'MAX BLOCKS: {max_block}')
    for i in range(STEP, 1000, STEP):
        all_blocks.extend(get_blocks(i))
        print(f'{(len(all_blocks) / max_block)*100}%')
    return all_blocks

def get_blocks(max_block: int):
    url = f'https://api.zksync.io/api/v0.1/blocks?max_block={max_block}&limit={STEP}'

    response = requests.get(url)
    block_list = response.json()
    return list(map(convert_to_block, block_list))


async def get_all_transactions():
    response = requests.get('https://api.zksync.io/api/v0.1/status')
    max_block = response.json()['last_verified']
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()

            tasks = [
                loop.run_in_executor(
                    executor,
                    get_transactions,
                    *(session, i) # Allows us to pass in multiple arguments to `fetch`
                )
                for i in range(1, max_block)
            ]
            csv_data = {}
            for response in await asyncio.gather(*tasks):
                csv_data =  {k: csv_data.get(k, 0) + response.get(k, 0) for k in set(csv_data) | set(response)}

            # for i in range(1, 10):
            #     all_transactions.extend(get_transactions(session, i))
            #     print(f'{(i / max_block)*100}%')
            return csv_data

def get_transactions(session, block: int):
    url = f'https://api.zksync.io/api/v0.1/blocks/{block}/transactions'
    with session.get(url) as response:
        if response.status_code != 200:
            print("FAILURE::{0}".format(url))
        block_list = response.json()
        last_key = None
        csv_content = {}
        count = 0
        for transaction in block_list:
            time = parser.parse(transaction['created_at'])
            key = f'{time.month}/{time.day}/{time.year}'
            if last_key != key:
                csv_content[key] = count
                count = 0
                last_key = key
            count += 1
        csv_content[last_key] = count

        return csv_content


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_all_transactions())
    csv_content = loop.run_until_complete(future)
    # csv_content = {}
    # first_date = transaction_list[0].created_at
    # last_date = transaction_list[-1].created_at
    # current_date = first_date
    # while current_date < last_date:
    #     key = f'{current_date.month}/{current_date.day}/{current_date.year}'
    #     csv_content[key] = 0
    #     current_date += timedelta(days=1)
    # for transaction in transaction_list:
    #     time = transaction.created_at
    #     key = f'{time.month}/{time.day}/{time.year}'
    #     csv_content[key] += 1
        # if not csv[f'{time.month}/{time.day}/{time.day}']:
        #     csv[f'{time.month}/{time.day}/{time.day}'] = 0
    with open('dict.csv', 'w') as csv_file:  
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