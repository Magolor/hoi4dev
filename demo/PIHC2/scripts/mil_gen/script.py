# %%
from hoi4dev import *
import pandas as pd
import math

# %%
def gender_map(x):
    return {'男': 'male', '女': 'female', '未知': 'undefined', '其他': 'undefined'}[x]
def role_map(x):
    return {
        '将军': 'corps_commander',
        '元帅': 'field_marshal',
        '海军': 'navy_leader'
    }[x]

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
def parse_mil(file, image_path="extracted", output_path="generated"):
    # read a comma separated csv from the file
    d = pd.read_csv(file, sep=',')
    d.columns = ['image', 'country', 'zh', 'en', 'gender', 'role', 'attack_skill', 'defense_skill', 'planning_skill', 'logistics_skill', 'skill', 'maneuvering_skill', 'coordination_skill', 'trait0', 'trait1', 'trait2']
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
            role_map(r['role']): {k:v for k,v in {
                "skill": int(r['skill']) if 'skill' in r else 1,
                "attack_skill": int(r['attack_skill'])              if ('attack_skill' in r        ) and (not math.isnan(r['attack_skill']))        else 1,
                "defense_skill": int(r['defense_skill'])            if ('defense_skill' in r       ) and (not math.isnan(r['defense_skill']))       else 1,
                "planning_skill": int(r['planning_skill'])          if ('planning_skill' in r      ) and (not math.isnan(r['planning_skill']))      else None,
                "logistics_skill": int(r['logistics_skill'])        if ('logistics_skill' in r     ) and (not math.isnan(r['logistics_skill']))     else None,
                "maneuvering_skill": int(r['maneuvering_skill'])    if ('maneuvering_skill' in r   ) and (not math.isnan(r['maneuvering_skill']))   else None,
                "coordination_skill": int(r['coordination_skill'])  if ('coordination_skill' in r  ) and (not math.isnan(r['coordination_skill']))  else None,
                "traits": traits_map([r['trait0'], r['trait1'], r['trait2']])
            }.items() if v is not None},
        }, pjoin(output_path, tag, "info.json"), indent=4)
        
        # deploy
        country = r['country']
        countries_path = "/Users/magolor/Documents/Paradox Interactive/Hearts of Iron IV/mod/PIHC2/resources/countries"
        data = LoadJson(pjoin(countries_path, country, "info.json"))
        assert ("recruit_character_batch" in data['history']), f"recruit_character_batch not found in {country}!"
        data['history']['recruit_character_batch'] = list(
            set(
                data['history']['recruit_character_batch'] + ["CHARACTER_"+tag]
            )
        )
        SaveJson(data, pjoin(countries_path, country, "info.json"), indent=4)
# %%
parse_mil("mil.csv", image_path="../ponies_crawler/extracted")

# %%