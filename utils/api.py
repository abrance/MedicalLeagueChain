import requests
import web3

session = requests.Session()


w3 = web3.Web3()


"""
暂时放这里 一些代码，陆续会整理
"""


def createJSONRPCRequestObject(_method, _params, _requestId):
    return {"jsonrpc": "2.0",
            "method": _method,
            "params": _params,  # must be an array [value1, value2, ..., valueN]
            "id": _requestId}, _requestId + 1


def postJSONRPCRequestObject(_HTTP_end_point, _jsonRPCRequestObject):
    _res = session.post(_HTTP_end_point,
                        json=_jsonRPCRequestObject,
                        headers={'Content-type': 'application/json'})

    return _res.json()
