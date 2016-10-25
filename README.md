# ```file_utils```
```file_utils``` is a collection of python file utility functions.

## Dependencies 

## Installation 
```
pip install -e . --user
```

## Usage 

The utility functions can be used to perform a number of functions. Most functions are analytical and will not change any file. The user is expected to write scripts to make the necessary modifications. Many operations are recursive in that sub-folders will be processed, however analysis is performed at each folder level and file properties are cached in a pickle file per folder.

- Check if there are duplicates within a folder 
```
python bin/check_duplicates.py folder_a 
```
- Check if all files in a folder are present in another. For instance, if you want to make sure that all your photos in ```folder_a``` have been imported into Lightroom (```folder_b```) you may run 
```
python bin/check_duplicates.py folder_a --not-in folder_b
```

