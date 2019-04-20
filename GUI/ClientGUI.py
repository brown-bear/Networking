# Basic data entry GUI
# Programmer: Arijit Das 

from tkinter import *
import socket

#Display a message in the staus box
def DisplayMessage() :
    
    s = socket.socket()         # Create a socket object
    host = '127.0.0.1' # Get local machine name
    port = 12345                # Reserve a port for your service.
    
    s.connect((host, port))
    msg=s.recv(1024)
    parts=msg.split(b'\0')
    rmsg=parts[:-1]
    msg=[msg.decode('utf-8') for msg in rmsg]
    t1.configure(state="normal") #entry in textbox OK
    t1.insert(END,msg[0])
    t1.configure(state="disable") #making sure no entry in text box
    s.close                     # Close the socket when done

#clears all entry widgets
def ClearText() :
   t1.configure(state="normal") #entry in textbox OK
   t1.delete('1.0',END)
   t1.configure(state="disable") #making sure no entry in text box 
   



#create a Tk root widget, give you some default options on a window
root = Tk()

#create label widgets
l3=Label(root, text="Status")

#create the text widgets and y-axis scrollbars
t1 = Text(root, height=3, width=30)
s1 = Scrollbar(root)
s1.config(command=t1.yview)
t1.config(yscrollcommand=s1.set)
t1.configure(state="disable") #making sure no entry in text box 


#create the Submit/Clear buttons
b1 = Button(root,text="Connect",command=DisplayMessage)
b2 = Button(root,text="Clear",command=ClearText)

#put all widgets into the root widget using the grid layout
l3.grid(row=2)
t1.grid(row=2, column=1)
s1.grid(row=2, column=1, sticky="E")
b1.grid(row=3, column=1, sticky="W")
b2.grid(row=3, column=1, sticky="E")

#Refresh the grahics memory (refresh rate)
mainloop()