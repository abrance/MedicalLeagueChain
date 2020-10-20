from constants import URL, HEADER
from utils.api import session
from utils.connect import TestServe
from utils.log import logger


method = 'net_version'
params = []

payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
response = session.post(URL, json=payload, headers=HEADER)
logger.info('raw json response: {}'.format(response.json()))
logger.info('network id: {}'.format(response.json()['result']))


def connect():
    t = TestServe()
    ret = t.init(params)
    logger.info(ret)


if __name__ == '__main__':
    connect()
