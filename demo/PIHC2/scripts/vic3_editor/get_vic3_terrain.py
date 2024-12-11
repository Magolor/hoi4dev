
# %%
from hoi4dev import *
import pandas as pd
import numpy as np
np.random.seed(42)

# %%
vic_terrains_example = ReadTxt("./province_terrains_vic.txt")
all_vic_terrains = set()
for line in vic_terrains_example.split('\n'):
    if '=' in line:
        all_vic_terrains.add(line.split('=')[1].strip('"'))
print(list(all_vic_terrains))
# ['mountain', 'forest', 'wetland', 'ocean', 'tundra', 'lakes', 'savanna', 'jungle', 'desert', 'hills', 'snow', 'plains']

# %%
color2prov = {k: int(v) for k, v in LoadJson("../../resources/copies/map/color2prov.json").items()}
prov2color = {int(v): k for k, v in color2prov.items()}
definition = pd.read_csv("../../resources/copies/map/definition.csv", sep=";", header=None)

terrains = {int(row.iloc[0]): row.iloc[6] for i, row in definition.iterrows()}

all_hoi_terrains = set(terrains.values())
print(list(all_hoi_terrains))
# ['mountain', 'forest', 'marsh', 'ocean', 'mirrors_terrain', 'lakes', 'unknown', 'jungle', 'desert', 'hills', 'urban', 'plains']
conversion_map = {
    'marsh': 'wetland',
    'mirrors_terrain': 'tundra',
    'urban': 'plains',
    'unknown': 'snow'
}
# %%
import numpy as np
from PIL import Image
if not ExistFile("unique_provs.json"):
    img = np.array(Image.open("./provinces_new.png"))
    unique_colors = [tuple(x[:3]) for x in np.unique(img.reshape(-1, img.shape[2]), axis=0).tolist()]
    unique_provs = sorted([color2prov[repr(x)] for x in unique_colors if repr(x) in color2prov])
    extra_colors = sorted([x for x in unique_colors if repr(x) not in color2prov])
    SaveJson(unique_provs, "unique_provs.json")
    SaveJson(extra_colors, "extra_colors.json")
unique_provs = set(LoadJson("unique_provs.json"))
extra_colors = [tuple(x) for x in LoadJson("extra_colors.json")]
# %%

def color2hex(color):
    r, g, b = eval(color)
    return "x"+f"{r:02x}{g:02x}{b:02x}".upper()
hex2terrain = {color2hex(color): conversion_map.get(terrains[prov_id], terrains[prov_id]) for color, prov_id in color2prov.items() if prov_id in unique_provs}
for color in extra_colors:
    hex2terrain[color2hex(repr(color))] = 'ocean'
with open("province_terrains.txt", "w") as f:
    for color, terrain in hex2terrain.items():
        f.write(f"{color}=\"{terrain}\"\n")

# %%
prov_to_state = {int(k): int(v) for k, v in LoadJson("../../resources/copies/map/prov2state.json").items()}
state_to_provs = {}
marked = set()
for prov, state in prov_to_state.items():
    if prov not in unique_provs:
        continue
    if state not in state_to_provs:
        state_to_provs[state] = []
    state_to_provs[state].append(prov)
    marked.add(prov)
SaveJson(state_to_provs, "state_to_provs.json", indent=4)
data = {}
for state_id, provs in state_to_provs.items():
    state_data = {
        "id": state_id,
        "subsistence_building": "building_subsistence_farms",
        "provinces": [
            '"'+color2hex(prov2color[x])+'"' for x in provs
        ],
        "arable_land": 2048,
        "arable_resources": [
            "bg_wheat_farms",
            "bg_livestock_ranches",
            "bg_coffee_plantations",
            "bg_cotton_plantations",
            "bg_dye_plantations",
            "bg_opium_plantations",
            "bg_tea_plantations",
            "bg_tobacco_plantations",
            "bg_silk_plantations",
            "bg_sugar_plantations",
            "bg_rye_farms",
            "bg_banana_plantations",
            "bg_vineyard_plantations",
        ],
        "capped_resources": {
            "bg_logging": 512,
            "bg_coal_mining": 256,
            "bg_sulfur_mining": 256,
            "bg_iron_mining": 256,
            "bg_lead_mining": 256,
            "bg_gold_mining": 16,
            "bg_fishing": 128,
            "bg_whaling": 32,
        },
        "resource": {
            "type": "bg_rubber",
            "undiscovered_amount": 128
        },
        "resource__D1": {
            "type": "bg_oil_extraction",
            "undiscovered_amount": 64
        }
    }
    state_data['city'] = np.random.choice(state_data['provinces'])
    state_data['farm'] = np.random.choice(state_data['provinces'])
    state_data['mine'] = np.random.choice(state_data['provinces'])
    state_data['wood'] = np.random.choice(state_data['provinces'])
    data = data | {f"STATE_{state_id}": state_data}
state_id = max(set(state_to_provs.keys()))+1
left_over_provs = unique_provs - marked
for prov in left_over_provs:
    data = data | {
        f"STATE_{state_id}": {
            "id": state_id,
            "provinces": [
                '"'+color2hex(prov2color[prov])+'"'
            ]
        }
    }
    state_id += 1

available_prov_ids = list(set(range(1,max(unique_provs)+1+5000)) - set(unique_provs))
for c, prov_id in zip(extra_colors, available_prov_ids):
    data = data | {
        f"STATE_{state_id}": {
            "id": state_id,
            "provinces": [
                '"'+color2hex(repr(c))+'"'
            ]
        }
    }
    state_id += 1

with open("states.txt", "w") as f:
    s = Dict2CCL(data)
    f.write(s.replace('"\\"', '"').replace('\\""', '"'))


# %%