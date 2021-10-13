from web3 import Web3
from web3.middleware import geth_poa_middleware


w3 = Web3(Web3.HTTPProvider('https://proxy.roninchain.com/free-gas-rpc'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(w3.isConnected())
print(w3.eth.get_block_transaction_count(5319455))
print(w3.eth.get_block(5319455).transactions)