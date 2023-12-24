from .config import *

LANGUAGE_MAPPING = {
    'zh': {'huggingface': 'zh', 'nltk':    'chinese', 'hoi4': 'simp_chinese', 'nl': 'Simplified Chinese'},
    'en': {'huggingface': 'en', 'nltk':    'english', 'hoi4':      'english', 'nl':            'English'},
    'ru': {'huggingface': 'ru', 'nltk':    'russian', 'hoi4':      'russian', 'nl':            'Russian'},
    'de': {'huggingface': 'de', 'nltk':     'german', 'hoi4':       'german', 'nl':             'German'},
    'fr': {'huggingface': 'fr', 'nltk':     'french', 'hoi4':       'french', 'nl':             'French'},
    'es': {'huggingface': 'es', 'nltk':    'spanish', 'hoi4':      'spanish', 'nl':            'Spanish'},
    'pt': {'huggingface': 'pt', 'nltk': 'portuguese', 'hoi4':     'braz_por', 'nl':         'Portuguese'},
    'ja': {'huggingface': 'ja', 'nltk':   'japanese', 'hoi4':     'japanese', 'nl':           'Japanese'},
    'pl': {'huggingface': 'pl', 'nltk':     'polish', 'hoi4':       'polish', 'nl':             'Polish'},
}

def ReadTxtLocs(path, scope=""):
    '''
    Read localisation file.
    Args:
        path: str. Path to the localisation file.
        scope: str. The scope name of all the localisations in this file.
    Return:
        dict. A dictionary of localisation.
    
    The localisation file is a plain text file. Special commands like `[language.key]` can set the language and key of the following lines. Key started with `@` will replace `@` with the current scope name. The lines will be stripped.
    For example, under "ABC" scope:
    ```
    [en.key01]
    test1
    test2
    [zh.@key01]
    
    中文测例1
    中文测例2
    [zh.key01]
    中文测例3
    中文测例4
    ```
    will be parsed as `{'key01: {'en': 'test1\ntest2', 'zh': '中文测例3\n中文测例4'}, 'ABC_key01': {'zh': '中文测例1\n中文测例2'}}`.
    '''
    locs = {}
    def add(key, language, value):
        if key and language and value:
            if key.startswith('@'):
                key = scope+"_"+key[1:] if len(key.strip())>1 else scope
            if key not in locs:
                locs[key] = {}
            locs[key][language] = value.strip()
    with open(path, 'r', encoding='utf-8') as f:
        text = ""; key = None; language = None
        for line in f.readlines():
            if line.strip().startswith('[') and line.strip().endswith(']'):
                add(key, language, text); text = ""
                language, key = (line.split('[')[-1].split(']')[0]).split('.',1)
            else:
                text += line
    add(key, language, text)
    return locs

def SaveLocs(locs, name, path, clear=True):
    '''
    Save localisation to separate `.yml` files.
    Args:
        locs: Dict. The localisation to save.
        name: str. The name of the localisation file.
        path: str. The path of the localisation folder.
        clear: bool. Whether to clear the localisation file before saving.
    Return:
        None
    '''
    languages = set([language for value in locs.values() for language in value.keys()])
    for language in languages:
        hoi4_lang = LANGUAGE_MAPPING[language]['hoi4']
        yml_file = pjoin(path, hoi4_lang, f"{name}_l_{hoi4_lang}.yml")
        if clear or (not ExistFile(yml_file)):
            CopyFile(find_resource(f'localisations/empty_l_{hoi4_lang}.yml'), yml_file)
    for key, value in locs.items():
        for language, value in value.items():
            hoi4_lang = LANGUAGE_MAPPING[language]['hoi4']
            yml_file = pjoin(path, hoi4_lang, f"{name}_l_{hoi4_lang}.yml")
            with open(yml_file, 'a', encoding='utf-8') as f:
                s = repr(value)
                if s.startswith("'") and s.endswith("'"):
                    s = '"' + s[1:-1].replace('"','\\"') + '"'
                f.write("\t" + f"{key}:0 {s}\n")