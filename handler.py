
"""
调用模版，暂时放在这儿，会清理
"""


import time

from utils.api import createJSONRPCRequestObject, postJSONRPCRequestObject, w3
from constants import *
from utils.log import logger

requestObject, requestId = createJSONRPCRequestObject('eth_getTransactionCount', [user, 'latest'], requestId)
responseObject = postJSONRPCRequestObject(URL, requestObject)
logger.info(responseObject)
myNonce = w3.toInt(hexstr=responseObject['result'])
logger.info('nonce of address {} is {}'.format(user, myNonce))

# prepare the data field of the transaction
# function selector and argument encoding
# https://solidity.readthedocs.io/en/develop/abi-spec.html#function-selector-and-argument-encoding
value1, value2 = 10, 32  # random numbers here
function = 'add(uint256,uint256)'  # from smart contract
methodId = w3.sha3(text=function)[0:4].hex()
param1 = value1.to_bytes(32, byteorder='big').hex()
param2 = value2.to_bytes(32, byteorder='big').hex()
data = '0x' + methodId + param1 + param2
contractAddress = state_addr
transaction_dict = {'from': user,
                    'to': contractAddress,
                    'chainId': CHAINID,
                    'gasPrice': 1,
                    # careful with gas price, gas price below the threshold defined in the node
                    # config will cause all sorts of issues (tx not bieng broadcasted for example)
                    'gas': 2000000,  # rule of thumb / guess work
                    'nonce': myNonce,
                    'data': data}

# sign the transaction
signed_transaction_dict = w3.eth.account.signTransaction(transaction_dict, private_key)
params = [signed_transaction_dict.rawTransaction.hex()]

# send the transacton to your node
logger.info('executing {} with value {},{}'.format(function, value1, value2))
requestObject, requestId = createJSONRPCRequestObject('eth_sendRawTransaction', params, requestId)
responseObject = postJSONRPCRequestObject(URL, requestObject)
transactionHash = responseObject['result']
logger.info('transaction hash {}'.format(transactionHash))

# wait for the transaction to be mined
while True:
    requestObject, requestId = createJSONRPCRequestObject('eth_getTransactionReceipt', [transactionHash], requestId)
    responseObject = postJSONRPCRequestObject(URL, requestObject)
    receipt = responseObject['result']
    if receipt is not None:
        if receipt['status'] == '0x1':
            logger.info('transaction successfully mined')
        else:
            logger.info(responseObject)
            raise ValueError('transacation status is "0x0", failed to deploy contract. Check gas, gasPrice first')
        break
    time.sleep(PERIOD / 10)
