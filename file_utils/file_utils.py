# 
# 

import os
import hashlib
import pickle
import base64

def hash_file(filename, blocksize=65536):
  """ Return SHA256 of all files in folder
  """
  hasher = hashlib.sha256()
  with open( filename, "rb" ) as fd:
    buf = fd.read(blocksize)
    while len(buf) > 0:
      hasher.update(buf)
      buf = fd.read(blocksize)
  return hasher.digest()


def hash_string(string):
  """ Return SHA256 of string 
  """
  return hashlib.sha256( string.encode() ).digest()



def move_file_to_trash( filename, trash = "/tmp" ):
  """ This will actually move to /tmp
  """
  dirname2 = "%s/%s" % ( trash, os.path.dirname( filename ) )
  filename2 = os.path.join( dirname2, os.path.basename( filename ) )
  try:
    if not os.path.exists( dirname2 ):
      os.makedirs( dirname2 )
    os.rename( filename, filename2 )
    print( "Moved %s to %s" % (filename, filename2) )
  except:
    print( "Failed to move %s to %s" % (filename, trash) )



def get_pickle_file( base_folder ):
  """
  """
  pfolder = os.path.join( os.path.expanduser( "~" ), ".pickle" )
  if not os.path.exists( pfolder ):
    print( "Creating folder %s" % pfolder )
    os.makedirs( pfolder )
  digest = hash_string( base_folder )
  digestfile = base64.urlsafe_b64encode( digest ).decode("utf-8").rstrip("=")[:16]
  return os.path.join( pfolder, digestfile )



def hashfile_folder( root_folder, force_pickle = False, delete = False, verbose = 0 ):
  """ Get SHA256 of all files in the folder 
  """
  root_folder = os.path.abspath( root_folder )
  allfiles = dict()
  uniquefiles = dict()
  for base_folder, sub_folder, file_list in os.walk(root_folder):
    data = dict()
    pfile = get_pickle_file( base_folder )
    if os.path.exists( pfile ) and not force_pickle:
      print( "%s <- %s" % ( base_folder, pfile ) )
      with open(pfile, 'rb') as handle:
        data = pickle.load(handle) 
    else:
      for f in file_list:
        filename = os.path.join( base_folder, f )
        fhash = hash_file( filename )
        data[filename] = fhash
        print( "  %s: %s" % ( f, base64.b64encode( fhash ).decode("utf-8") ) )
      print( "%s -> %s" % ( base_folder, pfile ) )
      with open(pfile, 'wb') as handle:
        pickle.dump(data, handle)
    allfiles.update( data )
    updated_folders = set()
    for (k,v) in data.items():
      unique = True
      for (k2,v2) in uniquefiles.items():
        if v == v2:
          dupes = (k,k2) if k > k2 else (k2,k)
          to_keep = dupes[0]
          to_delete = dupes[1]
          print( "remove %s (keep: %s)" % ( to_delete, to_keep ) )
          unique = False
          if delete:
            move_file_to_trash( to_delete )
            updated_folders.add( os.path.dirname( to_delete ) )
          break
      if unique:
        uniquefiles[k] = v

  """ Remove pickle files of updated folders
  """ 
  for f in updated_folders:
    pfile = get_pickle_file( f )
    if os.path.exists( pfile ):
      print( "Removing pickle file: %s" % pfile )
      os.remove( pfile )

