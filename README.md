# Description

Simple tool to manipulate $PATH in order to remove redundant entries, 
change the order etc.

The idea is to have a kind of final "cleanup tool" in the profile 
beeing called at the end (after all other tools had the chance to create their usual mess).

# Files

- path_mod.py: The acutual program
- path_mod: A convience shell executor
- path_mod.profile: An example how to integrate it in a bash profile
