#!/bin/env python 

import sys
import argparse
import file_utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( "target", help="Search target" )
    parser.add_argument( "--pickle", "-P", action="store_true", help="Force rewrite of pickle files" )
    parser.add_argument( "--verbose", "-v", action="count", default = 0, help="Verbosity level" )
    parser.add_argument( "--not-in", "-N", type=str, default = None, help="Find files not in this folder" )
    args = parser.parse_args()
    if args.not_in != None:
      print( "Looking for files in %s that are not in %s" % ( args.not_in, args.target ) )
      file_utils.not_in( args.target, args.not_in, verbose = args.verbose )
    else:
      print( "Searching for duplicates in %s, verbose = %d" % ( args.target, args.verbose ) )
      file_utils.find_duplicates( args.target, force_pickle = args.pickle, verbose = args.verbose )

