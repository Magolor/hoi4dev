from pyheaven import *

import os
os.environ['MAGICK_HOME'] = '/opt/homebrew/opt/imagemagick'
os.environ['PATH'] = f"{os.environ['MAGICK_HOME']}/bin:{os.environ['PATH']}"

import platform
def is_macos():
    return platform.system() == "Darwin"
def is_windows():
    return platform.system() == "Windows"

from copy import deepcopy