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
    key = find_ori(str(key))
    for key in dup_gen(key):
        if key not in ccl_dict:
            return key

def find_ori(key):
    return key.split('__D')[0] if '__D' in key else key

def find_idx(key):
    return int(key.split('__D')[1]) if '__D' in key else 0

def merge_dicts(l, d=False):
    merged = dict()
    for x in l:
        for key, value in x.items():
            if key.startswith('$'):
                key = key[1:]; skip_d = True
            else:
                skip_d = False
            if d and (not skip_d):
                merged[find_dup(key, merged)] = value
            else:
                if (key in merged) and isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key] = merge_dicts([merged[key], value], d=d)
                else:
                    merged[key] = value
    return merged

def sort_priority(key, priority_list):
    if 'OTHERS' not in priority_list:
        priority_list.append('OTHERS')
    priority_dict = {k:i-len(priority_list) for i, k in enumerate(priority_list)}
    default_order = priority_dict.get('OTHERS')
    return priority_dict.get("$"+key, priority_dict.get(find_ori(key), default_order))

def replace_list(l, pattern, target):
    replaced = list()
    for value in l:
        if isinstance(value, str):
            replaced_value = value if pattern not in value else value.replace(pattern, target)
        elif isinstance(value, dict):
            replaced_value = replace_dict(value, pattern, target)
        elif isinstance(value, list):
            replaced_value = replace_list(value, pattern, target)
        replaced.append(replaced_value)
    return replaced

def replace_dict(d, pattern, target):
    replaced = dict()
    for key, value in d.items():
        replaced_key = key if pattern not in key else key.replace(pattern, target)
        if isinstance(value, str):
            replaced_value = value if pattern not in value else value.replace(pattern, target)
        elif isinstance(value, dict):
            replaced_value = replace_dict(value, pattern, target)
        elif isinstance(value, list):
            replaced_value = replace_list(value, pattern, target)
        replaced[replaced_key] = replaced_value
    return replaced

RESOURCES_PATH = pjoin("resources")
def find_resource(name):
    return pkg_resources.resource_filename('hoi4dev', pjoin(RESOURCES_PATH, name))

ROOT_PATH = pjoin(expanduser("~"), ".hoi4dev")
CONFIG_PATH = pjoin(expanduser("~"), ".hoi4dev", "config.json")
def init_config(force=False, **kwargs):
    if force or not ExistFile(CONFIG_PATH):
        CreateFile(CONFIG_PATH)
        SaveJson(merge_dicts([{
            'HOI4_GAME_PATH': pjoin(expanduser("~"), "Library", "Application Support", "Steam", "steamapps", "common", "Hearts of Iron IV") if is_macos() else pjoin("C:", "Program Files (x86)", "Steam", "steamapps", "common", "Hearts of Iron IV"),
            'HOI4_WORKSHOP_PATH': pjoin(expanduser("~"), "Library", "Application Support", "Steam", "steamapps", "workshop", "content", "394360") if is_macos() else pjoin("C:", "Program Files (x86)", "Steam", "steamapps", "workshop", "content", "394360"),
            'HOI4_MODS_PATH': pjoin(expanduser("~"), "Documents", "Paradox Interactive", "Hearts of Iron IV", "mod"),
            'HOI4_MODS_COMPILE_PATH': pjoin(expanduser("~"), "Documents", "Paradox Interactive", "Hearts of Iron IV", "mod"),
            "CURRENT_MOD_PATH": None
        }, kwargs]), CONFIG_PATH, indent=4)
def get_config(key=None):
    config = LoadJson(CONFIG_PATH); return config if key is None else (config[key] if key in config else None)
def set_config(key, value):
    config = get_config(); config[key] = value; SaveJson(config, CONFIG_PATH, indent=4)
def F(path):
    return pjoin(get_config("CURRENT_MOD_PATH"), path)
def get_mod_config(key=None):
    config = LoadJson(F(pjoin('hoi4dev_settings', 'configs', 'config.json'))); return config if key is None else (config[key] if key in config else None)
def set_mod_config(key, value):
    config = get_mod_config(); config[key] = value; SaveJson(config, F(pjoin('hoi4dev_settings', 'configs', 'config.json')), indent=4)
def set_current_mod(path):
    set_config("CURRENT_MOD_PATH", path)

GIT_PATH = pjoin(expanduser("~"), ".hoi4dev", "gits")
def get_git_path(name):
    return pjoin(GIT_PATH, name)