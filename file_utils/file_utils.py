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
  return "%s/hash.pickle" % base_folder



def filter_files( file_list, ends_with ):
  file_list2 = list()
  for f in file_list:
    valid = list( f.lower().endswith( suffix ) for suffix in ends_with )
    if True in valid:
      file_list2.append( f )
  return file_list2



def hashfile_folder( root_folder, force_pickle = False, verbose = 0,
        ends_with = [".jpg",".jpeg", ".mov", ".mp4"]):
  """ Get all folders in root_folder and hashes of files in all folders
      Hash is SHA256 
  """
  root_folder = os.path.abspath( root_folder )
  allfolders = dict()
  uniquefiles = dict()
  for base_folder, sub_folder, file_list in os.walk(root_folder):
    data = dict()
    pfile = get_pickle_file( base_folder )
    force_pickle_this = force_pickle
    file_list2 = filter_files( file_list, ends_with )
    if verbose > 1:
      print( "Filtering files in %s: %d / %d" % ( base_folder, len( file_list2 ), len( file_list ) ) )
    if os.path.exists( pfile ) and not force_pickle:
      if verbose > 0:
        print( "Reading %s" % ( pfile ) )
      with open(pfile, 'rb') as handle:
        data2 = pickle.load(handle) 
      # if files are different, then re-pickle
      for f in file_list2:
        if f not in data2.keys():
          if verbose > 0:
            print( "%s: %s not found in pickle file" % ( pfile, f ) )
          print( "Repickling %s" % base_folder )
          force_pickle_this = True
          break
        else:
          data[f] = data2[f]
      if verbose > 2:
        for k, v in data.items():
          print( "  %s: %s" % ( k, base64.b64encode( v ).decode("utf-8") ) )
    else:
      force_pickle_this = True

    if force_pickle_this:
      for f in file_list2:
        filename = os.path.join( base_folder, f )
        fhash = hash_file( filename )
        data[f] = fhash
        if verbose > 2:
          print( "  %s: %s" % ( f, base64.b64encode( fhash ).decode("utf-8") ) )
      if len( data ):
        if verbose > 0:
          print( "Writing %s" % ( pfile ) )
        with open(pfile, 'wb') as handle:
          pickle.dump(data, handle)
    allfolders[base_folder] = data
  return allfolders



def file_extension( filename ):
  filename, extension = os.path.splitext( filename )
  return extension.upper()



def find_duplicates( target_folder, force_pickle = False, move = False, verbose = 0 ):
  """ Get SHA256 of all files in the folder 
      XXX TODO do cross folder check
  """
  target_dict = hashfile_folder( target_folder, force_pickle = force_pickle, verbose = verbose )
  for folder, data in target_dict.items():
    dupl = list()
    uniq_hash = set()
    dupl_hash = set()
    stats = dict()
    for (k,v) in data.items():
      if v in uniq_hash:
        dupl.append( k )
        dupl_hash.update( { v } )
        name, extension = os.path.splitext( k )
        extension = extension.upper()
        stats[extension] = stats[extension] + 1 if extension in stats.keys() else 1
      else:
        uniq_hash.update( { v } )
    if verbose > 0 or len( dupl ) > 0:
      print( "%d duplicates / %d total in %s" % ( len( dupl ), len( data ), folder ) )
      if len( dupl ) > 0:
        print( "\n".join( "  %d of type %s" % ( v2, k2 ) for ( k2, v2 ) in stats.items() ) )
    if move:
      for h in dupl_hash:
        dupl_files = list( key for key, val in data.items() if val == h )
        dupl_files.sort()
        for i, f in enumerate( dupl_files ):
          dupl_folder = "%s/dupe%d" % ( folder, i )
          if not os.path.exists( dupl_folder ):
            os.makedirs( dupl_folder )
          f1 = "%s/%s" % ( folder, f )
          f2 = "%s/%s" % ( dupl_folder, f )
          if verbose > 1:
            print( "  %s -> %s" % ( f1, f2 ) )
          elif verbose > 0:
            print( "  %s -> %s/" % ( f, os.path.basename( dupl_folder ) ) )
          os.rename( f1, f2 )
  return 

  # look for dupes in other folders
  hashset_dict = dict()
  for f1, d1 in target_dict.items():
    hashset_dict[f1] = set( d1.values() )
    if verbose > 1:
      print( "Getting hashset for %s: %d" % ( f1, len( d1 ) ) )

  allfolders = set( target_dict.keys() )
  for f1, s1 in hashset_dict.items():
    allfolders.remove( f1 )
    if verbose > 1:
      print( "Comparing %s: %d" % ( f1, len( s1 ) ) )
    for f2 in allfolders:
      s2 = hashset_dict[f2]
      if verbose > 1:
        print( "  with %s: %d" % ( f2, len( s2 ) ) )
      dupes = s1.intersection( s2 )
      n_dupes = len( dupes )
      if n_dupes > 0 or verbose > 0:
        print( "  %d files in %s are also in %s" % ( n_dupes, f1, f2 ) )



def not_in( target_folder, reference_folder, force_pickle = False, verbose = 0 ):
  """ Look for files in target_folder that are not in reference_folder
  """
  reference_dict = hashfile_folder( reference_folder, force_pickle = force_pickle, verbose = verbose )
  reference_set = set()
  for r in reference_dict.keys():
    reference_set.update( set( reference_dict[r].values() ) )
  target_dict = hashfile_folder( target_folder, force_pickle = force_pickle, verbose = verbose )
  not_in_folder = dict()
  for t in target_dict.keys():
    not_in_folder[t] = list()
    for f,h in target_dict[t].items():
      if h not in reference_set:
        not_in_folder[t].append( f )
    not_found = len( not_in_folder[t] )
    total = len( target_dict[t] )
    if not_found > 0:
      print( "%3d / %3d files in %s not found in reference" % ( not_found, total, t ) )
    else:
      print( "%3d / %3d files in %s not found in reference" % ( 0, total, t ) )

