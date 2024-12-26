from pyheaven import *

def ListResourceFolders(path):
    return [folder for folder in ListFolders(path, ordered=True) if not (folder.startswith('.') or folder.startswith('__'))]

import os
os.environ['MAGICK_HOME'] = '/opt/homebrew/opt/imagemagick'
os.environ['PATH'] = f"{os.environ['MAGICK_HOME']}/bin:{os.environ['PATH']}"

import platform
def is_macos():
    return platform.system() == "Darwin"
def is_windows():
    return platform.system() == "Windows"

from copy import deepcopy
from collections import defaultdict