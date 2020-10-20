"""
2020/10/20

说明
用于 部署
truffle 编译好的文件

使用方法
constants 中设置 路径等值
python3 deploy.py 执行即可

what
基于web3.py
使用 ipc，json_rpc方式进行接口调用

"""
import time

from utils.api import createJSONRPCRequestObject, postJSONRPCRequestObject, session, w3
from utils.log import logger
from constants import *


"""
test -- get net_version
"""
payload = {"jsonrpc": "2.0",
           "method": method,
           "params": params,
           "id": 1}
headers = {'Content-type': 'application/json'}
response = session.post(URL, json=payload, headers=headers)
logger.info('raw json response: {}'.format(response.json()))
logger.info('network id: {}'.format(response.json()['result']))
# create persistent HTTP connection


# compile your smart contract with truffle first
truffleFile = json.load(open(PATH_SC_TRUFFLE + '/build/contracts/Evidence.json'))
# truffleFile = json.load(open(PATH_SC_TRUFFLE + '/build/contracts/AdditionContract.json'))


abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# get your nonce
requestObject, requestId = \
    createJSONRPCRequestObject('eth_getTransactionCount', [user, 'latest'], requestId)
responseObject = postJSONRPCRequestObject(URL, requestObject)
myNonce = w3.toInt(hexstr=responseObject['result'])
logger.info('nonce of address {} is {}'.format(user, myNonce))

# create your transaction
# careful with gas price, gas price below the --gasprice option of
# Geth CLI will cause problems. I am running my node with --gasprice '1'
transaction_dict = {'from': user,
                    'to': '',  # empty address for deploying a new contract
                    'chainId': CHAINID,
                    'gasPrice': w3.toHex(20 * 1),
                    'gas': w3.toHex(2000000),  # rule of thumb / guess work
                    'nonce': myNonce,
                    'data': bytecode}  # no constrctor in my smart contract so bytecode is enough

# sign the transaction
signed_transaction_dict = w3.eth.account.signTransaction(transaction_dict, private_key)
params = [signed_transaction_dict.rawTransaction.hex()]

# send the transaction to your node
requestObject, requestId = createJSONRPCRequestObject('eth_sendRawTransaction', params, requestId)
responseObject = postJSONRPCRequestObject(URL, requestObject)
logger.info(responseObject)
transactionHash = responseObject['result']
logger.info('contract submission hash {}'.format(transactionHash))

# wait for the transaction to be mined and get the address of the new contract
while True:
    requestObject, requestId = createJSONRPCRequestObject('eth_getTransactionReceipt', [transactionHash], requestId)
    responseObject = postJSONRPCRequestObject(URL, requestObject)
    receipt = responseObject['result']
    if receipt is not None:
        if receipt['status'] == '0x1':
            contractAddress = receipt['contractAddress']
            logger.info('newly deployed contract at address {}'.format(contractAddress))
        else:
            logger.info(responseObject)
            raise ValueError('transacation status is "0x0", failed to deploy contract. Check gas, gasPrice first')
        break
    time.sleep(PERIOD / 10)
