from .config import *

def find_gui_scope(data, scope, func):
    for scope_alias in dup_gen(scope):
        if (scope_alias in data):
            try: 
                assert func(data[scope_alias])
                return data[scope_alias]
            except Exception as e:
                continue
        else:
            break
    
    for key, value in data.items():
        if isinstance(value, dict):
            result = find_gui_scope(value, scope, func)
            if result is not None:
                return result

    return None