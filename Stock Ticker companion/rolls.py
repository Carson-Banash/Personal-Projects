import PySimpleGUI as sg
import sqlite3

connection = sqlite3.connect('st.db')

cursor = connection.cursor()

# dice roll picker

sg.theme('Dark')
sg.set_options(element_padding=(0, 0),font=('Arial', 18))







roll_layout = [
    #radio elements for the different securities
    [sg.Radio('Grain', 'sec',size=(6,1), key='grain',text_color='#EDC643'),
    sg.Radio('Ind.', 'sec',size=(5,1), key='ind',text_color='#EE7A8D'),
    sg.Radio('Bonds', 'sec',size=(7,1), key='bonds',text_color='#93A561'),
    sg.Radio('Oil', 'sec',size=(4,1), key='oil',text_color='#94B6C5'),
    sg.Radio('Silver', 'sec',size=(6,1), key='silver',text_color='#D2C3AB'),
    sg.Radio('Gold', 'sec',size=(7,1), key='gold',text_color='#F2A547')
],
    #radio elements for the modifiers
    [sg.Radio('Up', 'mod', key='up',text_color='#09d928'),
    sg.Radio('Down', 'mod', key='down',text_color='#ed0707'),
    sg.Radio('Dividend', 'mod', key='div')
],
    #radio elements for the amount
    [sg.Radio('5','amm',key='5'),
    sg.Radio('10','amm',key='10'),
    sg.Radio('20','amm',key='20')
],
    #button for submitting the roll
    [sg.Button('Submit',button_color=('green')),sg.Button('Exit', button_color=('white', '#00406B'))]]

# window = sg.Window("Borderless Window",
#                    layout,
#                    default_element_size=(12, 1),
#                    text_justification='b',
#                    auto_size_text=False,
#                    auto_size_buttons=False,
#                    no_titlebar=True,
#                    grab_anywhere=True,
#                    default_button_element_size=(13, 1))
roll_window = sg.Window('Roll Window', roll_layout, default_element_size=(12, 1), return_keyboard_events=True, finalize=True)


#list of all possible sides of dice, used to select the right events
sec = ['grain','ind','bonds','oil','silver','gold']
mod = ['up','down','div']
amm = ['5','10','20']

