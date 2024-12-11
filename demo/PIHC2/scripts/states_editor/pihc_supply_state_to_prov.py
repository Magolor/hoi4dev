# %%
from hoi4dev import *

for file in TQDM(sorted([f for f in ListFiles("states") if f.endswith(".txt")], key=lambda x: int(x.split(".")[0]))):
    with open(pjoin("states", file), "r") as f:
        data = CCL2Dict(f.read())
    
    if ('buildings' in data['state']['history']) and ('supply_node' in data['state']['history']['buildings']):
        assert data['state']['history']['buildings']['supply_node'] == 1
        del data['state']['history']['buildings']['supply_node']
        vics = list()
        for key in dup_gen('victory_points'):
            if key not in data['state']['history']:
                break
            vics.append(data['state']['history'][key])
        max_vic = max(vics, key=lambda x: x[1])
        center_prov = max_vic[0]
        print(center_prov)
        data['state']['history']['buildings'][center_prov] = {'supply_node': 1}
    
    converted = Dict2CCL(data)
    with open(pjoin("converted", file), "w", encoding='utf-8', errors='ignore') as f:
        f.write(converted)

# %%
