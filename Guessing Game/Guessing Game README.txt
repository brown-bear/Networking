*============================================================================================*
   _____                       _   _           _     _   _                 _               
  / ____|                     | | | |         | |   | \ | |               | |              
 | |  __ _   _  ___  ___ ___  | |_| |__   __ _| |_  |  \| |_   _ _ __ ___ | |__   ___ _ __ 
 | | |_ | | | |/ _ \/ __/ __| | __| '_ \ / _` | __| | . ` | | | | '_ ` _ \| '_ \ / _ \ '__|
 | |__| | |_| |  __/\__ \__ \ | |_| | | | (_| | |_  | |\  | |_| | | | | | | |_) |  __/ |   
  \_____|\__,_|\___||___/___/  \__|_| |_|\__,_|\__| |_| \_|\__,_|_| |_| |_|_.__/ \___|_|   

*============================================================================================*


KNOWN BUG:  There is no issue in connecting multiple clients to the server simultaneously, but the GUIs will hang while loading until the first window that’s opened is fully connected.  I recommend loading each window with at least the player name, then start the next instance via command line.

This game includes two files:

*** The first, game_s.py takes two command line arguments: host and timer (in seconds)

For example:  python game_s.py localhost 20

Server Tips:
1. There's no GUI for the server.
2. CTRL-C to exit cleanly.  If clients are connected, it will disconnect them after letting them know.
3. There cannot be any ties: tiebreaker goes to the player who submitted the winning guess first.
4. Server allows unlimited guesses by each player until time expires, but only the most recent guess counts.
5. Players joining in the middle of a game will start guessing during next full round.
6. Game restarts automatically.


*** The second file is game_c.py and it takes one command line argument: host

For example:  python game_c.py localhost

Client Tips:
1. When playing on localhost, you have to submit a name on the first player before instantiating a second player.
2. Guesses are unlimited for a client.
3. Close the console to exit the game.
4. If a player joins in the middle of a game, they will start play (guessing) during next full round.
5. Game restarts automatically.


