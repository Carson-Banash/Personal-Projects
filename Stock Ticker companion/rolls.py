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
roll_window = sg.Window('Roll Window', roll_layout, default_element_size=(12, 1), text_justification='b', finalize=True)


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
    elif event == 'Submit':
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

        #if any of the chosen variables ar None then a radio element in the window was not selected
        if ch_sec == None or ch_mod == None or ch_amm == None:
            #a popup window is displayed to the user explaining the issue
            sg.popup('Error!!\nOne of the options was not selected!!',title="ERROR")
            #goes through all the elements and sets the radios back to false
            for key in values:
                roll_window[key].update(value=False)
            continue
        
        elif ch_mod == 'up':
            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            tpl_result = cursor.fetchone()
            result = [*tpl_result]
            result[0] = None
            # print(result)

            poss = sec_key[ch_sec]

            old = result[poss]
            new = old + 10*int(ch_amm)
            if new >= 2000:
                new = 1000
                print('Rollover: High')
            result[poss] = new
            # print(result)

            cursor.execute("INSERT INTO board_info VALUES (?,?,?,?,?,?,?)", (result))
            connection.commit()

        elif ch_mod == 'down':
            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            tpl_result = cursor.fetchone()
            result = [*tpl_result]
            result[0] = None
            

            poss = sec_key[ch_sec]

            old = result[poss]
            new = old + ((10*int(ch_amm)) * -1)
            if new <= 0:
                new = 1000
                print('Rollover: Low')
            result[poss] = new
            # print(result)

            cursor.execute("INSERT INTO board_info VALUES (?,?,?,?,?,?,?)", (result))
            connection.commit()

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
                #dictionary required for getting values from the database 
                player_sec_key = {'grain':4,'ind':5,'bonds':6,'oil':7,'silver':8,'gold':9}

                #gets the current security market values
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

    for key in values:
        roll_window[key].update(value=False)