# %%
from hoi4dev import *
import pandas as pd
import math

# %%
def gender_map(x):
    return {'男': 'male', '女': 'female', '未知': 'undefined'}[x]
def role_map(x):
    return {
        '政治顾问': 'political_advisor',
        '陆军指挥': 'army_chief',
        '海军指挥': 'navy_chief',
        '空军指挥': 'air_chief',
        '最高指挥': 'high_command',
        '理论家': 'theorist',
    }[x]
def ledger_map(x):
    return {
        '全部': 'all',
        '民事': 'civilian',
        '军事': 'military',
        '陆军': 'army',
        '海军': 'navy',
        '空军': 'air',
        '隐藏': 'hidden',
    }[x]
def cost_map(x):
    return int(x)
def removal_cost_map(x):
    return {'是': 350, '否': -1}[x]

# %%
def get_traits_table():
    traits_path = "/Users/magolor/Documents/Paradox Interactive/Hearts of Iron IV/mod/PIHC2/resources/traits"
    traits = ListFolders(traits_path)
    traits_table = {
        ReadTxtLocs(pjoin(traits_path, k, "locs.txt"))['']['zh']: k for k in traits
    }
    traits_table = traits_table | {
        '雷厉风行': "RUTHLESS",
        '外交蠢蛋': "DIPLOMATIC_IDIOT",
        '不善言辞': "DIPLOMATIC_IDIOT",
        '政界崇拜': "HIGH_POLITICAL_ESTEEM",
        '权术蠢蛋': "POLITICAL_IDIOT",
        '政治蠢蛋': "POLITICAL_IDIOT",
        '经济蠢蛋': "ECONOMICAL_IDIOT",
        '经济天才': "ECONOMICAL_GENIUS",
        '何不食肉糜': "SILVER_SPOON_SYNDROME",
        '不幸运马蹄铁': "HORSESHOE_UNLUCKY",
        '鬼牌': "HORSESHOE_JOKER",
        '全天候作战': "ALL_DAY_ALL_NIGHT",
        '自私': "CORRUPT",
        '恐怖的巨头': "PRINCE_OF_TERROR",
    }
    return traits_table

TRAITS = get_traits_table()
print(TRAITS)
def traits_map(X):
    traits = []
    for x in X:
        if isinstance(x, str):
            if x in TRAITS:
                traits.append("TRAIT_"+TRAITS[x])
            else:
                print(x); continue
    return list(set(traits))

# %%
def parse_adv(file, image_path="extracted", output_path="generated"):
    # read a comma separated csv from the file
    d = pd.read_csv(file, sep=',')
    d.columns = ['image', 'zh', 'en', 'gender', 'role', 'ledger', 'removable', 'cost', 'trait0', 'trait1', 'trait2']
    for r in d.to_dict('records'):
        img = ImageFind(pjoin(image_path, Prefix(r['image'])), find_default=False)
        tag = r['en'].replace(' ', '_').replace('\'','').replace('.','').upper()
        CreateFolder(pjoin(output_path, tag))
        
        # locs.txt
        CreateFile(pjoin(output_path, tag, "locs.txt"))
        with open(pjoin(output_path, tag, "locs.txt"), 'w') as f:
            f.write(f"[en.@NAME]\n{r['en']}\n[zh.@NAME]\n{r['zh']}\n\n[en.@DESC]\nTODO\n[zh.@DESC]\nTODO\n")
        
        # default.png
        CreateFolder(pjoin(output_path, tag, "portraits"))
        ImageSave(img, pjoin(output_path, tag, "portraits", "default.png"))
        
        # info
        SaveJson({
            "name": r['en'],
            "gender": gender_map(r['gender']),
            "advisor": {
                "slot": role_map(r['role']),
                "ledger": ledger_map(r['ledger']),
                "cost": cost_map(r['cost']),
                "removal_cost": removal_cost_map(r['removable']),
                "traits": traits_map([r['trait0'], r['trait1'], r['trait2']])
            }
        }, pjoin(output_path, tag, "info.json"), indent=4)
# %%
parse_adv("adv.csv", image_path="../ponies_crawler/extracted/Earth")

# %%