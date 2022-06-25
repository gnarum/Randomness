#!/usr/bin/python3
import sys

badChars = sys.argv
badChars.reverse()
badChars.pop()

for x in range(1,256):
    if "{:02x}".format(x) not in badChars:
        print("\\x" + "{:02x}".format(x), end='')

print("\n")
