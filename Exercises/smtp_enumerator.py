#!/usr/bin/python3
#-- coding: utf-8 --

import socket
import sys
import codecs

def printUsage( exitCode ):
	print("Usage: smtp_vrfy.py <username file> <IP of remote host>")
	sys.exit( exitCode )

def connectSMTP( conType ):
	# Create a socket
	global s
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Connect to the server
	global connect
	connect=s.connect((sys.argv[2],25))
	# Receive the banner
	banner = s.recv(1024)
	if( conType == 0 ):
		print( banner.decode() )

def main( ):
	global usernames 
	usernames = list()
	try:
		with open(sys.argv[1], errors='ignore') as f:
			for line in f.readlines():
				usernames.append(line[:-1])
			f.close()
	except IOError as e:
		print("Error:  file not found.")
		printUsage(1)
		sys.exit(1)
	
	connectSMTP(0)
	for username in usernames:
		# VRFY a user
		s.send(b'VRFY ' + codecs.encode(username) + b'\r\n')
		result = s.recv(1024)
		if( b'too many errors' in result ):
			connectSMTP(1)
			s.send(b'VRFY ' + codecs.encode(username) + b'\r\n')
			result = s.recv(1024)
		elif( b'User unknown' not in result ):
			print( result[:-1].decode() )

	# Close the socket
	s.close()

if __name__ == "__main__":
	if len(sys.argv) != 3:
		printUsage(0)
	else:
		main()
