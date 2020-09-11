from tkinter import *
from tkmacosx import Button

def encode():
    pass
def decode():
    pass


root = Tk()
root.title("Main Window")
root.configure(bg='black')

def en_win():
    #creates the window and configures it
    en_window = Toplevel()
    en_window.configure(bg='black')
    en_window.title("Encoder")

    #creates the prompt for the text box
    msg_lbl = Label(en_window, text='What is the message you would like to encode?', bg='black', fg='red')
    msg_lbl.grid(row=0, column=0, columnspan=3, pady=3, sticky=W)

    msg_ent = Entry(en_window, bg='grey', fg='white', width=35)
    msg_ent.grid(row=1, column=0, columnspan=3, sticky=W)

    bkpg_lbl = Label(en_window, text='What page is the book exerpt from?', bg='black', fg='red')
    bkpg_lbl.grid(row=2, column=0, pady=3, sticky=W)

    bkpg_ent = Entry(en_window, bg='grey', fg='white')
    bkpg_ent.grid(row=3, column=0, sticky=W)

    bk_msg_lbl = Label(en_window, text='What is the book exerpt?', bg='black', fg='red')
    bk_msg_lbl.grid(row=4, column=0, pady=3, sticky=W)

    bk_msg_ent = Entry(en_window, bg='grey', fg='white', width=35)
    bk_msg_ent.grid(row=5, column=0, columnspan=3, sticky=W)

    encoded_msg = Text(en_window, bg='black', fg='white', width=45, height=8)
    encoded_msg.grid(row=6, column=0, columnspan=3, sticky=W, pady=3)

    encode_btn = Button(en_window, text='Encode', command=encode(), bg='black', fg='red')
    encode_btn.grid(row=7, column=0, sticky=W, pady=5)

    #creates the close window button
    close = Button(en_window, text='Close Window', command=en_window.destroy, bg='black', fg='red')
    close.grid(row=7, column=2, sticky=E, pady=5)

def dc_win():
    
    dc_window = Toplevel()
    dc_window.configure(bg='black')
    dc_window.title("Encoder")

    msg_lbl = Label(dc_window, text='What is the message you would like to decode? \n (excluding the page number)', bg='black', fg='red')
    msg_lbl.grid(row=0, column=0, columnspan=3, pady=3, sticky=W)

    msg_ent = Entry(dc_window, bg='grey', fg='white', width=35)
    msg_ent.grid(row=1, column=0, columnspan=3, sticky=W)

    bk_msg_lbl = Label(dc_window, text='What is the book exerpt?', bg='black', fg='red')
    bk_msg_lbl.grid(row=2, column=0, pady=3, sticky=W)

    bk_msg_ent = Entry(dc_window, bg='grey', fg='white', width=35)
    bk_msg_ent.grid(row=3, column=0, columnspan=3, sticky=W)

    decode_btn = Button(dc_window, text='Decode', command=decode(), bg='black', fg='red')
    decode_btn.grid(row=4, column=0, sticky=W, pady=5)

    close2 = Button(dc_window, text='Close Window', command=dc_window.destroy, bg='black', fg='red')
    close2.grid(row=4, column=2, sticky=E, pady=5)



title = Label(root, text='Welcome to the secret message encoder/decoder \n wich one would you like?', bg='black', fg='red')
title.grid(row=0, column=0, columnspan=3)

en_btn = Button(root, text="Encode", command=en_win, bg='black', fg='red')
en_btn.grid(row=1, column=0)

dc_btn = Button(root, text="Decode", command=dc_win, bg='black', fg='red')
dc_btn.grid(row=1, column=2)

ex_btn = Button(root, text="Exit", command=root.destroy, bg='black', fg='red')
ex_btn.grid(row=1, column=1)



mainloop()
