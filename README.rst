Python file utilities
=====================

``file_utils`` is a collection of python file utilities for locating duplicates when dealing with media files such as images, videos, etc. The project was borne out of my collection of image and media files of which I had several copies and I wanted to sort them. While Adobe Lightroom locates some duplicates, it misses a fair few when the file names are different.

Installation 
------------

To install using PIP::

  pip install -e . --user

Usage 
-----

The utility functions can be used to perform the following functions. Functions are analytical and will not change any file. The user is expected to write scripts to make the necessary modifications. Many operations are recursive in that sub-folders will be processed, however analysis is performed at each folder level and file properties are cached in a pickle file per folder.

Check for duplicates within a folder 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To check if there are duplicates inside a folder. The check is performed recursively.::

  python bin/check_duplicates.py folder_a 

Check if files in a folder are present in another 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For instance, if you want to make sure that all your photos in ``folder_a`` have been imported into Lightroom (``folder_b``)::

  python bin/check_duplicates.py folder_a --not-in folder_b

