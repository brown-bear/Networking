'''
@author: Lucas Burke
Filename: game_s.py
OS: MacOS Sierra v10.12.6
Python: v3.6.3
Created on Feb 20, 2018

Source(s):  Dr. Xie's example code (echo_c.py)
https://gist.github.com/pklaus/c4c37152e261a9e9331f
http://www.techbeamers.com/python-tutorial-write-multithreaded-python-server/
https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170

This server-style Endpoint meets the requirements for the project:
1. Starts game on port 10000
2. Host is a command line option (argv[1])
3. Server picks a random number between 1 and 100
4. Server waits game_time() seconds (argv[2])
5. Server compares all guesses to determine the winner (with tie-handling built-in)
6. Server broadcasts winner to all players
7. Server restarts game automatically
'''

# Gameplay algorithms based on listed sources and previous parts of the submitted assignment

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import socketserver
import sys
import os
import time
import random

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        try:
            addresses[client] = client_address
            print("%s:%s has connected." % client_address)
            enter_name = 'Please enter your name. Type \'exit\' at anytime to quit. \n'
            client.send(enter_name.encode('utf-8'))
            time.sleep(0.3)
            follow_on = 'The game will continue when enough players have joined.'
            client.send(follow_on.encode('utf-8'))
            
            # These 'sleeps' throughout make it easier to read prompts on client console
            time.sleep(1)    
            name = client.recv(BUFSIZ).decode('utf-8')
            time.sleep(1)
            clients[client] = name  
            wait = 'Thanks %s, it will be just one moment...\n' % name
            client.send(wait.encode('utf-8'))
            time.sleep(1)              
        except: client.close()

# Start game logic for each client connected
def start_game():
    for client in clients:    
        GAME = Thread(target=run_game, args=(client,))  
        GAME.start()
 
# THE game.           
def run_game(client):  
    """Handles all game aspects for a player."""
    while True:
        try:        
            name = clients.get(client)
            time.sleep(0.5)
            welcome = '%s, welcome to the Guessing Game!\n' % name
            client.send(welcome.encode('utf-8'))
            time.sleep(0.5)
            enter_guess = 'Please enter your guess between 1 and 100 (inclusive).\n'
            client.send(enter_guess.encode('utf-8'))
            time.sleep(1)
            guess_list[name] = None   
            while True:
                try:
                    data = client.recv(BUFSIZ).decode()
                
                    if not data.isdigit():
                        NON_DIGIT = 'You did not enter a digit, try again...'
                        client.send(NON_DIGIT.encode('utf-8'))
                        data = client.recv(BUFSIZ).decode()
                        
                    elif int(data) <= 0 or int(data) >= 101:
                        OUTSIDE_RANGE = 'Guess out of range (1 to 100 inclusive), try again...'
                        client.send(OUTSIDE_RANGE.encode('utf-8'))
                        data = client.recv(BUFSIZ).decode()
                    
                    # I store the differences between the guess and actual number in a dictionary
                    num = abs(number-int(data)) 
                    diff_list[name] = num 
                    
                    # Storing the actual guess with name of user          
                    guess_list[name] = data
                    
                    # For server awareness
                    print("Incoming guess:", str(data))
                    MESSAGE = 'Guess acknowledged: '+str(data)+'\n'
                    client.send(MESSAGE.encode('utf-8'))
        
        
                except:  # Possibly client has left the game.
                    pass
        except:
                pass
        
        
# This nifty function broadcasts a message to all participants (taken from chat source listed above)            
def broadcast(msg): 
    """Broadcasts a message to all the clients."""
    for sock in clients:
        try:
            sock.send(bytes(msg))
        except:
            pass

# Game timer (takes argument from command line) and determining the winner.
def game_time():
    """Game timer, taking arg from command line."""
    
    timer = int(sys.argv[2])
    while timer > 0:
        time.sleep(1)
        timer -=1
    
    TIMESUP = "Time's up, the number is "+str(number)+'\n'
    broadcast(TIMESUP.encode('utf-8'))
    time.sleep(1)
    results = '**NOTE: Ties go to first player to submit their guess!'
    broadcast(results.encode('utf-8'))
    time.sleep(1)
    
    # First, check to see if there's guesses
    if any(diff_list.values()) is False:
        WINNER = "Nobody guessed anything, try again!"
        broadcast(WINNER.encode('utf-8'))
        time.sleep(2)
    else:
        # Winner based on closest guess
        winner = min(diff_list, key=diff_list.get) 
            
        # Then check to see if someone guessed correctly
        if 0 in diff_list.values():
            WINNER = str(winner)+" guessed the right number! \n"
            broadcast(WINNER.encode('utf-8'))
        
        # More likely, someone just guessed closest.
        else:
            WINNER = "The winner is: "+str(winner)+" with a guess of "+str(guess_list[str(winner)])+'\n'+'\n'+'\n' 
            broadcast(WINNER.encode('utf-8'))

    time.sleep(1)
    guess_list.clear()  # Clear guesses and diff_list for next game
    diff_list.clear()
    time.sleep(2)
    NEW_GAME = '********** NEW GAME **********'
    broadcast(NEW_GAME.encode('utf-8'))
  
# Throw error if command line arguments do not include host and timer setting
if len(sys.argv) < 3:
    print ("Need to provide <hostname>, e.g., localhost and/or timer in the command line!")
    exit(1)
    
# Initialize number and dictionaries for holding user/guess data:    
clients = {} # Log {connection : player name}
addresses = {}  # Log {connection : socket}
guess_list = {} # Log {player : guess}
diff_list = {} # Log {player : difference from number (determine winner)}

HOST = sys.argv[1]
PORT = 10000
BUFSIZ = 64
ADDR = (HOST, PORT)

# This runs the Server
if __name__ == "__main__":
    while True:
        try:
            SERVER = socket(AF_INET, SOCK_STREAM)
            SERVER.bind(ADDR)
            SERVER.listen()
            print("Waiting for connection...CTRL-C to kick clients and shutdown server")
            
            #  Accept players to the game
            ACCEPT_THREAD = Thread(target=accept_incoming_connections)
            ACCEPT_THREAD.start()
            while True:
                try:  
                    # If there are 2+ players...
                    if len(clients) > 1:
                        # Looping game logic...
                        while True:
                            number = random.randint(1,100)
                            # For debugging            
                            print("The random number to be guessed is: ", number) 
                            start_game()
                            TIMER = Thread(target=game_time)
                            TIMER.start()
                            TIMER.join()
                    else:
                        pass
                    
                # Handles closing the server by server admin during gameplay
                except KeyboardInterrupt:
                    print("Server EXIT: Disconnecting Clients!")
                    broadcast('exit'.encode('utf-8'))
                    time.sleep(1)
                    try:
                        sys.exit(0)  # Cleanup server for a graceful exit
                    except:
                        pass # Ignoring broken pipe errors from disconnected clients
                    finally:
                        os._exit(0)  # Obliterate anything left open
                        
        # Handles closing the server by server admin before gameplay begins
        except KeyboardInterrupt:
            print("Server EXIT: Disconnecting Clients!")
            broadcast('exit'.encode('utf-8'))
            time.sleep(1)
            try:
                sys.exit(0)  # Cleanup buffers for a graceful exit
            except:
                pass # Ignoring broken pipe errors from disconnected clients
            finally:
                os._exit(0)  # Obliterate anything left open