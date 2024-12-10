from .config import *

import re
from textwrap import indent

def is_ccl(file):
    if file.endswith('.txt'):
        return True
    if file.endswith('.gfx'):
        return True
    if file.endswith('.gui'):
        return True
    if file.endswith('.json'):
        return False
    raise TypeError(f"Invalid file type: \"{file}\" (must be `.txt`/`.gfx`/`.gui` or `.json`)!")

def ReadTxt(file, encoding=None):
    '''
    Read a text file.
    Args:
        file: str. Path to the text file.
        encoding: str. The encoding of the text file. Default to None, which will use the default encoding.
    Return:
        str. Content of the text file.
    '''
    encoding = load_default_encoding() if encoding is None else encoding
    with open(file, 'r', encoding=encoding, errors='ignore') as f:
        return f.read()

def SaveTxt(obj, file, encoding=None):
    '''
    Save a text file.
    Args:
        obj: any. The object to be saved, preferably a string.
        file: str. Path to the text file.
        encoding: str. The encoding of the text file. Default to None, which will use the default encoding.
    Return:
        None
    '''
    encoding = load_default_encoding() if encoding is None else encoding
    with open(file, 'w', encoding=encoding, errors='ignore') as f:
        f.write(str(obj))

def mark_ccl_string(ccl_string, patterns=[('"','"'),('#','\n')]):
    result = []
    l = ""
    inside = None
    escape = False
    for c in ccl_string:
        if escape:
            l += c; escape = False
        elif c == "\\":
            l += c; escape = True
        elif inside:
            if c == inside[1]:
                result.append((l+c,inside)); l = ""; inside = None
            else:
                l += c
        else:
            for p in patterns:
                if c == p[0]:
                    result.append((l,None)); l = c; inside = p
                    break
            else:
                l += c
    if inside and inside[1]=='\n':
        result.append((l+'\n',inside))
    else:
        result.append((l,None))
    return [w for w in result if w[0]]

def tokenize_ccl_string(ccl_string):
    sentences = mark_ccl_string(ccl_string); tokens = []
    for sentence in sentences:
        if sentence[1] == ('"', '"'):
            tokens.append(sentence[0])
        elif sentence[1] == ('#', '\n'):
            tokens.append('\n')
        else:
            # tokens.extend(re.findall(r'{|}|=|\n|-?\w+(?:[.]\w+)?|\S+', sentence[0]))
            # tokens.extend(re.findall(r"{|}|=|<|>|\n|-?\w+(?:[?.'@^:\-]\w+)*'?|\S+", sentence[0]))
            # tokens.extend(re.findall(r"{|}|=|<|>|\n|-?\w+(?:[?.'@^:\-]\w+)*%{1,2}|-?\w+(?:[?.'@^:\-]\w+)*'?|\S+", sentence[0]))
            tokens.extend(re.findall(r"{|}|=|<|>|\n|-?\w+(?:[?.'@^:\-\|]\w+)*%{1,2}|-?\w+(?:[?.'@^:\-\|]\w+)*'?|\S+", sentence[0]))
    return [w for w in tokens if w and w!='\n']

def ccl_type(t):
    if t == '§':
        return 'BUG' # There is one bug in HoI4 game file in `common/units/equipment/ship_hull_carrier.txt`
    if t.strip().startswith('#'):
        return 'COMMENT'
    if t == '=':
        return 'EQUAL'
    if t in ['<', '>']:
        return 'SYMBOL'
    if t == '{':
        return 'START'
    if t == '}':
        return 'END'
    if t.strip().lower() == 'rgb' or t.strip().lower() == 'hsv':
        return 'RGB'
    if t.strip().startswith('"') and t.strip().endswith('"'):
        return 'STRING'
    if t.strip().startswith('\'') and t.strip().endswith('\''):
        return 'STRING'
    try:
        return int(t)
    except:
        pass
    try:
        return float(t)
    except:
        pass
    return 'WORD'

def ccl_eval(t):
    k = ccl_type(t)
    c = (eval(t) if k=='STRING' else t) if isinstance(k, str) else k
    assert (k in ['WORD', 'STRING', c]), "Invalid item!"
    if k == 'WORD' and c.lower() == 'yes': return True
    if k == 'WORD' and c.lower() == 'no': return False
    return c

