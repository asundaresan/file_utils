#!/bin/env python 

import sys
import argparse
import file_utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( "folder", help="Search folder" )
    parser.add_argument( "folder2", help="A second search folder to comapre against" )
    parser.add_argument( "--pickle", "-P", action="store_true", help="Force rewrite of pickle files" )
    parser.add_argument( "--delete", "-D", action="store_true", help="Delete duplicates" )
    parser.add_argument( "--verbose", "-v", action="count", help="Verbosity level" )
    args = parser.parse_args()
    print( "Searching for duplicates in: %s" % args.folder )
    file_utils.hashfile_folder( args.folder, force_pickle = args.pickle, delete = args.delete, verbose = args.verbose )

        
