__all__ = [
    "find_ori", "find_idx",
    "dup_gen", "list_dups",
    "find_dup",
]

from ..base import *

def find_ori(key:str) -> str:
    return key.split('__D')[0] if '__D' in key else key

def find_idx(key:str) -> int:
    return int(key.split('__D')[1]) if '__D' in key else 0

def dup_gen(key:str, start:int = 0) -> Generator:
    i = start
    if i == 0:
        yield key
        i += 1
    while True:
        yield f"{key}__D{i}"
        i += 1

def list_dups(key:str, ccl_dict:Dict) -> Generator:
    for key in ccl_dict:
        if key.startswith(f"{key}__D"):
            yield key

def find_dup(key:str, ccl_dict:Dict, probe=True):
    key = find_ori(str(key))
    # Loop unwinding for performance ig
    if key not in ccl_dict: return key
    if f"{key}__D1" not in ccl_dict: return f"{key}__D1"
    if f"{key}__D2" not in ccl_dict: return f"{key}__D2"
    if f"{key}__D3" not in ccl_dict: return f"{key}__D3"
    if f"{key}__D4" not in ccl_dict: return f"{key}__D4"
    if f"{key}__D5" not in ccl_dict: return f"{key}__D5"
    if f"{key}__D6" not in ccl_dict: return f"{key}__D6"
    if f"{key}__D7" not in ccl_dict: return f"{key}__D7"
    if f"{key}__D8" not in ccl_dict: return f"{key}__D8"
    if f"{key}__D9" not in ccl_dict: return f"{key}__D9"
    if f"{key}__D10" not in ccl_dict: return f"{key}__D10"
    if f"{key}__D11" not in ccl_dict: return f"{key}__D11"
    if f"{key}__D12" not in ccl_dict: return f"{key}__D12"
    if f"{key}__D13" not in ccl_dict: return f"{key}__D13"
    if f"{key}__D14" not in ccl_dict: return f"{key}__D14"
    if f"{key}__D15" not in ccl_dict: return f"{key}__D15"
    start = 16
    if probe: # Notice that when the keys are not consecutive, this can result in unexpected indexes
        while f"{key}__D{start}" in ccl_dict:
            start *= 2
        start = max(16, start // 2 + 1)
    for key in dup_gen(key, start=start):
        if key not in ccl_dict:
            return key
