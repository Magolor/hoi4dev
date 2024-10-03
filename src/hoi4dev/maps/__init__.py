from ..utils import *
from .map2graph import *
from .state_stats import *
from .map2img import *

def get_num_states():
    return len([f for f in ListFiles(F(pjoin("data","map","converted_states"))) if f.endswith('.json')])

def get_num_provs():
    return sum([len(LoadJson(F(pjoin("data","map","converted_states",f)))['state']['provinces']) for f in ListFiles(F(pjoin("data","map","converted_states"))) if f.endswith('.json')])