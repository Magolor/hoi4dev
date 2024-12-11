# %%
from hoi4dev import *

for file in TQDM(sorted([f for f in ListFiles("states") if f.endswith(".txt")], key=lambda x: int(x.split(".")[0]))):
    with open(pjoin("states", file), "r") as f:
        data = CCL2Dict(f.read())
    
    data['state']['manpower'] = max(int(data['state']['manpower']) // 25, 1)
    
    converted = Dict2CCL(data)
    with open(pjoin("converted", file), "w", encoding='utf-8', errors='ignore') as f:
        f.write(converted)

# %%
