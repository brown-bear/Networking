#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
msg=s.recv(1024)
parts=msg.split(b'\0')
rmsg=parts[:-1]
msg=[msg.decode('utf-8') for msg in rmsg]
print (msg[0])
s.close                     # Close the socket when done