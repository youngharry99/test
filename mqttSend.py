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
import dingtalk_robot as ding
import logging
#配置信息
sn              = 'B2D2E00075'                                      #终端SN号
broker          = 'mqtt-alpha.smart-iov.net'                        #测试网
port            = 8801                                              #端口
topic           = 'S' + sn                                          #平台发布Topic
subTopic        = 'U/JSON/' + sn                                    #终端发布Topic
comfirTopic     = 'C/JSON/' + sn                                    #终端确认Topic
'''
userName        = 'test08'                                          #测试平台用户名
client_id       = 'app_test08'                                      #client_id
mqttPassword    = '18cbd2b9800.82d7ea652dc12ebc4e61adda8763066c'    #测试平台密码
'''

userName        = 'test10'
client_id       = "app_test10"
mqttPassword    = "18cbd2b9800.aca5bc82c4ed053e9b6bed3a785e756a"


# CSV文件路径,
current_time = datetime.datetime.now()
timestamp = current_time.strftime("%Y-%m-%dT%H_%M_%S")
csv_file = f"test_data_{timestamp}.csv"

#日志配置
logging.basicConfig(filename='text.log',filemode='a',level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s:%(message)s",
                    datefmt="%Y-%M-%d %H:%M:%S")
#warning_enable_flag = 1     #可提醒标志
#status_push_flag    = 0     #状态推送标志

def on_connect(client, userdata, flags, rc):
    # 连接回调函数
    print("Connected with result code " + str(rc))
    if rc == 0:
        print("Connect MQTT Server Success")
        #订阅终端发布主题
        client.subscribe(subTopic)
        client.subscribe(comfirTopic)
    elif rc == 4:
        print("User name or password wrong")


def on_subscribe(client, userdata, mid, grated_qos, properties=None):
    # 订阅回调函数
    print("subscribe success!")


