#!/usr/bin/env python 

import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( "folder", help="Search folder" )
    parser.add_argument( "--repickle", "-R", action="store_true", help="Force rewrite of pickle files" )
    parser.add_argument( "--verbose", "-v", action="count", help="Verbosity level" )
    args = parser.parse_args()
    print( "Searching for files in: %s" % args.folder )
    include = [ {"Model": "iPhone 6", "Size": "3264x2448"} ]
    image_utils.process_folder( args.folder, include = include, verbose = args.verbose )