def ccl_repr(t):
    if isinstance(t, bool):
        return 'yes' if t else 'no'
    if not isinstance(t, str):
        return str(t)
    if t=='':
        return '""'
    if (
        ((' ' in t) or ('\t' in t) or ('\n' in t) or ("'" in t) or ('"' in t) or ("/" in t) or ('[' in t) or (']' in t))
    and (not (t.startswith('rgb') or t.startswith('hsv')))
    and (not ('^' in t))
    and (not (re.match(r'^\d{2}:\d{2}$', t) is not None))
    and (not (t.endswith('%')))
    and (not (t.startswith('[') and t.endswith(']')))
    ):
        s = repr(t)
        if s.startswith("'") and s.endswith("'"):
            return '"' + s[1:-1].replace('"','\\"').replace("\\'","'") + '"'
        return s
    return str(t)

def CCL2List(ccl_string):
    '''
    Convert a CCL (Clausewitz scripting language) string to a json list format.
    Args:
        ccl_string: str. A CCL string.
    Return:
        list. A json list format.
    
    Please pay attention to the behavior of this function:
    1. Assignments will be converted to dictionaries. For example, `research_speed_factor = 0.5` will be converted to `{"research_speed_factor": 0.5}`.
    2. Comparisons will be converted to dictionary keys. For example, `value > 3` will be converted to `{"value > 3": None}`.
    3. Keys and values are almost always (I'm not so sure) evaluated. For example, `has_dlc = "Together for Victory"` will be converted to `{"has_dlc": "Together for Victory"}` instead of `{"has_dlc": "\\"Together for Victory\\""}`. And `value = 3` will be converted to `{"value": 3}` instead of `{"value": "3"}`.
    4. Boolean values are evaluated. For example, `is_ai = yes` will be converted to `{"is_ai": True}` instead of `{"is_ai": "yes"}. (So it is probably not recommended to use `yes` or `no` as keys)
    5. Comments will be ignored. For example, `# This is a comment` will be ignored.
    6. Duplicated keys does not have an impact as the converted target is a list. For example, `tag = USA` and `tag = GER` simultaneously will be converted to `[{"tag": "USA"}, {"tag": "GER"}]`.
    7. Lists are preserved. For example, `add_ideas = { my_idea_1 my_idea_2 }` will be converted to `{"add_ideas": ["my_idea_1", "my_idea_2"]}`.
    
    This function is highly suspicious in terms of robustness. Please report any bugs you find.
    '''
    tokens = tokenize_ccl_string(ccl_string)
    stack = [list()]
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if ccl_type(token) == 'BUG':
            i += 1; continue
        if ccl_type(token) == 'RGB':
            assert (i+1<len(tokens) and ccl_type(tokens[i+1])=='START'), "Invalid `RGB` type!"
            j = i+1
            while ccl_type(tokens[j])!='END':
                j += 1
            value = ' '.join([token.strip().lower()] + tokens[i+1:j+1])
            i = j+1
            op = stack.pop()
            key = ccl_eval(stack.pop())
            assert (ccl_type(op)=='EQUAL'), "Only assignment can have an rgb as right value!"
            stack[-1].append({key: value})
            continue
        if stack[-1] in ['=', '<', '>']:
            op = stack.pop()
            key = ccl_eval(stack.pop())
            if ccl_type(token) == 'START':
                assert (op == '='), "Only assignment can have a dictionary as right value!"
                stack[-1].append({key: list()})
                stack.append(stack[-1][-1][key])
            else:
                if ccl_type(op)=='EQUAL':
                    stack[-1].append({key: ccl_eval(token)})
                else:
                    stack[-1].append({' '.join([key, op, token]): None})
        elif ccl_type(token) == 'END':
            l = list()
            while not isinstance(stack[-1], list):
                l.append(ccl_eval(stack.pop()))
            stack[-1].extend(l[::-1])
            stack.pop()
        elif ccl_type(token) == 'START':
            stack[-1].append(list())
            stack.append(stack[-1][-1])
        else:
            stack.append(token)
        i += 1
    assert (len(stack) == 1), "Invalid CCL!"
    return stack[0]

