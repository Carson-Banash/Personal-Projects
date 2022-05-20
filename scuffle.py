import PySimpleGUI as sg

sg.theme('black')
size = (4,1.5)
key_size = (1.1,1.2)
sg.set_options(font = 'Franklin 20')
layout = [
    [sg.Text("SCUFFLE")],
    [sg.Text('', key="-11-"),sg.Text(''),sg.Text(''),sg.Text(''),sg.Text('')],
    [sg.Button('Start', size=size), sg.Button('Stop', size=size)],
    [sg.Button('Q',size=key_size),sg.Button('W',size=key_size),sg.Button('E',size=key_size),sg.Button('R',size=key_size),sg.Button('T',size=key_size),sg.Button('Y',size=key_size),sg.Button('U',size=key_size),sg.Button('I',size=key_size),sg.Button('O',size=key_size),sg.Button('P',size=key_size)]
]

window = sg.Window('Scuffle', layout) #size = (400,600), element_justification = 'center'

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    else:
        window['-11-'].update(event)
        window['Q'].update(button_color=('black','red'))
        window['R'].update(button_color=('black','green'))
window.close()