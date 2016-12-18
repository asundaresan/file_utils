# Get information about the media 
# 

from PIL import ImageFile
from PIL import ExifTags
import os
import pickle
import base64

def get_info( filename, koi = [] ):
  try:
    im = ImageFile.Image.open( filename )
  except:
    return {}
  try:
    exif = { ExifTags.TAGS[k]: v for k, v in im._getexif().items() if k in ExifTags.TAGS }
  except:
    exif = {}
  size = list( im.size )
  size.sort
  exif["Size"] = "x".join( "%d" % x for x in size )
  exif.update( { k:"" for k in koi if k not in exif.keys() } )
  if len( koi ) > 0:
    exif2 = { k:exif[k] for k in koi if k in exif.keys() }
    return exif2
  return exif


def is_match( reference, target, verbose = 0 ):
  """ reference is a list of dicts
      target is a dict
      return True if target matches all items in any one of the reference 
  """
  for ref in reference:
    checks = list( ref[k] == target[k] for k in ref.keys() if k in target.keys() )
    if verbose > 1:
      print( "%s == %s: %s %s" % ( exif_to_string( target ), exif_to_string( ref ), all( checks ), checks ) )
    if all( checks ):
      return True 
  return False


def exif_to_string( exif, keys = ["Make", "Model", "Size"] ):
  keystr = "_".join( exif[k] for k in keys if k in exif.keys() )
  return keystr.replace( " ", "" )



def process_folder( root_folder, koi = ["Make", "Model", "Size" ], include = [], recurse = False, verbose = 0, move = False ):
  """ Get info of all image files in the folder 
  """
  root_folder = os.path.abspath( root_folder )
  db = dict()
  ignored = 0
  found = 0
  for f in os.listdir( root_folder ):
    filename = os.path.join( root_folder, f )
    if os.path.isfile( filename ):
      exif = get_info( filename, koi )
      if len( exif.keys() ) > 0:
        found += 1
        k2 = exif_to_string( exif )
        if not k2 in db.keys():
          db[k2] = { "exif": exif, "files": list() }
        db[k2]["files"].append( filename )
      else:
        ignored += 1
        if verbose > 0:
          print( "Ignoring %s" % filename )
  print( "Found %d files, ignored %d" % ( found, ignored ) )

  if verbose >= 0:
    print( "Found following classes:\n%s" % ( "\n".join( "\t%s: %d images" %
      ( key, len( val["files"] ) ) for key, val in db.iteritems() ) ) )

  if move == True:
    for key, val in db.iteritems():
      #print( "%s: %d" % ( key, len(val["files"]) ) )
      include_file = is_match( include, val["exif"] )
      if include_file:
        print( "Moving to %s: %d files" % ( key, len(val["files"]) ) )
        for src in val["files"]:
          folder = "%s/%s" % ( os.path.dirname( src ), key )
          dst = "%s/%s" % ( folder, os.path.basename( src ) )
          if not os.path.exists( folder ):
            print( "Making directory: %s" % folder )
            os.makedirs( folder )
          if os.path.exists( src ) and not os.path.exists( dst ):
            os.rename( src, dst )
            if verbose > 1:
              print( "%s -> %s" % ( src, dst ) )


import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( "folder", help="Search folder" )
    parser.add_argument( "--repickle", "-R", action="store_true", help="Force rewrite of pickle files" )
    parser.add_argument( "--verbose", "-v", action="count", help="Verbosity level" )
    args = parser.parse_args()
    print( "Searching for files in: %s" % args.folder )
    include = [ {"Model": "iPhone 4S", "Size": "3264x2448"} ]
    process_folder( args.folder, include = include, verbose = args.verbose, move = True )

