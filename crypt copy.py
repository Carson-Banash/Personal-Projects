#imports the needed functions
from tkinter import *
from tkmacosx import Button #this is needed to change the colour of the buttons (mac osx bug)

#defines the encode function
def encode():
    pass

#defines the decode function
def decode():
    pass

#defines the encode window
def en_win():
    #creates the encode window and configures it
    en_window = Toplevel()
    en_window.configure(bg='black')
    en_window.title("Encoder")

    #creates the prompt for the text box
    msg_lbl = Label(en_window, text='What is the message you would like to encode?', bg='black', fg='red')
    msg_lbl.grid(row=0, column=0, columnspan=3, pady=3, sticky=W)
    msg_ent = Entry(en_window, bg='grey', fg='white', width=35)
    msg_ent.grid(row=1, column=0, columnspan=3, sticky=W)

    #creates label and entry for the page number of the book
    bkpg_lbl = Label(en_window, text='What page is the book exerpt from?', bg='black', fg='red')
    bkpg_lbl.grid(row=2, column=0, pady=3, sticky=W)
    bkpg_ent = Entry(en_window, bg='grey', fg='white')
    bkpg_ent.grid(row=3, column=0, sticky=W)

    #creates label and entry for the book message
    bk_msg_lbl = Label(en_window, text='What is the book exerpt?', bg='black', fg='red')
    bk_msg_lbl.grid(row=4, column=0, pady=3, sticky=W)
    bk_msg_ent = Entry(en_window, bg='grey', fg='white', width=35)
    bk_msg_ent.grid(row=5, column=0, columnspan=3, sticky=W)

    #added the area that the encoded message will appear
    encoded_msg = Text(en_window, bg='black', fg='white', width=45, height=8)
    encoded_msg.grid(row=6, column=0, columnspan=3, sticky=W, pady=3)

    #creates the encode button 
    encode_btn = Button(en_window, text='Encode', command=encode(), bg='black', fg='red')
    encode_btn.grid(row=7, column=0, sticky=W, pady=5)

    #creates the close window button
    close = Button(en_window, text='Close Window', command=en_window.destroy, bg='black', fg='red')
    close.grid(row=7, column=2, sticky=E, pady=5)

#defines the decode window
def dc_win():
    #creates the decode window and configures it 
    dc_window = Toplevel()
    dc_window.configure(bg='black')
    dc_window.title("Encoder")

    #creates the label and entry for the message to decode
    msg_lbl = Label(dc_window, text='What is the message you would like to decode? \n (excluding the page number)', bg='black', fg='red')
    msg_lbl.grid(row=0, column=0, columnspan=3, pady=3, sticky=W)
    msg_ent = Entry(dc_window, bg='grey', fg='white', width=35)
    msg_ent.grid(row=1, column=0, columnspan=3, sticky=W)

    #creates the label and entry for the book message
    bk_msg_lbl = Label(dc_window, text='What is the book exerpt?', bg='black', fg='red')
    bk_msg_lbl.grid(row=2, column=0, pady=3, sticky=W)
    bk_msg_ent = Entry(dc_window, bg='grey', fg='white', width=35)
    bk_msg_ent.grid(row=3, column=0, columnspan=3, sticky=W)

    #creates the decode button
    decode_btn = Button(dc_window, text='Decode', command=decode(), bg='black', fg='red')
    decode_btn.grid(row=4, column=0, sticky=W, pady=5)

    #creates the close window button
    close2 = Button(dc_window, text='Close Window', command=dc_window.destroy, bg='black', fg='red')
    close2.grid(row=4, column=2, sticky=E, pady=5)


##all of the code for the main page where you choose whether to decode or encode

#sets up and configures the main window
root = Tk()
root.title("Main Window")
root.configure(bg='black')

#the main prompt
title = Label(root, text='Welcome to the secret message encoder/decoder \n wich one would you like?', bg='black', fg='red')
title.grid(row=0, column=0, columnspan=3)

#encode button which opens the encode window
en_btn = Button(root, text="Encode", command=en_win, bg='black', fg='red')
en_btn.grid(row=1, column=0)

#decode button which opens the decode window
dc_btn = Button(root, text="Decode", command=dc_win, bg='black', fg='red')
dc_btn.grid(row=1, column=2)

#destroys the main window
ex_btn = Button(root, text="Exit", command=root.destroy, bg='black', fg='red')
ex_btn.grid(row=1, column=1)

#starts the main loop and executes the code
mainloop()
