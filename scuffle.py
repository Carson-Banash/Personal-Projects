import PySimpleGUI as sg

sg.theme('black')
size = (3,1)
key_size = (1.5,1)
sg.set_options(font = 'Franklin 20')
layout = [
    [sg.Text("SCUFFLE",justification='center',pad=(20,5),expand_x=True,font="Franklin 22",text_color='white')],
    [sg.Text('',key="-11-",justification='center',background_color='gray'),sg.Text('',key="-12-",justification='center'),sg.Text('',key="-13-",justification='center'),sg.Text('',key="-14-",justification='center'),sg.Text('',key="-15-",justification='center')],
    [sg.HorizontalSeparator()],
    [sg.Text('',expand_x=True),sg.Button('Q',size=key_size),sg.Button('W',size=key_size),sg.Button('E',size=key_size),sg.Button('R',size=key_size),sg.Button('T',size=key_size),sg.Button('Y',size=key_size),sg.Button('U',size=key_size),sg.Button('I',size=key_size),sg.Button('O',size=key_size),sg.Button('P',size=key_size),sg.Text('',expand_x=True)],
    [sg.Text('',expand_x=True),sg.Button('A',size=key_size),sg.Button('S',size=key_size),sg.Button('D',size=key_size),sg.Button('F',size=key_size),sg.Button('G',size=key_size),sg.Button('H',size=key_size),sg.Button('J',size=key_size),sg.Button('K',size=key_size),sg.Button('L',size=key_size),sg.Text('',expand_x=True)],
    [sg.Text('',expand_x=True),sg.Button('ENT',size=size),sg.Button('Z',size=key_size),sg.Button('X',size=key_size),sg.Button('C',size=key_size),sg.Button('V',size=key_size),sg.Button('B',size=key_size),sg.Button('N',size=key_size),sg.Button('M',size=key_size),sg.Button('DEL',size=size),sg.Text('',expand_x=True)]
]

window = sg.Window('Scuffle', layout) #size = (400,600), element_justification = 'center'

while True:
    event, values = window.read()
    guess = []
    if event == sg.WIN_CLOSED:
        break
    else:
        window['-11-'].update(event)
        window[event].update(button_color=('black','red'))
window.close()