def save_data_csv(data : list, csv_file):
    '''
        data: 数据列表
        csv_file: 文件路径'''
    with open(csv_file, 'a', newline='', encoding= "utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

flag = 0


def on_comfir_message(client, userdata, msg):
    #终端确认信息处理
    #存储终端确认信息日志信息
    logging.info('[IV100]' + str(msg.payload))

def on_message(client, userdata, msg):
    # 消息接收的回调函数
    # 解析
    #global warning_enable_flag
    #global status_push_flag
    global flag
    payload = json.loads(msg.payload)
    #print('[IV100] '+ 'msg: ', payload)

    try:
        #提取数据
        #获取ACC状态
        engine = payload['informations'][1]['value']['engine']
        collect_time_stamp = payload['informations'][1]['value']['collect_time']    #获取时间戳
        #计算时间
        dt = datetime.datetime.fromtimestamp(collect_time_stamp)
        date_time_str = dt.strftime("%Y-%m-%d %H:%M:%S")

        if userdata == 1:
            command = '启动'
        elif userdata == 0:
            command = '关闭'

        if userdata == engine:
            result = '正常'
            flag = 0
        else:
            result = '异常'

        '''
        #定时推送消息
        if (status_push_flag == 1):
            ding.warning_bot(sn= sn, time_str=date_time_str, command= command, ACC_status=engine, status=result, type= 1)
            status_push_flag = 0
            print("已推送状态信息到钉钉")
        '''

        data = [date_time_str, command, engine, result]
        save_data_csv(data, csv_file)   #存储数据到文件中
        rec_time = datetime.datetime.now()
        print(rec_time.strftime("%H:%M:%S") + '[IV100] '+ date_time_str + " engine: ", engine, " result: ", result)
        #print('[IV100] '+ 'msg: ', payload)
        if userdata != engine:
            flag = flag + 1
            #if(warning_enable_flag == 1):
            #warning_enable_flag = 0

            #钉钉推送
            if flag == 1:
                ding.warning_bot(sn= sn, time_str= date_time_str, command= command ,ACC_status=engine, status = result, type=-1)
                print("Exiting the program...")
                client.loop_stop()          #停止后台线程监听
                client.disconnect()         #与mqtt断开连接
                os._exit(0)                 #线程中退出整个进程

    except Exception as e:
        #print(e)
        pass


'''
def on_publish(client, userdata, mid):
    # 发布消息回调函数
    print(userdata,mid)
'''

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
    result = client.publish(des_Topic, paylad, qos=1)
    status = result[0]
    send_time = datetime.datetime.now()
    if status == 0:
        print('[Client]' , send_time.strftime("%H:%M:%S") , "publish cmd: " + paylad)
    else:
        print('[Client] Send Message Failed' , send_time.strftime("%H:%M:%S") , "publish cmd: " + paylad)


def clinet_Init():
    client.username_pw_set(username=userName, password=mqttPassword)    #set Username & passwprd
    client.on_connect = on_connect                                      #将回调函数指派给客户端实例
    client.message_callback_add(comfirTopic, on_comfir_message)         #终端确认的消息回调函数
    client.on_message = on_message                                      #终端发布的消息回调函数
    #client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.connect(broker, port, 60)    #连接MQTT服务器

def test_start(run_time = 20, interval_time = 60, count = None):
    ''' 设置测试逻辑.
        interval_time:   间隔时间S   默认60 s.\n
        run_time:       运行时间S   默认20 s.\n
        count:          测试次数    默认一直测试\n
        '''
    #global warning_enable_flag
    #i = 1
    #global status_push_flag
    #status_push_time = 1

    # 判断文件是否存在
    if not os.path.exists(csv_file):
        # 创建CSV文件
        with open(csv_file, 'w', newline='',encoding="utf-8") as file:
            writer = csv.writer(file)
            # 写入CSV文件的表头
            writer.writerow(["Time", "下发命令", "ACC_Status", "Result"])
        print("CSV文件已创建")
    else:
        print("CSV文件已存在")

    print("Test Start with----" + "运行时间: ", run_time, " 间隔时间: ", interval_time)
    #启动测试
    run_sample_time = 2
    interval_sample_time = 10


    while True:
        try:

            time_count = 0
            #下发启动命令（闪灯）：1
            client.user_data_set(1)
            publish_message(topic, 'C6')
            print("---------------------启动-----------------------------")

            while time_count < run_time:
                time.sleep(run_sample_time)
                #获取车辆信息数据
                get_car_reporting_data()
                time_count = time_count + run_sample_time
                print("获取数据 ","第: ", time_count, "s")

            time.sleep(2)        #延时2s,确保处理完响应

            time_count = 0
            #间隔测试
            #下发断开命令（鸣车）：0
            client.user_data_set(0)
            publish_message(topic, 'C7')
            print("---------------------关闭-----------------------------")

            while time_count < interval_time:
                time.sleep(interval_sample_time)
                #获取车辆信息数据
                get_car_reporting_data()
                time_count = time_count + interval_sample_time
                print("获取数据 ","第: ", time_count, "s")

            time.sleep(2)        #延时2s,确保处理完响应

        except Exception as result:
            print(result)

        '''
        if(warning_enable_flag == 0):
            if i == 4:                      #(run_time + interval_time)*4 s后允许继续发送警告
                i = 1
                warning_enable_flag = 1     #允许通知
            else:
                i = i + 1


        if(status_push_time == 36):         #(run_time + interval_time)*36 s后允许自动推送状态
            status_push_time = 1
            status_push_flag = 1    #开启推送
        else:
            status_push_time = status_push_time + 1
        '''

client = mqtt.Client(client_id)     #创建mqtt客户端

if __name__ == '__main__':
    clinet_Init()

    # 创建线程循环处理网络流量和消息回调
    client.loop_start()
    time.sleep(2)

    #开始测试
    test_start(run_time = 20,interval_time = 280)


    '''
    while True:
        publish_message(topic,'C6')
        time.sleep(5)
        publish_message(topic,'C7')
        time.sleep(5)
        '''
    client.loop_stop()
