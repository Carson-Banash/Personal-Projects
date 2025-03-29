import PySimpleGUI as sg
import sqlite3

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_plot():
    plt.style.use('dark_background')
    plt.margins(x=0,y=0)

    database = 'Stock Ticker Game 25,3,2025 13:14.db'
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    securities = ['grain','ind','bonds','oil','silver','gold']
    color = {'grain':'#EDC643','ind':'#EE7A8D','bonds':'#93A561','oil':'#94B6C5','silver':'#D2C3AB','gold':'#F2A547'}
    
    for sec in securities:
        cursor.execute("SELECT "+sec+" FROM board_info;")
        raw_result = cursor.fetchall()
        result = [x[0] for x in raw_result]
        # print(result)
        
        plt.plot(result, color=color[sec],lw=0.75)
        

    plt.hlines(y=[2000, 1000, 0], xmin=0, xmax=len(result), colors=['green','blue','red'], ls='--')

    plt.axis('off')
    plt.subplots_adjust(left=0.01,right=0.99,bottom=0.01,top=0.99)
    # plt.show()
    return plt.gcf()


# market_value = []
# for i in range(len(raw_result)):
#     market_value.append(raw_result[i][1])

# print(time)
# print(market_value)

# plt.plot(market_value,color='#94B6C5')
# plt.title('Value of security over game', fontsize=14)


# plt.grid(axis='y')
# plt.show()
btn_size = (6,2)
b1 = sg.Button('Grain', size=btn_size, key='grain',button_color='black on #EDC643')
b2 = sg.Button('Ind.', size=btn_size, key='ind',button_color='black on #EE7A8D')
b3 = sg.Button('Bonds', size=btn_size, key='bonds',button_color='black on #93A561')
b4 = sg.Button('Oil', size=btn_size, key='oil',button_color='black on #94B6C5')
b5 = sg.Button('Silver', size=btn_size, key='silver',button_color='black on #D2C3AB')
b6 = sg.Button('Gold', size=btn_size, key='gold',button_color='black on #F2A547')

buttons = [[b1],[b2],[b3],[b4],[b5],[b6]]
layout = [
    [sg.Column(buttons,element_justification='center'),sg.Canvas(size=(1275,920),key='graph',pad=(0,0))]      
          ]

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

window = sg.Window("plot",layout, finalize=True, margins=(0,0))

draw_figure(window['graph'].TKCanvas, create_plot())

securities = ['grain','ind','bonds','oil','silver','gold']
colors = {'grain':'black on #EDC643','ind':'black on #EE7A8D','bonds':'black on #93A561','oil':'black on #94B6C5','silver':'black on #D2C3AB','gold':'black on #F2A547'}

clicked = True
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event in securities:
        
        window[event].update(button_color='white on red' if clicked else colors[event])
        clicked = not clicked