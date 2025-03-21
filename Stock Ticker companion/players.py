import PySimpleGUI as sg
import sqlite3

def input_players(database,p_num):
    
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    #TODO: DELETE THE FOLLOWING BEFORE ROLLOUT#
    cursor.execute("DROP TABLE player_info")
    connection.commit()

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

    sg.set_options(font=('Arial', 16))
    player_input_layout = [
   [sg.Text('Enter Info For Player 1: ', key='display')],
   [sg.Text('players name: '), sg.Input(key='Name')],
   [sg.Text('Select How Many of Each Security They Start With')],
   [sg.Text('Grain'),sg.Combo([0,1,2,3,4,5],default_value=0,key='amm_grain'),
    sg.Text('Ind.'),sg.Combo([0,1,2,3,4,5],default_value=0,key='amm_ind'),
    sg.Text('Bonds'),sg.Combo([0,1,2,3,4,5],default_value=0,key='amm_bonds'),
    sg.Text('Oil'),sg.Combo([0,1,2,3,4,5],default_value=0,key='amm_oil'),
    sg.Text('Silver'),sg.Combo([0,1,2,3,4,5],default_value=0,key='amm_silver'),
    sg.Text('Gold'),sg.Combo([0,1,2,3,4,5],default_value=0,key='amm_gold')
    ],
   [sg.Button("Submit", key='add_player'), sg.Button('Exit')],
    ]
    
    player_window = sg.Window('Player Window', player_input_layout, finalize=True)
    player_count = 0
    flag = False

    while True:
        event, values = player_window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        elif event == 'add_player':
            player_count += 1
            #print('\nnumber of players: ',p_num,"\nCurrent player: ", player_count)
            
            if values['Name'] == None or values['Name'] == '':
                sg.popup("Error!\nYou Need to enter a name!")
                player_count -= 1
                print("\n\nERROR Player Count: ",player_count)
                flag = True
            else:
            
                name = values['Name']
                amm_grain = values['amm_grain']
                amm_ind = values['amm_ind']
                amm_bonds = values['amm_bonds']
                amm_oil = values['amm_oil']
                amm_silver = values['amm_silver']
                amm_gold = values['amm_gold']

                total_sec = amm_grain + amm_ind + amm_bonds + amm_oil + amm_silver + amm_gold
                #print("Total securities selected: ",total_sec)

            if total_sec > 5:
                sg.popup("Error!\nYou can only have a max of 5 securities total!!")
                # input_players(player_count)
                player_count -= 1
                flag = True

            elif total_sec < 5:
                money = 1000*(5 - total_sec)
                result = [player_count,1, name, money, amm_grain, amm_ind, amm_bonds, amm_oil, amm_silver, amm_gold, 5000]

            elif total_sec == 5:
                money = 0
                result = [player_count,1, name, money, amm_grain, amm_ind, amm_bonds, amm_oil, amm_silver, amm_gold, 5000]

            if flag:
                print('Not adding to database!!')
            else:
                print('\nAdded',result[2],'data to the database!')
                cursor.execute("INSERT INTO player_info VALUES (?,?,?,?,?,?,?,?,?,?,?)", (result))
                connection.commit()
                player_window['Name'].update('')
                for key in ['amm_grain','amm_ind','amm_bonds','amm_oil','amm_silver','amm_gold']:
                    player_window[key].update(0)
                player_window['display'].update('Enter Info For Player %d: '%(player_count+1))


            if player_count == p_num:
                player_window.close()
                break

            flag = False

