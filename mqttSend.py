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
import datetime
import os
import csv





#配置信息
sn              = 'B2D2E00075'                                      #终端SN号
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
# CSV文件路径
csv_file = 'test_data.csv'

start_time = 0
def on_connect(client, userdata, flags, rc):
    # 连接回调函数
    print("Connected with result code " + str(rc))
    if rc == 0:
        print("Connect MQTT Server Success")
        #订阅终端发布主题
        client.subscribe(subTopic)
    elif rc == 4:
        print("User name or password wrong")


def on_subscribe(client, userdata, mid, grated_qos, properties=None):
    # 订阅回调函数
    print("subscribe: " + subTopic)


def save_data_csv(data : list, csv_file):
    '''
        data: 数据列表
        csv_file: 文件路径'''
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def on_message(client, userdata, msg):
    # 消息接收的回调函数
    # 解析
    payload = json.loads(msg.payload)
    try:
        #提取数据
        #获取ACC状态
        engine = payload['informations'][1]['value']['engine']
        collect_time_stamp = payload['informations'][1]['value']['collect_time']

        #计算时间
        dt = datetime.datetime.fromtimestamp(collect_time_stamp)
        time = str(dt.time())

        if userdata == 1:
            command = '启动'
        elif userdata == 0:
            command = '关闭'

        if userdata == engine:
            result = '正常'
        else:
            result = '异常'

        data = [time, command, engine, result]
        print('[IV100] '+ time + " engine: ", engine, " result: ", result)
        save_data_csv(data, csv_file)

    except Exception as result:
        #print(result)
        pass
    #print('[IV100] '+ 'msg: ', payload)



def on_publish(client, userdata, mid):
    # 发布消息回调函数
    print("Message Send To MQTT")


#获取车辆上报数据
def get_car_reporting_data():
    client.publish(topic, '4,2,15')     #车辆信息批量上报(0x0F)
    send_time = datetime.datetime.now()
    print('[Client]' , send_time.strftime("%H:%M:%S") ,'Request Data')

def publish_message(des_Topic, cmd = 'C6'):
    #发送主题消息
    '''
    publish messages to des_Topic
    @des_Topic: 发布主题
    @cmd:       命令,默认C6 闪灯
    '''
    paylad = '5,3,1677235643,' + str(random.randint(1000, 3000)) + ',34383038,' + cmd
    client.publish(des_Topic, paylad)

    send_time = datetime.datetime.now()
    print('[Client]' , send_time.strftime("%H:%M:%S") , "publish cmd: " + paylad)


def clinet_Init():
    client.username_pw_set(username=userName, password=mqttPassword)    #set Username & passwprd
    client.on_connect = on_connect      # 将回调函数指派给客户端实例
    client.on_message = on_message
    #client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.connect(broker, port, 60)    #连接MQTT服务器



def test_start(run_time = 20, interval_time = 60, count = None):
    ''' 设置测试逻辑.
        interval_time:   间隔时间S   默认60 s.\n
        run_time:       运行时间S   默认20 s.\n
        count:          测试次数    默认一直测试\n
        record_file:  记录文件路径.
        '''

    # 判断文件是否存在
    if not os.path.exists(csv_file):
        # 创建CSV文件
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # 写入CSV文件的表头
            writer.writerow(["Time", "控制", "ACC_Status", "Result"])
        print("CSV文件已创建")
    else:
        print("CSV文件已存在")

    print("Test Start with----" + "运行时间: ", run_time, " 间隔时间: ", interval_time)
    #启动测试

    #采样时间
    if(run_time <= 10 or interval_time <= 10):
        run_sample_time =   2
        interval_time   =   2
    else:
        run_sample_time = run_time / 10
        interval_sample_time  = interval_time / 10

    while True:
        try:
            time_count = 0
            time.sleep(2)        #延时2s,确保处理完响应

            #下发启动命令（闪灯）
            client.user_data_set(1)
            publish_message(topic, 'C6')
            print("---------------------启动-----------------------------")

            time.sleep(200/1000)        #延时200ms,确保终端响应
            while time_count < run_time:
                time.sleep(run_sample_time)
                #获取车辆信息数据
                get_car_reporting_data()
                time_count = time_count + run_sample_time
                print("获取数据 ","第: ", time_count, "s")

            time_count = 0
            time.sleep(2)        #延时2s,确保处理完响应

            #间隔测试
            #下发断开命令（鸣车）
            client.user_data_set(0)
            publish_message(topic, 'C7')
            print("---------------------关闭-----------------------------")
            time.sleep(200/1000)        #延时200ms,确保终端响应
            while time_count < interval_time:
                time.sleep(interval_sample_time)
                #获取车辆信息数据
                get_car_reporting_data()
                time_count = time_count + interval_sample_time
                print("获取数据 ","第: ", time_count, "s")

        except Exception as result:
            print(result)


client = mqtt.Client(client_id)     #创建mqtt客户端

if __name__ == '__main__':
    clinet_Init()

    # 循环处理网络流量和消息回调
    client.loop_start()
    time.sleep(2)
    #开始测试
    test_start(run_time = 20,interval_time =300)

    client.loop_stop()

