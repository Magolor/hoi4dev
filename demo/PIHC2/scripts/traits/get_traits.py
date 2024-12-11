# %%
from hoi4dev import *

traits_path = "../../resources/traits/"

traits = {}
for folder in ListFolders(traits_path, ordered=True):
    data_path = pjoin(traits_path, folder, "info.json")
    data = LoadJson(data_path)
    locs_path = pjoin(traits_path, folder, "locs.txt")
    locs = ReadTxtLocs(locs_path)
    zh, en = locs['']['zh'], locs['']['en']
    traits[zh] = (data, en)

with open("traits.txt", "w", encoding='utf-8', errors='ignore') as f:
    for zh, (data, en) in traits.items():
        serialized = indent('\n'.join(str(k)+' = '+str(v) for k,v in data.items()),prefix='\t')
        f.write(f"{zh} ({en})"+"\n"+f"{serialized}"+"\n\n")
# %%
