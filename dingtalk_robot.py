import hmac
import hashlib
import base64
import urllib.parse
from time import time
#rom time import sleep
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

def warning_bot(sn : str, time_str : str, command : str, ACC_status, status : str, type):

    if type == -1:
        #出现异常
        title = "暗锁监控出现" + status
        header = "异常提醒"
    else:
        #定时推送
        title = "监控定时推送:" + status
        header = "定时推送"
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title ,
            "text": f"""#### {header}\n  
SN: {sn}  
时间: {time_str}  
下发控制: **{command}**  
ACC状态: **{ACC_status}**  
状态: **{status}**"""
        }

    }
    # 机器人链接地址，发post请求 向钉钉机器人传递指令
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=cc640d4648207c18f37d23b8d52e67560e8b8e9817b2d0e7838634ca4f358f43'
    # 利用requests发送post请求
    req = requests.post(webhook_url+get_digest(), json=data, timeout=2)
if __name__ == '__main__':


    #测试
    #warning_bot(sn= '100001', time_str= '2023-07-22 14:52', command= '启动' ,status = '正常', ACC_status = 1, type=1)

    '''
    warning_enable_flag = 1     #可提醒标志
    status_push_flag    = 0     #状态推送标志
    
    i = 1
    status_push_time = 1
    issue = 1

    while True:

        print("sec: ",status_push_time)
        if (issue == 0):
            if(warning_enable_flag == 1):
                warning_bot(sn= '100001', time_str= '2023-07-22 14:52', command= '启动' ,status = '异常', ACC_status = 0, type=-1)
                warning_enable_flag = 0
                print("异常推送")
                print("关闭异常推送权限")
                issue = 1

        sleep(1)

        if(warning_enable_flag == 0):
            print("缓冲:", i, 's')
            if i == 4:                      #(run_time + interval_time)*4 s后允许继续发送警告
                i = 1
                warning_enable_flag = 1     #允许通知
                print("允许发送异常通知")
            else:
                i = i + 1

        
        if(status_push_time == 20):
            status_push_time = 1
            issue = 0    #产生异常
            print("产生异常")
        else:
            status_push_time = status_push_time + 1 #(run_time + interval_time)*36 s后允许推送状态
            '''
