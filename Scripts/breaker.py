#!/usr/bin/python3
import sys

# print("Length of sys.argv " + str(len(sys.argv)))

Str = ''
n = 50
def breaker():
    for i in range(0,len(Str), n):
        print( "Str = Str + " + '"' + Str[i:i+n] + '"' )

if __name__ == "__main__":
    # No argument, assuming piped input
    if len(sys.argv) < 2:
        for line in sys.stdin:
            Str = Str + line
#            print(Str)
    # Argument instead of pipe
    else:
        Str = sys.argv[1]
    if len(Str) < 1:
        print( "Usage: " + sys.argv[0] + " <String to breakup>" )
        print( "   Or: echo 'String to breakup' | " + sys.argv[0] )
        exit(1)
    breaker()
