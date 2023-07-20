'''
topic: SBC66E100AC
paylad: 5,3,1677235643,1215,34383038,C7
1215每次要变

测试网: mqtt-alpha.smart-iov.net:8801
username: test10
client_id: app_test10
mqttPassword:18cbd2b9800.aca5bc82c4ed053e9b6bed3a785e756a

topic: SBC66E100AC
paylad: 4,2,15
请求车态数据

订阅 U/JSON/BC66E100AC

BC66E100AC
B2D2E00075
B4B2E0009E
'''

import paho.mqtt.client as mqtt
import random
import json
import time
import queue

#配置信息
sn              = 'B4B2E0009E'                                      #终端SN号
broker          = 'mqtt-alpha.smart-iov.net'                        #测试网
port            = 8801                                              #端口
topic           = 'S' + sn                                          #平台发布Topic
subTopic        = 'U/JSON/' + sn                                    #终端发布Topic
userName        = 'test08'                                          #测试平台用户名
client_id       = 'app_test08'                                      #client_id
mqttPassword    = '18cbd2b9800.82d7ea652dc12ebc4e61adda8763066c'    #测试平台密码

'''
userName        = 'test10'
client_id       = "app_test10"
mqttPassword    = "18cbd2b9800.aca5bc82c4ed053e9b6bed3a785e756a"
'''
INTERVAL_TIME   =   60
RUN_TIME        =   20

message_buff = queue.Queue()
start_time = 0

# 定义一个回调函数
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    if rc == 0:
        print("Connect MQTT Server Success")
        #订阅终端发布主题
        client.subscribe(subTopic)
    elif rc == 4:
        print("User name or password wrong")

# 订阅回调函数
def on_subscribe(client, userdata, mid, grated_qos, properties=None):
    print("subscribe: " + subTopic)

# 消息接收的回调函数
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    #print("Received Message: " , payload)
    try:
        #解析数据
        engine = payload['informations'][1]['value']['engine']
        collect_time = payload['informations'][1]['value']['collect_time']
        message_buff.put([engine, collect_time])

    except Exception as result:
        pass

    finally:
        if not message_buff.empty():
                print('engine,stamp: ', message_buff.get())
        #print("Received Message: " , message_buff.get())
'''
        global start_time
        send_time = time.time()
        elapsed_time = send_time - start_time
        print(f"Message sent to IV100 in {elapsed_time} seconds")
'''

# 发布消息回调函数
def on_publish(client, userdata, mid):
    print("Message Send To MQTT")


#获取车辆上报数据
def get_car_reporting_data():
    client.publish(topic, '4,2,15')     #车辆信息批量上报(0x0F)

#发送主题消息
def publish_message(des_Topic, cmd = 'C7'):
    '''
    publish messages to des_Topic
    @des_Topic: 发布主题
    @cmd:       命令,默认C7 鸣车
    '''
    paylad = '5,3,1677235643,' + str(random.randint(1000, 3000)) + ',34383038,' + cmd
    client.publish(des_Topic, paylad)

    send_time = time.time()
    print('stamp:', send_time, " publish msg: " + paylad)


def clinet_Init():
    client.username_pw_set(username=userName, password=mqttPassword)    #set Username & passwprd
    client.on_connect = on_connect      # 将回调函数指派给客户端实例
    client.on_message = on_message
    #client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.connect(broker, port, 60)    #连接MQTT服务器


def set_Test_Logic(interval_time, run_time):
    ''' 设置测试逻辑.
        interval_time:   间隔时间S   默认60 s.\n
        run_time:       运行时间S   默认20 s.\n
        record_file:  记录文件路径.
        '''
    global INTERVAL_TIME
    global RUN_TIME
    INTERVAL_TIME   = interval_time
    RUN_TIME        = run_time

def test_start():
    global RUN_TIME
    while RUN_TIME > 0:
        publish_message(topic, 'C18')
        time.sleep(1)
        RUN_TIME = RUN_TIME - 0.2

client = mqtt.Client(client_id)     #创建mqtt客户端

if __name__ == '__main__':
    clinet_Init()
    client.loop_start()
    set_Test_Logic(20, 3.0)
    publish_message(topic, 'C16')

    # 循环处理网络流量和消息回调
    #test_start()
    #while True:
        #pass
        # 记录开始发送消息的时间戳
        #start_time = time.time()
        #publish_message(topic, 'C6')

        #get_car_reporting_data()

        #time.sleep(0.5)
        #break

    client.loop_stop()

