from queue import Queue
from threading import Thread
from datetime import date
import sys
import csv
from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider('https://xdai-archive.blockscout.com'))
# w3 = Web3(Web3.HTTPProvider('https://xdai.poanetwork.dev'))
# w3 = Web3(Web3.WebsocketProvider('wss://xdai.poanetwork.dev/wss'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(w3.isConnected())

concurrent = 100

def doWork():
    while True:
        block, max_block = q.get()
        key, count = get_transactions(block, max_block)
        add_csv(key, count, block)
        q.task_done()

csv_data = {}
def add_csv(key, count, block):
    global csv_data
    if key == None or count == 0:
        return
    if key in csv_data:
        csv_data[key] += count
    else:
        csv_data[key] = count
    if block % 17280 == 0:
        print(csv_data)

def get_transactions(block: int, max_block: int):
    try:
        print(f'web3 {block}/{max_block}', end="\r")
        count = w3.eth.get_block_transaction_count(block)
        if count == 0:
            return None, None
        block_info = w3.eth.get_block(block)

        time = date.fromtimestamp(block_info.timestamp)
        key = f'{time.month}/{time.day}/{time.year}'
        print(f'web3 {block}/{max_block}', end="\r")
        return key, count
    except Exception as e:
        print("Error on block", block)
        print(e)
        return None, None



q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()

def get_all_transactions():
    max_block = w3.eth.get_block_number()
    try:
        for i in range(12000000, max_block):
            q.put(( i, max_block))
        q.join()
    except KeyboardInterrupt:
        sys.exit(1)

get_all_transactions()

with open('dict-xdai.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in csv_data.items():
            writer.writerow([key, value])