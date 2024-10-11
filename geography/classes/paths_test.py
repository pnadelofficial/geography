from pathlib import Path
import sys
import os

present_dir = Path(__file__).parent
#print(present_dir) #the parent directory of where this file is is geo/geo/classes

current_dir = os.path.dirname(os.path.abspath(__file__)) #another way of saying the above
#print(current_dir)
geo_root = os.path.dirname(os.path.dirname(current_dir)) #so this goes up two to get to geo repository's main folder
#the number of times I use os.path.dirname() depends on how far up I want to go
#print(geo_root) #so this currently works 

# if this doc/wherever I want to find direcotry is in FullProcess though I'd do:
#current_dir = os.path.dirname(os.path.abspath(__file__))
#geo_root = os.path.dirname(os.path(current_dir)) # maybe??

#some_file_path = base_dir / "config" / "config.json"