import PySimpleGUI as sg
import sqlite3

def graph_game(database):
    def create_plot(active,database):

        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        color = {'grain':'#EDC643','ind':'#EE7A8D','bonds':'#93A561','oil':'#94B6C5','silver':'#D2C3AB','gold':'#F2A547'}
        
        cursor.execute("SELECT ID FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
        tpl = cursor.fetchone()
        num_of_entries = tpl[0]

        window['graph'].erase()
        x_step = 1400/num_of_entries

        for sec in active:
            cursor.execute("SELECT "+sec+" FROM board_info;")
            raw_result = cursor.fetchall()
            result = [x[0] for x in raw_result]

            x=0
            for i in range(num_of_entries-1):
                window['graph'].draw_line((x,result[i]),(x+x_step,result[i+1]), color=color[sec], width=1) 
                x=x+x_step       

        for y, color in [(0, 'red'), (1000, 'blue'), (2000, 'green')]:
            for x in range(-1, 1400, int(x_step)): 
                window['graph'].draw_line((x, y), (x+1, y), color=color, width=2)
        
    btn_size = (6,2)
    bt = sg.Button('Toggle On All', size=btn_size, key='toggle_all', button_color='black on grey')
    b1 = sg.Button('Grain', size=btn_size, key='grain',button_color='white on red')
    b2 = sg.Button('Ind.', size=btn_size, key='ind',button_color='white on red')
    b3 = sg.Button('Bonds', size=btn_size, key='bonds',button_color='white on red')
    b4 = sg.Button('Oil', size=btn_size, key='oil',button_color='white on red')
    b5 = sg.Button('Silver', size=btn_size, key='silver',button_color='white on red')
    b6 = sg.Button('Gold', size=btn_size, key='gold',button_color='white on red')
    eb = sg.Button('Exit', size=btn_size, key='Exit', button_color='black on red')

    layout = [
        [sg.Graph(
            canvas_size=(1400, 800),
            graph_bottom_left=(-1, -50),
            graph_top_right=(1400, 2100),
            background_color='black',
            key='graph')],
            [bt,sg.Text(expand_x=True,background_color='grey',size=(1,6),pad=(0,0)),b1,b2,b3,b4,b5,b6,sg.Text(expand_x=True,background_color='grey',size=(1,6),pad=(0,0)),eb],
            ]


    window = sg.Window("plot",layout, finalize=True,element_justification='c',margins=(0,0),background_color='black',no_titlebar=True)


    securities = ['grain','ind','bonds','oil','silver','gold']
    colors = {'grain':'black on #EDC643','ind':'black on #EE7A8D','bonds':'black on #93A561','oil':'black on #94B6C5','silver':'black on #D2C3AB','gold':'black on #F2A547'}
    active = []

    all_on = False

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            print('Ending Program!')
            window.close()
            break
        if event in securities:
            old_color = window[event].ButtonColor
            if old_color[1] == 'red':
                window[event].update(button_color=colors[event])
                active.append(event)
            else:
                window[event].update(button_color='white on red')
                active.remove(event)
        elif event == 'toggle_all':
            if sorted(active) != sorted(securities):
                for sec in securities:
                    if sec not in active:
                        window[sec].update(button_color=colors[sec])
                        active.append(sec)
            else:
                for sec in securities:
                    window[sec].update(button_color='white on red')
                    active.remove(sec)
                    
        if sorted(active) == sorted(securities):
            window['toggle_all'].update('Toggle Off All')
        elif sorted(active) != sorted(securities) :
            window['toggle_all'].update('Toggle On All')
        
        create_plot(active,database)
