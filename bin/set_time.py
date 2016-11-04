#!/usr/bin/python3

import argparse
from datetime import datetime, timedelta
from gi.repository import GExiv2


def get_datetime( filename ):
  exif = GExiv2.Metadata( filename )
  return exif.get_date_time()


def set_datetime( filename, dt ):
  exif = GExiv2.Metadata( filename )
  exif.set_date_time( dt )
  exif.save_file()


def set_date_offset( filename, delta, verbose = 0 ):
  date = get_datetime( filename )
  date2 = date + delta
  print( "Setting datetime for %s: %s to %s" % ( filename, date, date2 ) )
  set_datetime( filename, dt )


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
  parser.add_argument( "--decrement", "-d", type = str, default = "",
    help="Decrement timestamp as a CSV " )
  parser.add_argument( "--datetime", "-s", type = str, default = "",
    help="Set timestamp e.g. \"2014-06-03 8:21\"" )
  args = parser.parse_args()

  if args.increment != None or args.decrement != None:
    delta = get_timedelta( args.increment ) - get_timedelta( args.decrement )
    for f in args.images:
      set_date_offset( f, delta )
  elif args.datetime != "":
    try: 
      dt = datetime.strptime( arg.datetime, "%Y-%m-%d %H:%M" )
    except:
      print( "Failed to parse datetime string: %s" % args.datetime )
      print( "  E.g.: 2014-06-03 21:33" )
    finally:
      for f in args.images:
        set_datetime( f, dt )


