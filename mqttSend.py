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

broker          = 'mqtt-alpha.smart-iov.net'     #测试网
port            = 8801                             #端口
topic           = "SB2D2E00075"                   #发布主题

subTopic        = "U/JSON/B2D2E00075"              #终端主题

username        = 'test10'

client_id       = "app_test10"
mqttPassword    ="18cbd2b9800.aca5bc82c4ed053e9b6bed3a785e756a"
'''
client_id       = "app_test08"
mqttPassword    ="18cbd2b9800.82d7ea652dc12ebc4e61adda8763066c"
'''
# 定义一个回调函数
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    if rc == 0:
        print("Connect MQTT Server Success")

    elif rc == 4:
        print("User name or password wrong")

# 消息接收的回调函数
def on_message(client, userdata, msg):
    #print("Received message: " + str(msg.payload.decode()))
    payload = json.loads(msg.payload)
    print("Received message: " , payload)


# 发布回调函数
def on_publish(client, userdata, mid):
    print("Messaged send success")


def publish_message():
    # publish 5 messages to topic
    paylad = '5,3,1677235643,' + str(random.randint(1000, 3000)) + ',34383038,C7'
    client.publish(topic, paylad)
    print("publish msg: " + paylad)
    time.sleep(2)

    requset_car_status_paylad = '4,2,8'
    #请求车态数据
    client.publish(topic, requset_car_status_paylad)
    print("publish msg: " + requset_car_status_paylad)

def on_subscribe(client, userdata, mid, grated_qos, properties=None):
    print("订阅成功")


client = mqtt.Client(client_id)     #创建mqtt客户端
client.username_pw_set(username=username, password=mqttPassword)    #set Username & passwprd

client.on_connect = on_connect      # 将回调函数指派给客户端实例
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe

client.connect(broker, port, 60)    #连接MQTT服务器

client.subscribe(subTopic)
print("subscribe: " + subTopic)

time.sleep(2)
#publish_message()


# 循环处理网络流量和消息回调
client.loop_start()