while True:
    event, values = roll_window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        print('Ending Program!')
        roll_window.close()
        break

    # Check for keyboard events ('1' through '6')
    if event in [str(i) for i in range(1, 7)]:
        radio_number = int(event) - 1  # Convert to index (0-based)
        radio_keys = ['grain', 'ind', 'bonds', 'oil', 'silver', 'gold']
        print(radio_keys[radio_number])
        roll_window[radio_keys[radio_number]].update(value=True)  # Select the appropriate radio button
    elif event in ['Up:2113992448','Down:2097215233','Right:2080438019','Left:2063660802']:
        if event == 'Up:2113992448':
            roll_window['up'].update(value=True)
        elif event == 'Down:2097215233':
            roll_window['down'].update(value=True)
        else:
            roll_window['div'].update(value=True)
    elif event in ['a','s','d']:
        if event == 'a':
            roll_window['5'].update(value=True)
        elif event == 's':
            roll_window['10'].update(value=True)
        elif event == 'd':
            roll_window['15'].update(value=True)



    if event == 'Submit' or event == 'Return:603979789':
        #sets the chosen variables to None, this is used for error handling
        ch_sec,ch_mod,ch_amm = [None,None,None]
        #the following loops though all of the values that were returned by the read of the window
        for key in values:
            #if the value is true then that means that the radio element was selected
            if values[key] == True:
                #if the key is in the list of securities then its a security and it is saved as the chosen security
                if key in sec:
                    ch_sec = key
                #if the key is in the list of modifiers then its a security and it is saved as the chosen modifier
                elif key in mod:
                    ch_mod = key
                #if the key is in the list of amounts then its a security and it is saved as the chosen amount
                elif key in amm:
                    ch_amm = key
 
        #this dictionary is used to determine where the security is in the return of the board info database
        sec_key = {'grain':1,'ind':2,'bonds':3,'oil':4,'silver':5,'gold':6}
        #dictionary required for getting values from the database 
        player_sec_key = {'grain':4,'ind':5,'bonds':6,'oil':7,'silver':8,'gold':9}

        #if any of the chosen variables ar None then a radio element in the window was not selected
        if ch_sec == None or ch_mod == None or ch_amm == None:
            #a popup window is displayed to the user explaining the issue
            sg.popup('Error!!\nOne of the options was not selected!!',title="ERROR")
            #goes through all the elements and sets the radios back to false
            for key in values:
                roll_window[key].update(value=False)
            continue
        
        #the following is responsible for taking the board info from the data base and incrementing the chosen security by the chosen rate
        if ch_mod == 'up':
            #gets the latest entry of the security market values from the database
            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            tpl_result = cursor.fetchone()
            #the following converts the return from the database from a tuple to a list
            result = [*tpl_result]
            #sets the first element to none, this is so that when the values are added back to the database the ID, indicating the most recent entry, will be auto incremented
            result[0] = None

            #gets the current players
            cursor.execute("SELECT DISTINCT name FROM player_info;")
            player_result = cursor.fetchall() 
            #creates a list of the list of tuples returned by the database
            players = [item for name in player_result for item in name]
            
            #calculates the position of the chosen security in the database
            poss = sec_key[ch_sec]
            #gets the value that is currently in the database
            old = result[poss]
            #calculates the new amount as the addition of the old value and the dice roll rate
            new = old + 10*int(ch_amm)

            #if the new value is more than 2000 then the security has split and the market value is returned to 1000
            if new >= 2000:
                #the new value is now 1000 as the security is set back to the par line of 1000
                new = 1000

                #starts the message that will be in a popup telling the user how many securities should be handed out
                msg = f"{ch_sec} has Split!!\n"
                #initializes the list that will be used to create the popup telling the banker what the payout should be to each player
                split_msg = []
                for player in players:
                    #gets the most recent entry from the database for the player
                    cursor.execute("SELECT * FROM player_info WHERE name = '"+player+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+player+"');")
                    player_info = list(cursor.fetchone())
                    
                    #gets the previous amount of the split security
                    old_sec_amm = player_info[player_sec_key[ch_sec]]
                    #doubles the amount of the split security owned
                    new_sec_amm = old_sec_amm*2

                    #calculates the new new worth as difference between the max market value, 2000, and the old market value before the split.
                    #this is then multiplied by the amount of securities the player used to own. this new amount is then added to the old net worth
                    net_worth = player_info[10]+((2000-old)*old_sec_amm)
                    
                    #if the new security is zero then the player does not own any shares in that security so they should not be added to the popup message
                    if new_sec_amm != 0:
                        #creates the string for the player that will be displayed in the popup window for the amount of the payout to receive
                        msg = str(f"{player} gets {old_sec_amm} more {ch_sec} for a total of {new_sec_amm}\n")
                        #extends the ongoing list of payout messages
                        split_msg.extend(msg)

                    #creates the new player info that will be added to the database. the only values that are changed are the recent modifier, the doubled amount of the chosen security and the new net worth
                    new_player_info = [None,player_info[1]+1,player_info[2],player_info[3]]+player_info[4:10]+[net_worth]
                    new_player_info[player_sec_key[ch_sec]] = new_sec_amm

                    #adds the new player entry to the database 
                    cursor.execute("INSERT INTO player_info VALUES (?,?,?,?,?,?,?,?,?,?,?)", (new_player_info))
                    connection.commit()

                #creates the message for the popup window as the combination of all the messages from the different players
                popup_msg = ''.join([str(i) for i in split_msg])
                #makes the popup with the message created above
                sg.popup(popup_msg, title=f'{ch_sec} Has Split')
            else: 
                for player in players:
                    #gets the most recent entry from the database for the player
                    cursor.execute("SELECT * FROM player_info WHERE name = '"+player+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+player+"');")
                    player_info = list(cursor.fetchone())

                    net_worth = player_info[10] + ((10*int(ch_amm))*player_info[player_sec_key[ch_sec]])
                    print(f"{player}'s net worth has changed by {((10*int(ch_amm))*player_info[player_sec_key[ch_sec]])}")

                    #creates the new player info that will be added to the database. the only values that are changed are the recent modifier and the new net worth
                    new_player_info = player_info.copy()
                    new_player_info[1] = new_player_info[1] + 1
                    new_player_info[10] = net_worth
                    
                    print(player_info)
                    print(new_player_info,'\n')
                    #adds the new player entry to the database 
                    # cursor.execute("INSERT INTO player_info VALUES (?,?,?,?,?,?,?,?,?,?,?)", (new_player_info))
                    # connection.commit()
                    

            #replaces the old market value for the chosen security with the new value
            result[poss] = new 
            
            #adds the new value along with the other unchanged values to the database
            # cursor.execute("INSERT INTO board_info VALUES (?,?,?,?,?,?,?)", (result))
            # connection.commit()

        elif ch_mod == 'down':
            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            tpl_result = cursor.fetchone()
            result = [*tpl_result]
            result[0] = None
            

            poss = sec_key[ch_sec]

            old = result[poss]
            new = old + ((10*int(ch_amm)) * -1)
            
            #if the market value of a security falls to zero or below the security has 'busted' all owned securities by players are returned to the banker and the security marker is returned to the par line of 1000
            if new <= 0:
                #since the stock has busted it is set back to the par of 1000
                new = 1000

                #gets the current players
                cursor.execute("SELECT DISTINCT name FROM player_info;")
                player_result = cursor.fetchall() 
                #creates a list of the list of tuples returned by the database
                players = [item for name in player_result for item in name]

                #starts the message that will be in a popup telling the user how many securities should be handed out
                msg = f"{ch_sec} has Busted!!\n"
                #initializes the list that will be used to create the popup telling the banker what the payout should be to each player
                bust_msg = []
                for player in players:
                    #gets the most recent entry from the database for the player
                    cursor.execute("SELECT * FROM player_info WHERE name = '"+player+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+player+"');")
                    player_info = list(cursor.fetchone())
                    
                    #gets the previous amount of the split security
                    old_sec_amm = player_info[player_sec_key[ch_sec]]
                    #sets the new amount to zero
                    new_sec_amm = 0

                    #calculates the new new worth as the total amount of the securities lost
                    #this is then subtracted from the old net worth as the player has lost this value
                    net_worth = player_info[10]-(old_sec_amm*old)
                    print(f"{player}'s old net worth is ${player_info[10]}\nthe new net worth is ${net_worth}")
                    
                    #if the old security is zero then the player did not own any shares in that security so they should not be added to the popup message
                    if old_sec_amm != 0:
                        #creates the string for the player that will be displayed in the popup window for the amount of shares lost
                        msg = str(f"{player} lost {old_sec_amm}\n")
                        #extends the ongoing list of payout messages
                        bust_msg.extend(msg)

                    #creates the new player info that will be added to the database. the only values that are changed are the recent modifier, the doubled amount of the chosen security and the new net worth
                    new_player_info = [None,player_info[1]+1,player_info[2],player_info[3]]+player_info[4:10]+[net_worth]
                    new_player_info[player_sec_key[ch_sec]] = new_sec_amm
                    print(player_info)
                    print(new_player_info)
                    #adds the new player entry to the database 
                    # cursor.execute("INSERT INTO player_info VALUES (?,?,?,?,?,?,?,?,?,?,?)", (new_player_info))
                    # connection.commit()

                #creates the message for the popup window as the combination of all the messages from the different players
                popup_msg = ''.join([str(i) for i in bust_msg])
                #makes the popup with the message created above
                sg.popup(popup_msg, title=f'{ch_sec} Has Split')
                result[poss] = new

            #replaces the old market value for the chosen security with the new value
            result[poss] = new 

            # print(result)

            # cursor.execute("INSERT INTO board_info VALUES (?,?,?,?,?,?,?)", (result))
            # connection.commit()

        elif ch_mod == 'div':
            print("\ndiv chosen")
            #gest all the current market values for the securities
            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            tpl_result = cursor.fetchone()
            #converts the tuple returned by the database to a list, its easier to deal with
            result = [*tpl_result]
            #calculates the position of the chosen security in the database
            poss = sec_key[ch_sec]
            
            #if the value of the security is below 1000 the security will not pay a dividend
            if result[poss] < 1000:
                print("NO DIVIDEND!")
            #otherwise it will pay a dividend
            else:
                #gets the current players
                cursor.execute("SELECT DISTINCT name FROM player_info;")
                result = cursor.fetchall() 

                #creates a list of the list of tuples returned by the database
                players = [item for name in result for item in name]

                #initializes the list that will be used to create the popup telling the banker what the payout should be to each player
                amm_payable = []
                #loops though all the active players
                for player in players:
                    #gets the most recent entry from the database for the player
                    cursor.execute("SELECT * FROM player_info WHERE name = '"+player+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+player+"');")
                    player_info = list(cursor.fetchone())
                    #gets the previous cash amount for the player
                    cash = player_info[3]
                    #calculates the amount to payout as the multiplication of the amount of the security owned and the rate chosen by the dice roll
                    div_payout = int(player_info[player_sec_key[ch_sec]])*int(ch_amm)*10
                    #calculates the new cash value as the addition of the old cash amount and the dividend payout
                    new_cash = div_payout+cash

                    # print(f"{player}'s old cash ${cash} in addition to the payout of ${div_payout} is ${new_cash}")
                    # print(f"{player}'s amount owned {player_info[player_sec_key[ch_sec]]} changed amount {ch_amm} payout is ${div_payout}\n")

                    #creates the string for the player that will be displayed in the popup window for the amount of the payout to receive
                    msg = str(f"{player}'s payout is ${div_payout}\n")
                    #extends the ongoing list of payout messages
                    amm_payable.extend(msg)
                    
                    #creates the new player info that will be added to the database. the only values that are changed are the recent modifier, the new amount of cash held by the player and the new net worth
                    new_player_info = [None,player_info[1]+1,player_info[2],new_cash]+player_info[4:10]+[player_info[10]+div_payout]
                    #adds the new player entry to the database 
                    cursor.execute("INSERT INTO player_info VALUES (?,?,?,?,?,?,?,?,?,?,?)", (new_player_info))
                    connection.commit()

                #creates the message for the popup window as the combination of all the messages from the different players
                popup_msg = ''.join([str(i) for i in amm_payable])
                #makes the popup with the message created above
                sg.popup(popup_msg, title='Dividend Payout')

    # for key in values:
    #     roll_window[key].update(value=False)