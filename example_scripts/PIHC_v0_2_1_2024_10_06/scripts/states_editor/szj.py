# %%
from hoi4dev import *

for file in TQDM(sorted([f for f in ListFiles("states") if f.endswith(".txt")], key=lambda x: int(x.split("-")[0]))):
    with open(pjoin("states", file), "r") as f:
        data = CCL2Dict(f.read())
    
    if data['state']['history']['owner'] == 'EQS':
        data['state']['manpower'] = data['state']['manpower'] * 3
    if data['state']['history']['owner'] == 'CHN':
        data['state']['manpower'] = data['state']['manpower'] * 3
    
    converted = Dict2CCL(data)
    with open(pjoin("converted", file), "w", encoding='utf-8', errors='ignore') as f:
        f.write(converted)

# %%
