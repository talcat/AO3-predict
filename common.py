""" 
Talia Weiss     MLP Project     March 2013 
common.py

This File contains functions/classes that are used by a variety of scripts for
various purposes
"""

import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


