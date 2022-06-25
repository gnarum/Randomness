#!/usr/bin/python

import sys
import re

def main( fn ):
    fileName = fn[0]
    foundFiles = []
    with open(fileName, encoding='utf8', errors='ignore') as f:
        for line in f.readlines():
            name = re.search( '[a-zA-Z0-9\.]+\.js ', line[:-1] )
            if( name ):
                if( not ( name.group() in foundFiles ) ):
                    print("Adding file " + name.group())
                    foundFiles.append( name.group() )
        f.close()
    print( "Javascript files found:" )
    for f in foundFiles:
        print("    " + f )




if __name__ == "__main__":
    if( len(sys.argv) > 1 ):
        main(sys.argv[1:])
    else:
        print( "Usage to sift a file for .js filenames." )
        print( sys.argv[0] + " <filename>")
        sys.exit(-1)
