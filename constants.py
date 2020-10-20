import json

requestId = 0  # is automatically incremented at each request

URL = 'http://localhost:8545'  # url of my geth node
PATH_GENESIS = '/data/gethdata/genesis.json'
PATH_SC_TRUFFLE = '/data/gethdata/contracts'  # smart contract path
# extracting data from the genesis file
genesisFile = json.load(open(PATH_GENESIS))
CHAINID = genesisFile['config']['chainId']
PERIOD = genesisFile['config']['clique']['period']
GASLIMIT = int(genesisFile['gasLimit'], 0)

# 从metamask 地址是账户 中导出 私钥
user = '0xCcDAb94Dd44693BAd4451A4b720d2C2fc0C965Ec'
private_key = '6aebff48fe70e79113c7d83623a01b412a05329d50cd6aa19e34da53832d6bdf'
passwd = 'abrance'

state_addr = '0x9c5cb4db1baa559cbbac01f21cbf02f5c02496cc9a5db94a1b14028acd02db18'
evi_addr = '0x4e80df42150cbefe50a706b045e8394c5a75bb65'
evi_hash = '0x4966a8dc2f0dbd514c95c29fceac946bb71f18f8724e3ae1aefe89d69ff42c29'

HEADER = {'Content-type': 'application/json'}