def CCLList2Dict(ccl_list):
    '''
    Convert a json list format (generated by `CCL2List`) to a dictionary format for ease of edit.
    Args:
        ccl_list: list. A json list format.
    Return:
        dict. A json dict format.
    
    Please pay attention to the behavior of this function:
    0. Please refer to the documentation of `CCL2List` for the definition of json list format.
    1. Duplicated keys will be appended with "__D" and the number of duplications. For example, `[{"tag": "USA"}, {"tag": "GER"}, {"tag": "SOV"}]` will be converted to `{"tag": "USA", "tag__D1": "GER", "tag__D2": "SOV"}`.
    2. Each item/domain is preassumed to be a list, unless it contains a dictionary. Mixing list and dictionary leads to an error. For example, `["states": [1, 2, 3]]` will be unchanged. But `["limit": [{"tag": "USA"}, {"tag": "GER"}, {"tag": "SOV"}]]` will be converted to `{"limit": {"tag": "USA", "tag__D1": "GER", "tag__D2": "SOV"}}`. To my knowledge, it is illegal to produce expressions like `["states": [1, 2, 3, {"tag": "USA"}]]`. Please report if you believe otherwise.
    
    This function is highly suspicious in terms of robustness. Please report any bugs you find.
    '''
    all_list = True
    for i, item in enumerate(ccl_list):
        if isinstance(item, dict):
            for k, v in item.items():
                if isinstance(v, list):
                    item[k] = CCLList2Dict(v)
            all_list = False
        elif isinstance(item, list):
            ccl_list[i] = CCLList2Dict(item)
    if not all_list:
        converted = {}
        for i, item in enumerate(ccl_list):
            assert (isinstance(item, dict) or isinstance(item, str)), "Invalid CCL with mixed list and dictionary!"
            if isinstance(item, str):
                converted[find_dup(item, converted)] = None
            else:
                for k, v in item.items():
                    converted[find_dup(k, converted)] = v
        return converted
    else:
        return ccl_list

def CCL2Dict(ccl_string):
    '''
    Convert a CCL (Clausewitz scripting language) string to a json dict format.
    Args:
        ccl_string: str. A CCL string.
    Return:
        dict. A json dict format.
    
    Please refer to the documentation of `CCL2List` and `CCLList2Dict` for the behavior of this function.
    
    This function is highly suspicious in terms of robustness. Please report any bugs you find.
    '''
    return CCLList2Dict(CCL2List(ccl_string))

def CCLDict2List(ccl_dict):
    '''
    Convert a json dict format (generated by `CCL2Dict` or `CCLList2Dict`) to a list format.
    Args:
        ccl_dict: Dict. A json dict format.
    Return:
        list. A json list format.
    
    Please pay attention to the behavior of this function:
    1. Duplicated keys with "__D" will be merged to the same key. For example, `{"tag": "USA", "tag__D1": "GER", "tag__D2": "SOV"}` will be converted to `[{"tag": "USA"}, {"tag": "GER"}, {"tag": "SOV"}]`.
    2. Values will not be modified whatsoever.
    3. (sus) Nested lists may be processed incorrectly.
    '''
    if isinstance(ccl_dict, list):
        assert (ccl_dict == list()), "The input should be a dictionary unless it is an empty list!"
        return list()
    ccl_list = list()
    for k, v in ccl_dict.items():
        key = find_ori(str(k))
        if isinstance(v, dict):
            ccl_list.append({key: CCLDict2List(v)})
        elif isinstance(v, list):
            new_list = list()
            for item in v:
                if isinstance(item, dict):
                    new_list.append(CCLDict2List(item))
                    # new_list.append({key: CCLDict2List(item)})
                else:
                    new_list.append(item)
            ccl_list.append({key: new_list})
        else:
            ccl_list.append({key: v})
    return ccl_list

