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

def ReadTxtLocs(path, scope="", encoding=None):
    '''
    Read localisation file.
    Args:
        path: str. Path to the localisation file.
        scope: str. The scope name of all the localisations in this file.
        encoding: str. The encoding of the localisation file. Default to None, which will use the default encoding.
    Return:
        dict. A dictionary of localisation.
    
    The localisation file is a plain text file. Special commands like `[language.key]` can set the language and key of the following lines. Key with `@` will replace `@` with the current scope name with `_` (unless ends with `@`). The lines will be stripped.
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
                key = key.replace('@', scope+'_').strip('_')
            if key not in locs:
                locs[key] = {}
            locs[key][language] = value.strip()
    encoding = load_default_encoding() if encoding is None else encoding
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        text = ""; key = None; language = None
        for line in f.readlines():
            if line.strip().startswith('[') and line.strip().endswith(']'):
                stripped_line = line.strip().strip('[]')
                if ('.' not in stripped_line) or (len(stripped_line.split('.',1)[0])!=2):
                    text += line
                else:
                    add(key, language, text); text = ""
                    language, key = stripped_line.split('.',1)
            else:
                text += line
    add(key, language, text)
    return locs

def SaveTxtLocs(locs, path, encoding=None):
    '''
    Save localisation to a plain text file.
    Args:
        locs: Dict. The localisation to save.
        path: str. The path of the localisation file.
        encoding: str. The encoding of the localisation file. Default to None, which will use the default encoding.
    Return:
        None
    '''
    encoding = load_default_encoding() if encoding is None else encoding
    with open(path, 'w', encoding=encoding, errors='ignore') as f:
        for key, loc in locs.items():
            for language, value in loc.items():
                f.write(f"[{language}.{key}]\n{value}\n")
            f.write("\n")

def ReadYmlLocs(path, encoding=None):
    '''
    Read localisation file.
    Args:
        path: str. Path to the localisation file.
        encoding: str. The encoding of the localisation file. Default to None, which will use the default encoding.
    Return:
        dict. A dictionary of localisation.
    '''
    locs = dict()
    encoding = load_default_encoding() if encoding is None else encoding
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        lang = None
        for line in f:
            if line.strip().startswith('#'):
                continue
            if lang is None:
                for k, v in LANGUAGE_MAPPING.items():
                    if f"l_{v['hoi4']}:" in line:
                        lang = k
                        break
            else:
                pattern = r'^(\w+):(?:(\d+))?\s*(.*)$'
                match = re.match(pattern, line.strip())
                if match is not None:
                    key = match.group(1)
                    value = match.group(3) if match.group(3) else match.group(2)
                    try:
                        locs[key] = {lang: eval(value.strip())}
                    except:
                        try:
                            locs[key] = {lang: eval("'"+value.strip()[1:1]+"'")}
                        except:
                            pass
    return locs

def SaveLocs(locs, name, path, replace=False, clear=True, encoding=None):
    '''
    Save localisation to separate `.yml` files.
    Args:
        locs: Dict. The localisation to save.
        name: str. The name of the localisation file (you do not need to add `_l_{language}.yml`).
        path: str. The path of the localisation folder.
        replace: str. Whether to put the localisation in the `replace` folder.
        clear: bool. Whether to clear the localisation file before saving.
        encoding: str. The encoding of the localisation file. Default to None, which will use the default encoding.
    Return:
        None
    '''
    languages = set([language for value in locs.values() for language in value.keys()])
    for language in languages:
        hoi4_lang = LANGUAGE_MAPPING[language]['hoi4']
        yml_file = pjoin(path, "replace" if replace else hoi4_lang, f"{name}_l_{hoi4_lang}.yml")
        if clear or (not ExistFile(yml_file)):
            CopyFile(F(pjoin("hoi4dev_settings", "localisations", f"empty_l_{hoi4_lang}.yml")), yml_file, rm=True)
    encoding = load_default_encoding() if encoding is None else encoding
    for key, value in locs.items():
        for language, value in value.items():
            hoi4_lang = LANGUAGE_MAPPING[language]['hoi4']
            yml_file = pjoin(path, "replace" if replace else hoi4_lang, f"{name}_l_{hoi4_lang}.yml")
            with open(yml_file, 'a', encoding=encoding, errors='ignore') as f:
                s = repr(value)
                if s.startswith("'") and s.endswith("'"):
                    s = '"' + s[1:-1].replace('"','\\"').replace("\\'","'") + '"'
                f.write("\t" + f"{key}:0 {s}\n")