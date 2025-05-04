__all__ = [
    "yml_from_dict", "yml_to_dict",
    "load_yml", "save_yml",
    "loc_from_dict", "loc_to_dict",
    "load_loc", "save_loc",
]

from ..base import *
import re
from collections import defaultdict

def yml_from_dict(data:Dict) -> Dict:
    """
    Convert a dictionary to a HoI4 YML string.
    Args:
        data (dict): The dictionary to convert.
    Returns:
        Dict: The HoI4 YML string for each language.
    """
    return {
        lang: (
            f"l_{SUPPORTED_LANGUAGES[lang]['hoi4']}:\n"+(
                "\n".join(
                    f"  {repr(key)}: {dumps_json(str(value))}"
                    for key, value in data.items()
                )
            )
        )
        for lang in SUPPORTED_LANGUAGES
    }

def yml_to_dict(yml:str) -> Dict:
    """
    Convert a HoI4 YML string to a dictionary.
    Args:
        data (dict): The HoI4 YML string to convert.
    Returns:
        Dict: The dictionary for each language.
    """
    data = defaultdict(dict)
    lang = DEFAULT_LANGUAGE
    for line in yml.splitlines():
        if line.strip().startswith('#'):
            continue
        key, value_ver = [x.strip() for x in line.split(":", 1)]
        if (key.startswith("l_")) and (value==""):
            lang = {v['hoi4']:l for l,v in SUPPORTED_LANGUAGES.items()}.get(key[2:], lang)
        pattern = r"(?:(\d+))?\s*(.*)$"
        match = re.match(pattern, value_ver)
        try:
            value = loads_json((match.group(2) if match.group(2) else match.group(1)).strip())
        except Exception as e:
            raise ValueError(f"Error parsing value '{value}' for key '{key}': {e}")
        data[key] = value
    return data

def load_yml(path:str) -> str:
    """
    Load a HoI4 YML file.
    Args:
        path (str): The path to the YML file.
    Returns:
        str: The YML string.
    """
    return load_txt(path, encoding="utf-8-sig")

def save_yml(content:str, path:str):
    """
    Save a dictionary to a HoI4 YML file.
    Args:
        content (str): The YML string to save.
        path (str): The path to save the YML file.
    """
    save_txt(content, path=path, encoding="utf-8-sig")

def loc_from_dict(data:Dict) -> str:
    """
    Convert a dictionary to a HOI4DEV loc string.
    Args:
        data (dict): The dictionary to convert.
    Returns:
        str: The HOI4DEV loc string.
    """
    return "\n".join(
        f"[{lang}.{key}]\n{value}\n"
        for key, values in data.items()
        for lang, value in values.items()
    )

def loc_to_dict(loc:str, scope="") -> Dict:
    """
    Convert a HOI4DEV loc string to a dictionary.
    Args:
        loc (str): The HOI4DEV loc string to convert.
        scope (str): The scope to use for the keys.
    Returns:
        dict: The dictionary.
    """
    data = defaultdict(dict)
    def add(key, lang, value):
        if key and lang and value:
            if key=='@':
                key = scope
            elif key.startswith('@'):
                key = key.replace('@', scope+'_').strip('_')
            data[key][lang] = value.strip()
    lang = DEFAULT_LANGUAGE
    value = ""
    for line in loc.splitlines():
        content = line.strip()
        if content.startswith('[') and content.endswith(']') and content[3]=='.':
            _lang, _key = content[1:-1].split('.', 1)
            if _lang in SUPPORTED_LANGUAGES:
                add(lang, key, value)
                lang, key, value = _lang, _key, ""
                continue
        value += line+"\n"
    return data

def load_loc(path:str) -> str:
    """
    Load a HOI4DEV loc file.
    Args:
        path (str): The path to the loc file.
    Returns:
        str: The loc string.
    """
    return load_txt(path)

def save_loc(content:str, path:str):
    """
    Save a dictionary to a HOI4DEV loc file.
    Args:
        content (str): The loc string to save.
        path (str): The path to save the loc file.
    """
    save_txt(content, path=path)
