import PySimpleGUI as sg

def win1():
   sg.set_options(font=('Arial', 16))
   layout1 = [
      [sg.Text('Welcome!!')],
      [sg.Text('Select how many players there are:')],
      [sg.Combo([2,3,4,5,6,7,8],default_value=' ',key='num_players')],
      [sg.Button('Submit',key='player_entry'), sg.Button('Exit')]
   ]
   return sg.Window('First Window', layout1, finalize=True)

def wait_to_start():
   sg.set_options(font=('Arial', 16))
   wait_layout = [
      [sg.Text('Warning!!',font=('Arial',20),text_color='Yellow')],
      [sg.Text('input player info BEFORE selecting next')],
      [sg.Button('Next',key='start_game')]
   ]
   return sg.Window('Wait Window', wait_layout, finalize=True)

def input_players(p_num):
    sg.set_options(font=('Arial', 16))
    layout2 = [
   [sg.Text('Enter Info For Player %d: ' % p_num)],
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
    return sg.Window('Player Window %d'% p_num, layout2, finalize=True)
    


window1 = win1()



player_count = 0

while True:
    window, event, values = sg.read_all_windows()
    print("Title: ",window.Title,"\nEvent: ",event,"\nValues: ",values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break


    elif event == 'player_entry':
        print('booga!!')
        window.close()
        wait_to_start()

        p_num = values['num_players']
        if not isinstance(p_num, int) or p_num < 2 or p_num > 8:
            sg.popup('Incorrect input please try again!')
            break

        player_count = 1
        player_window = input_players(player_count)

        while True:
            event, values = player_window.read()
            print('ooga!!')

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            if event == 'add_player':
                player_count += 1
                #print('\nThe player number is: ',player_count)
                print("\nEvent: ",event,"\nValues: ",values)
                if values['Name'] == None:
                    sg.popup("Error!\nYou Need to enter a name!")
                    player_count -= 1
                    print("\n\nERROR Player Count: ",player_count)
                    input_players(player_count)
                else:
                
                    name = values['Name']

                    amm_grain = values['amm_grain']
                    amm_ind = values['amm_ind']
                    amm_bonds = values['amm_bonds']
                    amm_oil = values['amm_oil']
                    amm_silver = values['amm_silver']
                    amm_gold = values['amm_gold']

                    total_sec = amm_grain + amm_ind + amm_bonds + amm_oil + amm_silver + amm_gold
                    print("Total securities selected: ",total_sec)

                if total_sec > 5:
                    sg.popup("Error!\nYou can only have a max of 5 securities total!!")
                    # input_players(player_count)
                    player_count -= 1

                elif total_sec < 5:
                    money = 5 - total_sec
                    result = [player_count, name, money, amm_grain, amm_ind, amm_bonds, amm_oil, amm_silver, amm_gold]
                    #print(result)

                elif total_sec == 5:
                    money = 0
                    result = [player_count, name, money, amm_grain, amm_ind, amm_bonds, amm_oil, amm_silver, amm_gold]
                    #print(result)
                
                # print(result)
                player_window.close()
                
                if player_count <= p_num:
                    print("\n\nREGULAR Player Count: ",player_count)
                    player_window = input_players(player_count)
                if player_count == p_num+1:
                    break
                
        
    elif event == 'start_game':
        print('\nSTARTING GAME!\nSTARTING GAME!\nSTARTING GAME!')

        
    
        
