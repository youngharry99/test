import PySimpleGUI as sg
#import mqttSend as ms

sg.theme('DarkAmber')   # Add a touch of color
layout = [
    [sg.Text("终端SN:"), sg.Input(key="SN", do_not_clear=True) ],
    [sg.Text("Beat:"), sg.Input(key="BEAT", do_not_clear=True)],
    [sg.Text("授权类型:"), sg.Combo(('MP3租赁', 'WAV租赁','进阶租赁'), key="-CB-",default_value='请选择',size=(20,1), enable_events=True)],
    [sg.Button("确定"), sg.Exit()]
]

window = sg.Window("暗锁测试工具", layout,element_justification="right")


while True:
    event, values = window.read()

    #退出按钮
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    if event == "确定":
        break
window.close()