from pyheaven import *

import os
os.environ['MAGICK_HOME'] = '/opt/homebrew/opt/imagemagick'
os.environ['PATH'] = f"{os.environ['MAGICK_HOME']}/bin:{os.environ['PATH']}"

from copy import deepcopy
