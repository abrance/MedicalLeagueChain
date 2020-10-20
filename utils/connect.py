from constants import *
from utils.api import session
from utils.log import logger


"""
拟定此模块专门用于提供json_rpc 接口
"""


class HttpEthCon(object):
    """
    json_rpc 通信基类
    """
    def __init__(self):
        self.json_req = None
        self.req_id = 0
        self.url = URL

    def get_req_id(self):
        return self.req_id

    def init(self, _params, _method):
        self.req_id += 1
        ret = {"jsonrpc": "2.0", "method": _method, "params": _params}
        self.json_req = ret
        return ret

    def post(self):
        if self.json_req:
            res = session.post(self.url, json=self.json_req, headers=HEADER)
            json_res = res.json()
            logger.info(json_res)
            return json_res


class GetTrans(HttpEthCon):
    """
    获取交易信息
    """
    def __init__(self):
        super(GetTrans, self).__init__()

    def init(self, _params, _method='eth_getTransactionByHash'):
        super(GetTrans, self).init(_params, _method=_method)


class TestServe(HttpEthCon):
    """
    测试 json_rpc服务是否可用
    """
    def __init__(self):
        super(TestServe, self).__init__()

    def init(self, _params, _method='net_version'):
        super(TestServe, self).init(_params, _method=_method)
