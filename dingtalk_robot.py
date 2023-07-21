import hmac
import hashlib
import base64
import urllib.parse
from time import time
import requests
'''
钉钉机器人数字签名计算
'''
def get_digest():
    # 取毫秒级别时间戳，round(x, n) 取x小数点后n位的结果，默认取整
    timestamp = str(round(time() * 1000))
    secret = 'SECe7fab3c74169aff7ba7d70faf7d5d5cbee9830f56b79b5ba5b0a902807aa389f'
    secret_enc = secret.encode('utf-8')  # utf-8编码
    string_to_sign = '{}\n{}'.format(timestamp, secret)  # 字符串格式化拼接
    string_to_sign_enc = string_to_sign.encode('utf-8')  # utf-8编码
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()  # HmacSHA256算法计算签名
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))  # Base64编码后进行urlEncode
    #  返回时间戳和计算好的编码拼接字符串，后面直接拼接到Webhook即可
    return f"&timestamp={timestamp}&sign={sign}"
# 简单发送markdown消息

def warning_bot(time_str : str, status : str):
    text = """### 测试监控提醒\n@时间:""" + time_str + """ \n状态: **""" + status + """**\n"""
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "暗锁测试监控" + status ,
            "text": text
        }
    }
    # 机器人链接地址，发post请求 向钉钉机器人传递指令
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=cc640d4648207c18f37d23b8d52e67560e8b8e9817b2d0e7838634ca4f358f43'
    # 利用requests发送post请求
    req = requests.post(webhook_url+get_digest(), json=data)
if __name__ == '__main__':
    warning_bot('17:27','异常')
