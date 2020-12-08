import json

from constants import user
from utils.api import w3
from utils.log import logger, log_path
import datetime


"""
此模块提供 web3 ipc接口
"""


class EthInit(object):
    def __init__(self):
        self.log = {}

    def commit(self, method, param, ret):
        t = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.log.__setitem__(method, [t, param, ret])
        logger.info(ret)

    def __del__(self):
        t = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        with open('{}/{}.info'.format(log_path, t), 'a+') as f:
            f.write(json.dumps(self.log, indent=4))

    def is_address(self, param):
        ret = w3.isAddress(param)
        self.commit('is_address', param, ret)
        return ret

    def get_balance(self, param):
        account = param
        ret = w3.eth.getBalance(account)
        self.commit('get_balance', param, ret)
        return ret

    def keccak(self, param):
        # 代替 sha 方法
        # >> > Web3.keccak(0x747874)
        # >> > Web3.keccak(b'\x74\x78\x74')
        # >> > Web3.keccak(hexstr='0x747874')
        # >> > Web3.keccak(hexstr='747874')
        # >> > Web3.keccak(text='txt')
        if type(param) is dict:
            ret = w3.keccak(**param)
        else:
            ret = w3.keccak(param)
        self.commit('keccak', param, ret)
        return ret

    def unlock(self, account, passphrase):
        param = (account, passphrase)
        ret = w3.geth.personal.unlock_account(account, passphrase)
        self.commit('unlock', param, ret)
        return ret

    @staticmethod
    def get_private_key(key_store_file_path, passphrase):
        # 2020/12/8 获取私钥
        with open(key_store_file_path, "r") as file:
            encrypted_key = file.read()
            p_key = w3.eth.account.decrypt(encrypted_key, passphrase)
            import binascii
            p_key = str(binascii.b2a_hex(p_key))
            return p_key


if __name__ == '__main__':
    a = EthInit()
    # a.is_address('0x2cc7fc9f579fd5fed62633548b2ca11bd029f779')
    # a.get_balance(user)
    # a.keccak()
    del a
