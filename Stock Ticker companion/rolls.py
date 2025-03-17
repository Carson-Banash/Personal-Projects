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
        #print(event, values)
        for key in values:
            if values[key] == True:
                #print(key)
                if key in sec:
                    ch_sec = key
                elif key in mod:
                    ch_mod = key
                elif key in amm:
                    ch_amm = key
                else:
                    print('ERROR!!')

        print('chosen security: '+ ch_sec +
                '\nchosen modifier: '+ ch_mod +
                '\nchosen amount: ' + ch_amm
                )    
            
        sec_key = {'grain':1,'ind':2,'bonds':3,'oil':4,'silver':5,'gold':6}
        if ch_mod == 'up':
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

            cursor.execute("SELECT * FROM board_info WHERE ID=(SELECT max(ID) FROM board_info);")
            tpl_result = cursor.fetchone()
            result = [*tpl_result]

            poss = sec_key[ch_sec]

            if result[poss] < 1000:
                print("NO DIVIDEND!")
            else:
                player_sec_key = {'grain':4,'ind':5,'bonds':6,'oil':7,'silver':8,'gold':9}
                owned_sec = ['grain','ind','bonds','oil','silver','gold']

                cursor.execute("SELECT DISTINCT name FROM player_info;")
                result = cursor.fetchall() 
                players = [item for t in result for item in t]
                print(players)
                print(ch_sec)
                amm_payable = []
                for player in players:
                    cursor.execute("SELECT * FROM player_info WHERE name = '"+player+"' AND RECENT=(SELECT max(RECENT) FROM player_info WHERE name='"+player+"');")
                    player_info = list(cursor.fetchone())
                    cash = player_info[3]

                    div_payout = int(player_info[player_sec_key[ch_sec]])*int(ch_amm)*10

                    new_cash = div_payout+cash

                    # print(f"{player}'s old cash ${cash} in addition to the payout of ${div_payout} is ${new_cash}")
                    # print(f"{player}'s amount owned {player_info[player_sec_key[ch_sec]]} changed amount {ch_amm} payout is ${div_payout}\n")

                    msg = str(f"{player}'s payout is ${div_payout}\n")
                    amm_payable.extend(msg)
                    
                    new_player_info = [None,player_info[1]+1,player_info[2],new_cash]+player_info[4:10]+[player_info[10]+div_payout]
                    cursor.execute("INSERT INTO player_info VALUES (?,?,?,?,?,?,?,?,?,?,?)", (new_player_info))
                    connection.commit()

                popup_msg = ''.join([str(i) for i in amm_payable])
                sg.popup(popup_msg, title='Dividend Payout')
                
                #TODO: get all players amount of the security and do math to figure out how much money to add to their total
                
            


    
