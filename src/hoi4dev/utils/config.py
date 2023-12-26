from .utils import *
import pkg_resources
from os.path import expanduser

def dup_gen(key):
    yield key
    i = 1
    while True:
        yield f"{key}__D{i}"
        i += 1

def find_dup(key, ccl_dict):
    for key in dup_gen(key):
        if key not in ccl_dict:
            return key

def find_ori(key):
    return key.split('__D')[0] if '__D' in key else key

def merge_dicts(l, d=False):
    merged = {}
    for x in l:
        for key, value in x.items():
            if key.startswith('$'):
                key = key[1:]; skip_d = True
            else:
                skip_d = False
            if d and (key in merged) and (not skip_d):
                merged[find_dup(key, merged)] = value
            else:
                if (key in merged) and isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key] = merge_dicts([merged[key], value])
                else:
                    merged[key] = value
    return merged

RESOURCES_PATH = pjoin("resources")
def find_resource(name):
    return pkg_resources.resource_filename('hoi4dev', pjoin(RESOURCES_PATH, name))

ROOT_PATH = pjoin(expanduser("~"), ".hoi4dev")
CONFIG_PATH = pjoin(expanduser("~"), ".hoi4dev", "config.json")
def init_config(**kwargs):
    CreateFile(CONFIG_PATH); SaveJson(merge_dicts([LoadJson(find_resource('configs/paths.json')), kwargs]), CONFIG_PATH, indent=4)
def get_config(key=None):
    config = LoadJson(CONFIG_PATH); return config if key is None else (config[key] if key in config else None)
def set_config(key, value):
    config = get_config(); config[key] = value; SaveJson(config, CONFIG_PATH, indent=4)
def F(path):
    return pjoin(get_config("CURRENT_MOD_PATH"), path)
def get_mod_config(key=None):
    config = LoadJson(F(pjoin('hoi4dev_settings', 'config.json'))); return config if key is None else (config[key] if key in config else None)