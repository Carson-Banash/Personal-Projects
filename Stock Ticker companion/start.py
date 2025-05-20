import PySimpleGUI as sg
import sqlite3
import datetime

import rolls
import players
import buysell
import graph

def create_database():
    # using now() to get current time
    current_time = datetime.datetime.now()

    #creates a database file with the current date and time. for archiving
    database = f'PastGames/StockTickerGame-{current_time.day},{current_time.month},{current_time.year}-{current_time.hour}:{current_time.minute}.db'
    # database = 'test.db'
    # connects to the database
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE player_info (
        id INTEGER PRIMARY KEY,
        recent INTEGER,
        name TEXT,
        cash INTEGER,
        grain INTEGER,
        ind INTEGER,
        bonds INTEGER,  
        oil INTEGER,
        silver INTEGER,
        gold INTEGER,
        net_worth INTEGER
    );""")
    connection.commit()

    cursor.execute("""CREATE TABLE board_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grain INTEGER,
        ind INTEGER,
        bonds INTEGER,  
        oil INTEGER,
        silver INTEGER,
        gold INTEGER
    );""")
    connection.commit()

    cursor.execute("INSERT INTO board_info VALUES (NULL, 1000,1000,1000,1000,1000,1000);")
    connection.commit()
    return database

def welcome():
    sg.set_options(font=('Arial', 16))
    layout = [
      [sg.Push(),sg.Text('Welcome!!', font=('Arial', 20)),sg.Push()],
      [sg.Push(),sg.Text('To the Stock Ticker Companion App'),sg.Push()],
      [sg.Push(),sg.Text('how you would like to use this app'),sg.Push()],
      [sg.Button('New Game',key='new',button_color='black on #66FA34'),sg.Button('View Past Graphs',key='graph',button_color='black on #FAB922'),sg.Button('Load an old game',key='old',button_color='black on #4F9CFA')],
      [sg.Button('Exit')]
    ]
    welcome_window = sg.Window('welcome', layout, finalize=True) 

    while True:
        #reads the values from the window
        event, values = welcome_window.read()

        #if the exit button is selected then close the window and exit the program
        if event in (sg.WIN_CLOSED, 'Exit'):
            print('Ending Program!')
            welcome_window.close()
            exit()
            break

        new_game = False
        view_graph = False
        load_game = False

        if event == 'new':
            new_game = True
        elif event == 'graph':
            view_graph = True
        elif event == 'old':
            load_game = True
        welcome_window.close()
        break


    return new_game, view_graph, load_game
#----------------------------------#
#This function makes the starting window
#the starting window gets how many players there are and how many rolls there are before buy/sell
#it returns the amount of players and the rolls
def start():
   sg.set_options(font=('Arial', 16))
   layout1 = [
      [sg.Text('Select how many players there are:')],
      [sg.Combo([2,3,4,5,6,7,8],default_value=' ',key='num_players',readonly=True)],
      [sg.Text('How many rolls will be between Buy/Sell phase?')],
      [sg.Slider(range=(2,20),default_value=5,orientation='horizontal',key='rolls_between')],
      [sg.Button('Submit',key='player_entry'), sg.Button('Exit')]
   ]
   start_window = sg.Window('Start', layout1, finalize=True) 

   while True:
        #reads the values from the window
        event, values = start_window.read()

        #if the exit button is selected then close the window and exit the program
        if event in (sg.WIN_CLOSED, 'Exit'):
            print('Ending Program!')
            start_window.close()
            exit()
            break
        
        #if the submit button is selected then get the chosen values and save them. then close the window
        elif event == 'player_entry':
            num_of_p = values['num_players']
            amm_rolls = int(values['rolls_between'])
            start_window.close()
            break
    #return the user inputted values
   return num_of_p,amm_rolls

def recovery_screen():
    rcvry_layout = [
        [sg.Button('Select File', button_color='orange',key='select_file')],
        [sg.Text('How many rolls were between Buy/Sell phase?')],
        [sg.Slider(range=(2,20),default_value=5,orientation='horizontal',key='rolls_between')],
        [sg.Button('To Buy/Sell',key='buysell'),sg.Button('To Rolls',key='rolls')]
    ]
    recovery_window = sg.Window('Start', rcvry_layout, finalize=True) 

    while True:
        #reads the values from the window
        event, values = recovery_window.read()

        #TODO: get the file and save the name as the database and get the amount of players from the database
        if event == 'select_file':
            file_path = sg.PopupGetFile('Select Game File', initial_folder='/PastGames')
            database = "PastGames/"+file_path.split("/")[-1]
            print(database)
            
        if event in ['buysell','rolls']:
            connection = sqlite3.connect(database)
            cursor = connection.cursor()

            #gets the current players
            cursor.execute("SELECT DISTINCT name FROM player_info;")
            result = cursor.fetchall() 

            #creates a list of the list of tuples returned by the database
            players = [item for name in result for item in name]

            num_of_p = len(players)

            print(num_of_p)

            amm_rolls = values['rolls_between']
            screen = event
            recovery_window.close()
            break

    return database, amm_rolls, num_of_p, screen

#this function 
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

def game_end(database):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    #gets the current players
    cursor.execute("SELECT DISTINCT name FROM player_info;")
    result = cursor.fetchall() 

    #creates a list of the list of tuples returned by the database
    players = [item for name in result for item in name]
    win_order = []
    for player in players:
        cursor.execute("SELECT * FROM player_info WHERE name = '"+player+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+player+"');")
        player_info = list(cursor.fetchone())
        net_worth = player_info[10]
        print(f"{player}'s net worth is: ${net_worth}")
        win_order.append((player,net_worth))
    
    win_order.sort(key=lambda x: x[-1],reverse=True)
    # print(win_order)

    layout = [
        [sg.Text("The game is now over!!\nthe leaderboard is as follows:")],
        [sg.Text(key='leaderboard')],
        [sg.Text("Thanks for playing and using the program!")],
        [sg.Button("End Program",button_color='red')]
    ]

    end_window = sg.Window('End Window', layout, finalize=True)
    place = ['First','Second','Third','Fourth','Fifth','Sixth','Seventh','Last']

    leaderboard_msg = []
    for i in range(len(win_order)):
        if i == len(win_order)-1:
            leaderboard_msg.extend(str(f"in {place[-1]} place is {win_order[i][0]} with a total of ${win_order[i][1]}\n"))
        else:
            leaderboard_msg.extend(str(f"in {place[i]} place is {win_order[i][0]} with a total of ${win_order[i][1]}\n"))

    update_msg = ''.join([str(i) for i in leaderboard_msg])
    # print(update_msg)
    end_window['leaderboard'].update(update_msg)

    while True:
        event, values = end_window.read()

        if event in (sg.WIN_CLOSED, 'End Program'):
            print('Ending Program!')
            end_window.close()
            break

        

# sg.set_options(font=('Arial', 16))

final_round = False

new_game, view_graph, load_game = welcome()

if new_game == True:
    num_of_p, amm_rolls = start()

    database = create_database()
    players.input_players(database,num_of_p)
    while final_round == False:
        rolls.roll(database,amm_rolls,num_of_p)
        final_round = buysell.buy_sell(database)
        print(final_round)

    lr_rolls = int(last_round())
    print(lr_rolls)

    rolls.roll(database,lr_rolls,num_of_p)

    game_end(database)

    graph.graph_game(database)

elif view_graph == True:
    file_path = sg.PopupGetFile('Select Game File', initial_folder='/PastGames')
    database = "PastGames/"+file_path.split("/")[-1]
    print(database)

    graph.graph_game(database)

elif load_game == True:
    database, amm_rolls, num_of_p, screen = recovery_screen()

    if screen == 'buysell':
        final_round = buysell.buy_sell(database)


    while final_round == False:
        rolls.roll(database,amm_rolls,num_of_p)
        final_round = buysell.buy_sell(database)
        print(final_round)

    lr_rolls = int(last_round())
    print(lr_rolls)

    rolls.roll(database,lr_rolls,num_of_p)

    game_end(database)

    graph.graph_game(database)