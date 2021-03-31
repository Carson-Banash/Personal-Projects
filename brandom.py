from tkinter import *    
master = Tk()

# Create this method before you create the entry
def com():
    """Gets and prints the content of the entry"""
    content = entry.get()
    print(content)  

Label(master, text="Input: ").grid(row=0, sticky=W)

entry = Entry(master)
entry.grid(row=0, column=1)

# Connect the entry with the return button
Button(master, command=com(), text='press me').grid(row=1,column=0,sticky=W)

mainloop()