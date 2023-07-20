import PySimpleGUI as sg
#import mqttSend as ms
import time
sg.theme('DarkAmber')   # Add a touch of color
layout = [
    [sg.Text("测试网: " + ms.broker + " 端口: " + str(ms.port) + " 状态 ", font=('Arial Bold', 15))],
    [sg.Text("终端SN: ", font=('Arial', 15)), sg.Input(key="SN" , default_text= str(ms.sn), do_not_clear=True, font=('Arial', 15), size=(15,1))],
    [sg.Button("亮灯"), sg.Button("获取车辆数据")],
    [sg.Text("Beat:"), sg.Input(key="BEAT", do_not_clear=True)],
    [sg.Text("授权类型:"), sg.Combo(('MP3租赁', 'WAV租赁','进阶租赁'), key="-CB-",default_value='请选择',size=(20,1), enable_events=True)],
    [sg.Button("确定"), sg.Exit()]
]

if __name__ == '__main__':
    window = sg.Window("暗锁测试工具", layout)
    #ms.clinet_Init()

    #ms.client.loop_start()
    while True:
        event, values = window.read()

        #退出按钮
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break

        if event == "确定":
            break

        if event == "亮灯":
            ms.publish_message(ms.topic, 'C6')

        if event == "上报车辆数据":
            ms.get_car_reporting_data()
            #time.sleep(1)

    ms.client.loop_start()
    window.close()
