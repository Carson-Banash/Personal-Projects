import PySimpleGUI as sg
import sqlite3
import datetime

import rolls
import players
import buysell

# using now() to get current time
current_time = datetime.datetime.now()

#creates a database file with the current date and time. for archiving
# database = f'Stock Ticker Game {current_time.day},{current_time.month},{current_time.year} {current_time.hour}:{current_time.minute}.db'
database = 'test.db'
#connects to the database
# connection = sqlite3.connect(database)
# cursor = connection.cursor()

# cursor.execute("""CREATE TABLE player_info (
#     id INTEGER PRIMARY KEY,
#     recent INTEGER,
#     name TEXT,
#     cash INTEGER,
#     grain INTEGER,
#     ind INTEGER,
#     bonds INTEGER,  
#     oil INTEGER,
#     silver INTEGER,
#     gold INTEGER,
#     net_worth INTEGER
# );""")
# connection.commit()

# cursor.execute("""CREATE TABLE board_info (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     grain INTEGER,
#     ind INTEGER,
#     bonds INTEGER,  
#     oil INTEGER,
#     silver INTEGER,
#     gold INTEGER
# );""")
# connection.commit()

# cursor.execute("INSERT INTO board_info VALUES (NULL, 1000,1000,1000,1000,1000,1000);")
# connection.commit()

#----------------------------------#
def start():
   sg.set_options(font=('Arial', 16))
   layout1 = [
      [sg.Text('Welcome!!')],
      [sg.Text('Select how many players there are:')],
      [sg.Combo([2,3,4,5,6,7,8],default_value=' ',key='num_players',readonly=True)],
      [sg.Text('How many rolls will be between Buy/Sell phase?')],
      [sg.Slider(range=(2,20),default_value=5,orientation='horizontal',key='rolls_between')],
      [sg.Button('Submit',key='player_entry'), sg.Button('Exit')]
   ]
   return sg.Window('First Window', layout1, finalize=True)

def last_round():
    lr_layout = [
        [sg.Text('You have indicated that this will be the last few rolls before the end of the game!\nPlease indicate below how many rolls each player should have before the game is over.')],
        [sg.Slider(range=(2,20),default_value=5,orientation='horizontal',key='lr_rolls')],
        [sg.Button('Confirm',key='lr_rolls_confirm')]
    ]

    lr_info_window = sg.Window('Roll Window', lr_layout, finalize=True)

    while True:
        event, values = lr_info_window.read()

        if event == 'lr_rolls_confirm':
            lr_amm_rolls = values['lr_rolls']
            lr_info_window.close()
            break

    return lr_amm_rolls

start_window = start()

player_number = 1
t_read = 0
final_round = False

while True:
    event, values = start_window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    
    elif event == 'player_entry':
        num_of_p = values['num_players']
        amm_rolls = int(values['rolls_between'])

        if not isinstance(num_of_p, int) or num_of_p < 2 or num_of_p > 8:
            sg.popup('Incorrect input please try again!')
            break
        
        # players.input_players(database,num_of_p)

        while final_round == False:
            start_window.close()
            rolls.roll(database,amm_rolls,num_of_p)
            final_round = buysell.buy_sell(database)
            print(final_round)

        lr_rolls = last_round()
        print(lr_rolls)

        rolls.roll(database,lr_rolls,num_of_p)
            
        