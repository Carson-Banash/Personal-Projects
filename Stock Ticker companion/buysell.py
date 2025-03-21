import PySimpleGUI as sg
import sqlite3

def buy_sell(database):

    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT name FROM player_info;")
    players = cursor.fetchall()
    
    def update_elements(elem_lst, max_values, start=0):
        j = start
        for elem in elem_lst:
            to_update = []
            for k in range(max_values[j]+1):
                to_update.append(k)
            # print(key,': ',to_update)
            window[elem].update(value=0, values=to_update)
            j += 1


    sg.set_options(font=('Arial', 16))
    layout = [
    [sg.Text('Buy and Sell')],
    [sg.Text('players name: '), sg.Combo(players, key='name_chosen',enable_events=True)],
    [sg.Text('select how many of each security to sell')],
    [sg.Text('Grain'),sg.Combo([0],default_value=0,key='sell_grain',readonly=True),
        sg.Text('Ind.'),sg.Combo([0],default_value=0,key='sell_ind',readonly=True),
        sg.Text('Bonds'),sg.Combo([0],default_value=0,key='sell_bonds',readonly=True),
        sg.Text('Oil'),sg.Combo([0],default_value=0,key='sell_oil',readonly=True),
        sg.Text('Silver'),sg.Combo([0],default_value=0,key='sell_silver',readonly=True),
        sg.Text('Gold'),sg.Combo([0],default_value=0,key='sell_gold',readonly=True)
        ],
    [sg.Button("Sell", key='sell', button_color='red')],

        [sg.Text('Select how many of each security to buy: ')],
    [sg.Text('Grain'),sg.Combo([0],default_value=0,key='buy_grain',enable_events=True,readonly=True),
        sg.Text('Ind.'),sg.Combo([0],default_value=0,key='buy_ind',enable_events=True,readonly=True),
        sg.Text('Bonds'),sg.Combo([0],default_value=0,key='buy_bonds',enable_events=True,readonly=True),
        sg.Text('Oil'),sg.Combo([0],default_value=0,key='buy_oil',enable_events=True,readonly=True),
        sg.Text('Silver'),sg.Combo([0],default_value=0,key='buy_silver',enable_events=True,readonly=True),
        sg.Text('Gold'),sg.Combo([0],default_value=0,key='buy_gold',enable_events=True,readonly=True)
        ],

        [sg.Button("Buy", key='buy', button_color='green')],
        [sg.Button('Exit',button_color='orange')],
        [sg.Text(expand_x=True)],
        [sg.Button("Last round?",key='end')]
        
        ]

    window = sg.Window('First Window', layout, finalize=True)

    sell_lst = ['sell_grain','sell_ind','sell_bonds','sell_oil','sell_silver','sell_gold']
    buy_lst = ['buy_grain','buy_ind','buy_bonds','buy_oil','buy_silver','buy_gold']
    changed = []
    final_round = False

    while True:
        event, values = window.read()
        # print(event, values)

        if event in (sg.WIN_CLOSED, 'Exit'):
            print('Ending Program!')
            window.close()
            break

        elif event == 'end':
            print('ending')
            final_round = True

        elif event == 'name_chosen':
            changed=[]
            ch_name = values['name_chosen'][0]
            cursor.execute("SELECT * FROM player_info WHERE name = '"+ch_name+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+ch_name+"');")
            player_info = list(cursor.fetchone())

            update_elements(sell_lst,player_info,4)
            
            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            sec_price = list(cursor.fetchone())
            del sec_price[0]
            # print(sec_price)
            cash = player_info[3]
            print("The amount of Cash is: %d"%cash)
            if  cash != 0:
                max_amm_buy = []
                for k in range(len(sec_price)):
                    # print('\nprice of security: ',sec_price[k],'\nable to buy: ',cash//sec_price[k])
                    max_amm_buy.append(cash//sec_price[k])

                update_elements(buy_lst,max_amm_buy)
                print('max amm buy',max_amm_buy)
            else: 
                for key in buy_lst:
                    window[key].update(value=0)

        elif event == 'sell':
            #gets the name, necessary for getting the information from the database
            ch_name = values['name_chosen'][0]

            #gets the amount of owned securities of the chosen players from the database
            cursor.execute("SELECT * FROM player_info WHERE name = '"+ch_name+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+ch_name+"');")
            player_info = list(cursor.fetchone())
            cash = player_info[3]

            # print(player_info)

            #dictionary and lists required for iterating through the chosen amounts to create lists with the amounts
            player_sec_key = {'grain':4,'ind':5,'bonds':6,'oil':7,'silver':8,'gold':9}
            # sell_sec = ['sell_grain','sell_ind','sell_bonds','sell_oil','sell_silver','sell_gold']
            owned_sec = ['grain','ind','bonds','oil','silver','gold']

            #The following creates the list that stores the amount of sold securities
            amm_sell = []
            for key in sell_lst:            
                #appends the value of the chosen amount to sell to the list
                amm_sell.append(int(values[key]))
            
            #the following creates the list that stores the owned amount of securities from the database 
            amm_owned = []
            for key in owned_sec:
                #appends the owned amount of each security from the database
                amm_owned.append(player_info[player_sec_key[key]])

            print('the amount being sold is: ',amm_sell)
            print('the amount that is owned is: ',amm_owned)
            # print("test statement: ",all(isinstance(sec, int) for sec in amm_sell))

            #if the user has input an amount of any security that the player does not own it is saved as a string
            #the following catches that error, shows a popup window to the user and sets all the securities chosen
            #back to zero
            if not all(isinstance(sec, int) for sec in amm_sell):
                #the following loop is for setting the chosen amounts back to zero
                for key in sell_lst:
                    window[key].update(value=0)
                #creates a popup explain to the user the error
                sg.popup("Error!\nYou are trying to sell more securities than that player owns!")
                #skips the rest of the error due to the error
                continue
            
            #calculates the difference in the securities owned and the amount sold
            final_amm = [x-y for x, y in zip(amm_owned, amm_sell)]
            print(final_amm)
            #updates the gui to display the new amount owned to prevent double selling the same thing and if another sell action is needed
            update_elements(sell_lst,final_amm)
            
            #the following gets the current values of the securities on the board from the database
            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            sec_value = list(cursor.fetchone())
            del sec_value[0]

            cash_sell = 0
            for i in range(6):
                cash_sell += sec_value[i] * amm_sell[i]
            
            total_cash = cash + cash_sell

            print('cash in hand: %d\ncash from selling: %d\nnew total cash: %d'%(cash,cash_sell,total_cash))
            
            new_player_info = [None,player_info[1]+1, ch_name, total_cash]+final_amm+[player_info[10]]
            cursor.execute("INSERT INTO player_info VALUES (?,?,?,?,?,?,?,?,?,?,?)", (new_player_info))
            connection.commit()

            # print(new_player_info)

            max_amm_buy = []
            for k in range(len(sec_value)):
                max_amm_buy.append(total_cash//sec_value[k])
            print(max_amm_buy)

            update_elements(buy_lst,max_amm_buy)
            
            sg.set_options(font=('Arial', 18))
            sg.popup("The total cash is %d"%cash_sell)
            
        elif event in buy_lst and event not in changed:
            #gets the name, necessary for getting the information from the database
            ch_name = values['name_chosen'][0]
            changed.append(event)
            print('Changed Values are',changed)

            #gets the amount of owned securities of the chosen players from the database
            cursor.execute("SELECT * FROM player_info WHERE name = '"+ch_name+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+ch_name+"');")
            player_info = list(cursor.fetchone())
            cash = player_info[3]

            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            sec_value = list(cursor.fetchone())
            del sec_value[0]
            
            player_sec_key = {'grain':4,'ind':5,'bonds':6,'oil':7,'silver':8,'gold':9}
            owned_sec = ['grain','ind','bonds','oil','silver','gold']

            #The following creates the list that stores the amount of bought securities
            amm_buy = []
            for key in buy_lst:            
                #appends the value of the chosen amount to buy to the list
                amm_buy.append(int(values[key]))

            cash_buy = 0
            for i in range(6):
                cash_buy += sec_value[i] * amm_buy[i]
            
            cash_left = cash - cash_buy
            print('The cash left is: ',cash_left)

            #if the user has somehow selected more securities than they can afford their money will be below zero, 
            #the following catches that and shows a popup window to the user and sets all the securities chosen
            #back to zero
            if cash_left < 0:
                #the following loop is for setting the chosen amounts back to zero
                for key in buy_lst:
                    window[key].update(value=0)
                #creates a popup explain to the user the error
                sg.popup("Error!\nYou are trying to buy more securities than that player can afford!")
                #skips the rest of the error due to the error
                continue

            # print(cash_buy)

            
            to_change = [key for key in buy_lst if key not in changed]
            # buy_lst = ['buy_grain','buy_ind','buy_bonds','buy_oil','buy_silver','buy_gold']s

            amm_buy_key = {'buy_grain':0,'buy_ind':1,'buy_bonds':2,'buy_oil':3,'buy_silver':4,'buy_gold':5}

            print(amm_buy)
            i = 0
            for sec in buy_lst:
                if sec in changed:
                    
                    print('cash left: ',cash_left,'security value: ',sec_value[i],'max amount to buy: ',cash_left//sec_value[i])
                    max_amm_buy = []
                    for j in range(-1*(amm_buy[i]),(cash_left//sec_value[i])+1):
                        max_amm_buy.append(j)
                    
                    print('the new amount to buy is: ',max_amm_buy)
                    window[sec].update(value=amm_buy[amm_buy_key[sec]],values=max_amm_buy)
                    i += 1
                else:
                    max_amm_buy = []
                    for j in range((cash_left//sec_value[i])+1):
                        max_amm_buy.append(j)

                    window[sec].update(value=0, values=max_amm_buy)

                    i += 1
            
            print('\n\ncash in hand: %d\ncash used to buy: %d\nnew total cash: %d'%(cash,cash_buy,cash_left))

        elif event in changed:
            ch_name = values['name_chosen'][0]
            print('the value changed is: ',event)
            #gets the amount of owned securities of the chosen players from the database
            cursor.execute("SELECT * FROM player_info WHERE name = '"+ch_name+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+ch_name+"');")
            player_info = list(cursor.fetchone())
            cash = player_info[3]

            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            sec_value = list(cursor.fetchone())
            del sec_value[0]

            amm_buy_key = {'buy_grain':0,'buy_ind':1,'buy_bonds':2,'buy_oil':3,'buy_silver':4,'buy_gold':5}

            #The following creates the list that stores the amount of bought securities
            amm_buy = []
            for key in buy_lst:            
                #appends the value of the chosen amount to buy to the list
                amm_buy.append(int(values[key]))
            
            print(prev_buy, 'Before')
            print(amm_buy, ' amount bought')

            for key in buy_lst:
                if key == event:
                    amm_buy[amm_buy_key[event]] = amm_buy[amm_buy_key[event]]+prev_buy[amm_buy_key[event]]
                    window[event].update(value=amm_buy[amm_buy_key[event]])
                    print(amm_buy,'After')
            
            cash_buy = 0
            for i in range(6):
                cash_buy += sec_value[i] * amm_buy[i]
            
            cash_left = cash - cash_buy
            print('changed value\nThe cash left is: ',cash_left)

            #if the user has somehow selected more securities than they can afford their money will be below zero, 
            #the following catches that and shows a popup window to the user and sets all the securities chosen
            #back to zero
            if cash_left < 0:
                #the following loop is for setting the chosen amounts back to zero
                for key in buy_lst:
                    window[key].update(value=0)
                #creates a popup explain to the user the error
                sg.popup("Error!\nYou are trying to buy more securities than that player can afford!")
                #skips the rest of the error due to the error
                continue

            i = 0
            for sec in buy_lst:
                if sec in changed:
                    
                    print('cash left: ',cash_left,'security value: ',sec_value[i],'max amount to buy: ',cash_left//sec_value[i])
                    max_amm_buy = []
                    for j in range(-1*(amm_buy[i]),(cash_left//sec_value[i])+1):
                        max_amm_buy.append(j)
                    
                    print('the new amount to buy is: ',max_amm_buy)
                    window[sec].update(value=amm_buy[amm_buy_key[sec]],values=max_amm_buy)
                    i += 1
                elif sec == event:
                    print('is changed value, not modifying')
                    i+=1
                else:
                    max_amm_buy = []
                    for j in range((cash_left//sec_value[i])+1):
                        max_amm_buy.append(j)

                    window[sec].update(value=0, values=max_amm_buy)

                    i += 1


        elif event == 'buy':
            changed = []

            ch_name = values['name_chosen'][0]

            player_sec_key = {'grain':4,'ind':5,'bonds':6,'oil':7,'silver':8,'gold':9}
            owned_sec = ['grain','ind','bonds','oil','silver','gold']

            cursor.execute("SELECT * FROM player_info WHERE name = '"+ch_name+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+ch_name+"');")
            player_info = list(cursor.fetchone())
            cash = player_info[3]

            #the following creates the list that stores the owned amount of securities owned from the database 
            amm_owned = []
            for key in owned_sec:
                #appends the owned amount of each security from the database
                amm_owned.append(player_info[player_sec_key[key]])

            
            #The following creates the list that stores the amount of bought securities
            amm_buy = []
            for key in buy_lst:            
                #appends the value of the chosen amount to buy to the list
                amm_buy.append(int(values[key]))

            final_amm = [x+y for x, y in zip(amm_owned, amm_buy)]

            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            sec_value = list(cursor.fetchone())
            del sec_value[0]

            cash_buy = 0
            for i in range(6):
                cash_buy += sec_value[i] * amm_buy[i]
            
            total_cash = cash - cash_buy

            print('Amount bought: ',amm_buy,'\nSecurities owned: ',amm_owned,'\nNew total: ', final_amm)

            #if the user has somehow selected more securities than they can afford their money will be below zero, 
            #the following catches that and shows a popup window to the user and sets all the securities chosen
            #back to zero
            if cash_left < 0:
                #the following loop is for setting the chosen amounts back to zero
                for key in buy_lst:
                    window[key].update(value=0)
                #creates a popup explain to the user the error
                sg.popup("Error!\nYou are trying to buy more securities than that player can afford!")
                #skips the rest of the error due to the error
                continue
            
            new_player_info = [None,player_info[1]+1, ch_name, total_cash]+final_amm+[player_info[10]]
            cursor.execute("INSERT INTO player_info VALUES (?,?,?,?,?,?,?,?,?,?,?)", (new_player_info))
            connection.commit()

            print('adding ',new_player_info,' to database')

            max_amm_buy = []
            for k in range(len(sec_value)):
                # print('\nprice of security: ',sec_price[k],'\nable to buy: ',cash//sec_price[k])
                max_amm_buy.append(total_cash//sec_value[k])

            update_elements(buy_lst,max_amm_buy)

            update_elements(sell_lst,final_amm)

            sg.set_options(font=('Arial', 18))
            sg.popup("The amount of money needed for the purchase is:\n%d"%cash_buy)


        event, values = window.read(timeout=1)
        
        #the following gets the amount of securities to buy before a new selection is made
        prev_buy = []
        for key in buy_lst:            
            #appends the value of the chosen amount to previously bought list
            prev_buy.append(int(values[key]))
        
        print('previously bought',prev_buy)

    return final_round