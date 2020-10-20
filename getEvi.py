# -*- coding: utf-8 -*-

from utils.api import w3
from utils.verify import get_md5
from utils.log import logger
from utils.app import unlock
from constants import *

file_hash = get_md5('1111')
filename_hash = get_md5('a.txt')


truffleFile = json.load(open(PATH_SC_TRUFFLE + '/build/contracts/Evidence.json'))

abi = truffleFile['abi']
# 存证智能合约地址
_evi_address = w3.toChecksumAddress(evi_addr)
logger.info('evi_address: {}'.format(_evi_address))
evi_abi = abi
evidence = w3.eth.contract(
    address=_evi_address,
    abi=evi_abi,
)


class GetEvidence(object):
    def __init__(self, _evidence):
        self.evidence = _evidence

    def get_evidence(self, _filename_hash, _file_hash):
        evi_ret = self.evidence.functions.getEvidence(_filename_hash, _file_hash).call()
        # 解析evi_ret数据

        return evi_ret

    def save_evidence(self, _filename_hash, _file_hash, timestamp):
        ret = unlock(user, passwd)
        logger.info(ret)
        tx_hash = self.evidence.functions.saveEvidence(_filename_hash, _file_hash, timestamp).transact(
            {'from': user, 'gas': 900000, 'gasPrice': 10}
        )
        # 2020/10/20 gas -- gas_limit  这个值和gasPrice需要配好，应该要刚好比gasPrice*gasUse大一点
        # gasUse 一般最低为21000，暂时不知道规则，报错为 exceed gas_limit
        return tx_hash

    def run(self):
        failed, success, offset = 0, 0, 0

        t = int(time.time())
        byte_fn = filename_hash.encode('utf-8')
        byte_fh = file_hash.encode('utf-8')
        logger.info(byte_fn)
        logger.info(byte_fh)
        ret1 = self.save_evidence(byte_fn, byte_fh, t)
        tx_receipt = w3.eth.waitForTransactionReceipt(ret1)
        # 2020/10/20 一定需要这一步
        logger.info('tx_receipt: {}'.format(tx_receipt))

        logger.info(ret1)
        result = self.get_evidence(byte_fn, byte_fh)
        logger.info(result)
        assert isinstance(result, list)
        if result[0] == 0:
            success += 1
        else:
            failed += 1
        logger.info("success: {}, failed: {}".format(success, failed))


if __name__ == "__main__":
    get_evidence = GetEvidence(evidence)
    get_evidence.run()
