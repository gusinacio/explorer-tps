from queue import Queue
from threading import Thread
import requests
from datetime import date
import sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import csv

s = requests.Session()
retries = Retry(total=5, status=5, backoff_factor=0.1, status_forcelist=[404, 500])
s.mount('https://', HTTPAdapter(max_retries=retries))
concurrent = 85

def doWork():
    while True:
        block, max_block = q.get()
        key, count = get_transactions(block, max_block)
        add_csv(key, count)
        q.task_done()

csv_data = {}
def add_csv(key, count):
    global csv_data
    if key == None or count == 0:
        return
    if key in csv_data:
        csv_data[key] += count
    else:
        csv_data[key] = count
    print(csv_data)

def get_transactions(block: int, max_block: int):
    url = f'https://explorer.roninchain.com/_next/data/agwuR1HgqJ1TmwK1-7hel/block/{block}.json'
    with s.get(url) as response:
        if response.status_code != 200:
            print("FAILURE::{0}".format(url))
            print(response.status_code)
            print(response)
            return None, None
        block_data = response.json()
        time = date.fromtimestamp(block_data['pageProps']['block']['timestamp'])
        count = block_data['pageProps']['block']['transactions']
        key = f'{time.month}/{time.day}/{time.year}'
        print(f'{block}/{max_block}', end="\r")
        return key, count


q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()

def get_all_transactions():
    response = requests.get('https://explorer.roninchain.com/_next/data/agwuR1HgqJ1TmwK1-7hel/index.json')
    max_block = response.json()['pageProps']['latestBlocks']['total']
    try:
        for i in range(1, 10000):
            q.put(( i, max_block))
        q.join()
    except KeyboardInterrupt:
        sys.exit(1)

get_all_transactions()

with open('dict-ronin.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in csv_data.items():
            writer.writerow([key, value])