from .utils import *
import pkg_resources
from os.path import expanduser

def merge_dicts(l):
    merged = {}
    for d in l:
        for key, value in d.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = merge_dicts([merged[key], value])
            else:
                merged[key] = value
    return merged

RESOURCES_PATH = pjoin("resources")
def find_resource(name):
    return pkg_resources.resource_filename('seed', pjoin(RESOURCES_PATH, name))

CONFIG_PATH = pjoin(expanduser("~"), ".hoi4dev", "config.json")
def init_config(**kwargs):
    CreateFile(CONFIG_PATH); SaveJson(merge_dicts([LoadJson(find_resource('configs/default.json')), kwargs]), CONFIG_PATH, indent=4)
def get_config(key=None):
    config = LoadJson(CONFIG_PATH); return config if key is None else (config[key] if key in config else None)
def set_config(key, value):
    config = get_config(); config[key] = value; SaveJson(config, CONFIG_PATH, indent=4)