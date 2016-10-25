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

def is_match( reference, target ):
  """ reference is a list of dicts
      target is a dict
      return True if target matches all items in any one of the reference 
  """
  for ref in reference:
    checks = list( ref[k] == target[k] for k in ref.keys() if k in target.keys() )
    print( "- check = [%s]" % ','.join( "%s" % k for k in checks ) )
    if False not in checks:
      return True 
  return False


def process_folder( root_folder, koi = ["Make", "Model", "Size" ], include = [], recurse = False, verbose = 0 ):
  """ Get info of all image files in the folder 
  """
  root_folder = os.path.abspath( root_folder )
  db = dict()
  for f in os.listdir( root_folder ):
    filename = os.path.join( root_folder, f )
    if os.path.isfile( filename ):
      exif = get_info( filename, koi )
      if len( exif.keys() ) > 0:
        k2 = "(%s)" % ','.join( "%s:%s" % (k, exif[k]) for k in koi if k in exif.keys() )
        if not k2 in db.keys():
          db[k2] = { "exif": exif, "files": list() }
        db[k2]["files"].append( filename )
      else:
        print( "Ignoring %s" % filename )

  for k in db.keys():
    print( "%s: %d" % ( k, len(db[k]["files"]) ) )
    include_file = is_match( include, db[k]["exif"] )
    if include_file:
      for src in db[k]["files"]:
        folder = "%s/include" % os.path.dirname( src )
        dst = "%s/%s" % ( folder, os.path.basename( src ) )
        if not os.path.exists( folder ):
          print( "Making directory: %s" % folder )
          os.makedirs( folder )
        if os.path.exists( src ) and not os.path.exists( dst ):
          os.rename( src, dst )