def List2CCL(ccl_list, tab2space=4):
    '''
    Convert a json list format (generated by `CCL2List` or `CCLDict2List`) to a CCL (Clausewitz scripting language) string.
    Args:
        ccl_list: list. A json list format.
        tab2space: int. Tab size. Negative value means using `'\\t'` as tabs.
    Return:
        str. A CCL string.
    
    Please pay attention to the behavior of this function:
    1. Strings will be represented as non-quoted strings unless it contains `'\\t'`, `'\\n'`, or `' '`. For example, `{"tag": "USA"}` will be converted to `tag = USA` instead of `tag = "USA"`. But `{"has_dlc": "Together for Victory"}` will be converted to `has_dlc = "Together for Victory"` instead of `has_dlc = Together for Victory`.
    2. Boolean values will be represented as `yes` or `no`. For example, `{"is_ai": True}` will be converted to `is_ai = yes` instead of `is_ai = True`.
    3. Values will be represented as values instead of strings. For example, `{"value": 3}` will be converted to `value = 3` instead of `value = "3"`.
    4. Items with `None` values will be represented as keys. For example, `{"value": None}` will be converted to `value` instead of `value = None`.
    5. Keys starting with "//" will be ignored. For example, `{"// This is a comment": None}` will be ignored.
    
    This function is highly suspicious in terms of robustness. Please report any bugs you find.
    '''
    values = []
    for item in ccl_list:
        if isinstance(item, dict):
            for k, v in item.items():
                if k.startswith('//'):
                    continue
                if isinstance(v, list):
                    values.append(f"{ccl_repr(k)}" + " = {\n" + indent(List2CCL(v), (tab2space*' ') if tab2space>=0 else '\t')  + "\n}")
                elif v is None:
                    values.append(f"{k}")
                else:
                    values.append(f"{ccl_repr(k)}" + " = " + f"{ccl_repr(v)}")
        elif isinstance(item, list):
            values.append("{\n" + indent(List2CCL(item), (tab2space*' ') if tab2space>=0 else '\t')  + "\n}")
        elif isinstance(item, str) and item.startswith('//'):
            continue
        else:
            values.append(f"{ccl_repr(item)}")
    return "\n".join(values)

def Dict2CCL(ccl_dict):
    '''
    Convert a json dict format (generated by `CCL2Dict` or `CCLList2Dict`) to a CCL (Clausewitz scripting language) string.
    Args:
        ccl_dict: Dict. A json dict format.
    Return:
        str. A CCL string.
    
    Please refer to the documentation of `CCLDict2List` and `List2CCL` for the behavior of this function.
    
    This function is highly suspicious in terms of robustness. Please report any bugs you find.
    '''
    return List2CCL(CCLDict2List(ccl_dict))

def CCLConvert(src_path, tgt_path):
    '''
    Convert files from source to target regardless of the file type (CCL or a json dict).
    Args:
        src_path: str. Path to the source file.
        tgt_path: str. Path to the target file.
    Return:
        str. tgt_path.
    '''
    CreateFile(tgt_path)
    if (is_ccl(src_path)) and (is_ccl(tgt_path)):
        CopyFile(src_path, tgt_path); return tgt_path
    if (not is_ccl(src_path)) and (not is_ccl(tgt_path)):
        SaveJson(LoadJson(src_path), tgt_path, indent=4); return tgt_path
    if (is_ccl(src_path)) and (not is_ccl(tgt_path)):
        assert (ExistFile(src_path)), f"File not found: \"{src_path}\"!"
        ccl_string = ReadTxt(src_path)
        SaveJson(CCL2Dict(ccl_string), tgt_path, indent=4); return tgt_path
    if (not is_ccl(src_path)) and (is_ccl(tgt_path)):
        SaveTxt(Dict2CCL(LoadJson(src_path)), tgt_path); return tgt_path

def CCLConvertBatch(src_path, tgt_path, format='json'):
    '''
    Convert all files from source directory to target directory regardless of the file type (CCL or a json dict).
    Args:
        src_path: str. Path to the source directory.
        tgt_path: str. Path to the target directory.
        format: str. Only 'json' or CCL: 'txt'/'gfx'/'gui'.
    Return:
        List[str]. List of converted file paths.
    '''
    return [CCLConvert(pjoin(src_path, f), AsFormat(pjoin(tgt_path, f), format)) for f in ListFiles(src_path)]

def Edit(file, dict, d=False, clear=True):
    '''
    Edit a CCL/json file by merging it with a dictionary.
    Args:
        file: str. Path to the CCL/json file.
        dict: Dict. A json dict format.
        d: bool. If True, identical keys will be duplicated.
        clear: bool. If True, the original file will be cleared before editing.
    Return:
        None
    '''
    if d:
        clear = False
    if is_ccl(file):
        SaveTxt(Dict2CCL(merge_dicts([{} if clear or not ExistFile(file) else CCL2Dict(ReadTxt(file)), dict], d=d)), file)
    else:
        SaveJson(merge_dicts([{} if clear or not ExistFile(file) else LoadJson(file), dict], d=d), file, indent=4)