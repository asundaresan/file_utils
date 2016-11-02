#!/usr/bin/python3

import argparse
from datetime import datetime, timedelta
from gi.repository import GExiv2


def set_date_offset( filename, delta, verbose = 0 ):
  exif = GExiv2.Metadata( filename )
  date = exif.get_date_time()
  date2 = date + delta
  print( "Setting datetime for %s: %s to %s" % ( filename, date, date2 ) )
  exif.set_date_time( date2 )
  exif.save_file()

def get_timedelta( value ):
  delta = timedelta()
  for v in value.split( "," ):
    v = v.strip()
    if v.endswith( "d" ):
      delta = delta + timedelta( days = int( v.rstrip( "d" ) ) )
    elif v.endswith( "h" ):
      delta = delta + timedelta( hours = int( v.rstrip( "h" ) ) )
  return delta

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument( "images", nargs = "+", help="Images to modify" )
  parser.add_argument( "--verbose", "-v", action="count", help="Verbosity level" )
  parser.add_argument( "--increment", "-i", type = str, default = "",
    help="Increment timestamp as a CSV (E.g. 5d,7h is 5 days and 7 hours)" )
  args = parser.parse_args()

  if args.increment != None:
    delta = get_timedelta( args.increment )
    for f in args.images:
      set_date_offset( f, delta )



