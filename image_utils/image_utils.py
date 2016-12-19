# Get information about the media 
# 

from PIL import ImageFile
from PIL import ExifTags
import os
import pickle
import base64
import subprocess

def run_command( command ):
  p = subprocess.Popen( command,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT )
  return iter(p.stdout.readline, b'')


def get_video_info( filename, keys = ["Model", "Make", "Size"], verbose = 0 ):
  if verbose > 0:
    print( "processing %s" % filename )
  outputfile = "/tmp/metadata.txt"
  if os.path.exists( outputfile ):
    os.remove( outputfile )
  cmd = "ffmpeg -i %s -f ffmetadata %s" % ( filename, outputfile )
  exif = {}
  for line in run_command( cmd.split() ):
    if ":" in line:
      v = line.split( ":" )
      key = v[0].strip()
      val = v[1].strip()
      if key.startswith( "Stream #0" ) and val.startswith( "0(und)" ):
        if len( v ) == 4: 
          v2 = v[3].split( ", " )
          if len( v2 ) >= 4:
            key = "size-eng" 
            val = v2[3]

      for k in keys:
        if key.startswith( k.lower() ) and key.endswith( "-eng" ):
          exif[k] = val
          if verbose > 1:
            print( "%s:%s (%s:%s)" % ( key, val, v[0].strip(), v[1].strip() ) )
  if verbose > 0:
    print( "  exif: %s" % exif )
  return exif


def get_metadata( filename, koi, verbose = 0, video_extensions = ["MOV"], image_extensions = ["JPG", "JPEG"] ):
  name, extension = os.path.splitext( filename )
  filetype = extension.upper().lstrip( "." )
  exif = {}
  if filetype in video_extensions:
    exif = get_video_info( filename, koi, verbose = verbose )
  elif filetype in image_extensions:
    exif = get_image_info( filename, koi, verbose = verbose )
  
  exif.update( {"Type": filetype } )
  return exif


def get_image_info( filename, koi, verbose = 0 ):
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


def exif_to_string( exif, keys = ["Type", "Make", "Model", "Size"] ):
  keystr = "_".join( exif[k] for k in keys if k in exif.keys() )
  return keystr.replace( " ", "" )



def move_to_subfolder( files, subfolder, verbose = 0 ):
  """ Copy files to subfolder in their respective folders,
      i.e. f is copied to dirname( f )/subfolder/basename( f )
  """
  print( "Moving %d files to %s" % ( len( files ), subfolder ) )
  for src in files:
    folder = "%s/%s" % ( os.path.dirname( src ), subfolder )
    dst = "%s/%s" % ( folder, os.path.basename( src ) )
    if not os.path.exists( folder ):
      print( "Making directory: %s" % folder )
      os.makedirs( folder )
    if os.path.exists( src ) and not os.path.exists( dst ):
      os.rename( src, dst )
      if verbose > 0:
        print( "%s -> %s" % ( src, dst ) )


def process_folder( root_folder, koi = ["Make", "Model", "Size" ], include = [], move = False, move_complement = False, recurse = False, verbose = 0 ):
  """ Get info of all image files in the folder 
  """
  root_folder = os.path.abspath( root_folder )
  db = dict()
  ignored = 0
  found = 0
  for f in os.listdir( root_folder ):
    filename = os.path.join( root_folder, f )
    if os.path.isfile( filename ):
      exif = get_metadata( filename, koi, verbose = verbose )
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
  print( "Found %d files, ignored %d (%d classes)" % ( found, ignored, len( db ) ) )

  for key, val in db.iteritems():
    selected = is_match( include, val["exif"] )
    if selected:
      if move:
        subfolder = key
        move_to_subfolder( val["files"], key, verbose )
        print( "* %s (%d files -> %s)" % ( key, len( val["files"] ), subfolder ) )
      elif move_complement:
        subfolder = "complement"
        move_to_subfolder( val["files"], subfolder, verbose )
        print( "* %s (%d files -> %s)" % ( key, len( val["files"] ), subfolder ) )
      else:
        print( "* %s (%d files)" % ( key, len( val["files"] ) ) )
    else:
      if verbose > 0:
        print( "  %s" % key )


import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( "folder", help="Search folder" )
    parser.add_argument( "--repickle", "-R", action="store_true", help="Force rewrite of pickle files" )
    parser.add_argument( "--verbose", "-v", action="count", help="Verbosity level" )
    parser.add_argument( "--move", "-m", action="store_true", help="Move selected files to folder" )
    parser.add_argument( "--move-complement", "-c", action="store_true", help="Move complement of selected files to folder" )
    args = parser.parse_args()
    print( "Searching for files in: %s" % args.folder )
    include = []
    for model in ["iPhone 4S", "iPhone 6"]:
      #include.append( {"Type": "MOV", "Model": model, "Size": "1920x1080" } )
      #include.append( {"Type": "JPG", "Model": model, "Size": "3264x2448"} )
      #include.append( {"Type": "MOV", "Model": model, "Size": "1920x1080" } )
      include.append( { "Type": "MOV", "Model": model } )
      include.append( { "Type": "JPG", "Model": model } )
    process_folder( args.folder, include = include, move = args.move,
        move_complement = args.move_complement, verbose = args.verbose )
