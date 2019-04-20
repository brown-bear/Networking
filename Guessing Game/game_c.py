'''
@author: Lucas Burke
Filename: game_c.py
OS: MacOS Sierra v10.12.6
Python: v3.6.3
Created on Feb 20, 2018

Source(s):  Dr. Xie's example code (echo_c.py)
https://gist.github.com/pklaus/c4c37152e261a9e9331f
http://www.techbeamers.com/python-tutorial-write-multithreaded-python-server/
https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170

This client-style endpoint meets the requirements for the project:
1. GUI-based guessing game displays server prompt to guess game
2. (BONUS) Client can change guess as many times as they want before time expires
'''

# The framework for tkinter GUI is from the Medium.com link above
# Gameplay algorithms based on other listed sources and previous parts of 
# the submitted assignment

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import tkinter
import sys


def receive():
    """Handles receiving of messages from server."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode('utf-8')
            msg_list.insert(tkinter.END, msg)
            msg_list.see('end') # Keeps window scrolling to bottom
            if msg == 'exit':
                client_socket.close()
                msg_list.insert(tkinter.END, 'Server quit, closing game!')
                msg_list.see('end')
                time.sleep(2)
                top.quit()
        except OSError:  # Possibly the server has disconnected.
            break


def send(event=None):
    """Handles the sending of the Name and Guess"""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(msg.encode('utf-8'))
    if msg == "exit":
        client_socket.close()
        top.destroy()
 
def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("exit")
    send()

top = tkinter.Tk()
top.title("Guessing Game Console")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar() 
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)

# Setting up the GUI user console
msg_list = tkinter.Listbox(messages_frame, selectmode=tkinter.SINGLE)
msg_list.config(width=0)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# Sockets/connection
HOST = sys.argv[1]
PORT = 10000

BUFSIZ = 4096
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() # Starts GUI execution.

