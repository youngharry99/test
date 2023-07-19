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
'''

import paho.mqtt.client as mqtt
import random
import json
import time

sn              = 'BC66E100AC'                                      #终端SN号
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
    #print("Received message: " + str(msg.payload.decode()))
    payload = json.loads(msg.payload)
    print("Received Message: " , payload)


# 发布消息回调函数
def on_publish(client, userdata, mid):
    print("Message Send To MQTT")

#获取车辆上报数据
def get_car_reporting_data():
    client.publish(topic, '4,2,15')     #车辆信息批量上报(0x0F)
'''
def publish_message():
    # publish 5 messages to topic
    paylad = '5,3,1677235643,' + str(random.randint(1000, 3000)) + ',34383038,C7'
    client.publish(topic, paylad)
    print("publish msg: " + paylad)
    time.sleep(2)
    requset_car_status_paylad = '4,2,15'
    #请求车态数据
    client.publish(topic, requset_car_status_paylad)
    print("publish msg: " + requset_car_status_paylad)
'''
def clinet_Init():
    client.username_pw_set(username=userName, password=mqttPassword)    #set Username & passwprd
    client.on_connect = on_connect      # 将回调函数指派给客户端实例
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.connect(broker, port, 60)    #连接MQTT服务器

client = mqtt.Client(client_id)     #创建mqtt客户端

if __name__ == '__main__':
    #client = mqtt.Client(client_id)     #创建mqtt客户端
    clinet_Init()
    
    time.sleep(2)

    # 循环处理网络流量和消息回调
    client.loop_start()

    while True:
        get_car_reporting_data()
        time.sleep(2)

    client.loop_stop()

