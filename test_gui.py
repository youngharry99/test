import PySimpleGUI as sg
import mqttSend as ms
import time
sg.theme('DarkAmber')   # Add a touch of color
layout = [
    [sg.Text("终端SN:"), sg.Input(key="SN", do_not_clear=True) ],
    [sg.Button("亮灯"), sg.Button("上报车辆数据")],
    [sg.Text("Beat:"), sg.Input(key="BEAT", do_not_clear=True)],
    [sg.Text("授权类型:"), sg.Combo(('MP3租赁', 'WAV租赁','进阶租赁'), key="-CB-",default_value='请选择',size=(20,1), enable_events=True)],
    [sg.Button("确定"), sg.Exit()]
]

if __name__ == '__main__':
    window = sg.Window("暗锁测试工具", layout,element_justification="right")
    ms.clinet_Init()

    ms.client.loop_start()
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
