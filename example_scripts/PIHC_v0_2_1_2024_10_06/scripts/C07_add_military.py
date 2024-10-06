# ================================= #
# ==== CHAPTER 7: Add Military ==== #
# ================================= #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# First, we manually set up the unit types and sub unit types.
# They are included in:
# - `resources/copies/data/common/units/cannon.json`.
# - `resources/copies/data/common/units/infantry.json`.
# - `resources/copies/data/common/units/tank.json`.
# - `resources/copies/data/common/units_tags/00_categories.json`.
# Their localisation at:
# - `resources/copies/localisation/pihc_units_l_simp_chinese.yml`.
# Their gfx images at:
# - `resources/copies/gfx/interface/counters/`.
# Now we need to register the gfxs:
gfxs = pjoin("resources", "copies", "gfx", "interface", "counters"); data = []
for file in [f for f in ListFiles(pjoin(gfxs, "divisions_large")) if f.endswith(".dds")]:
    tag = file[5:-9]
    data.append({
        "spriteType": {'name': f'GFX_unit_{tag}_icon_medium', 'textureFile': f'gfx/interface/counters/divisions_large/{file}', 'noOfFrames': 2},
    })
    data.append({
        "spriteType": {'name': f'GFX_unit_{tag}_icon_medium_white', 'textureFile': f'gfx/interface/counters/divisions_small/onmap_{file}', 'noOfFrames': 2},
    })
    data.append({
        "spriteType": {'name': f'GFX_unit_{tag}_icon_small', 'textureFile': f'gfx/interface/counters/divisions_small/onmap_{file}', 'legacy_lazy_load': False},
    })
SaveJson({'spriteTypes':merge_dicts(data,d=True)}, F(pjoin("data", "interface", "PIHC_subuniticons.json")), indent=4)

# %%
# Now we add the archetypes from the files.
for archetype in TQDM(ListFolders(pjoin("resources","equipments","archetypes")), desc='Building archetypes...'):
    path = pjoin("resources", "equipments", "archetypes", archetype)
    AddArchetype(path, translate=False)

# %%
# Let's add all equipments. The resources of the equipments are located in `resources/equipments/equipments`.
AddEquipments(pjoin("resources","equipments","equipments"), translate=False, debug=False)

# Let's add all modules. The resources of the modules are located in `resources/equipments/modules`.
AddModules(module_type='tank' , path=pjoin("resources","equipments","modules","tank" ), translate=False)
AddModules(module_type='plane', path=pjoin("resources","equipments","modules","plane"), translate=False)

# Before adding technologies, duplicate for nsb, mtg and bba.
for tech in TQDM(ListFolders(pjoin("resources","technologies")), desc='Duplicating technologies...'):
    path = pjoin("resources", "technologies", tech)
    category = LoadJson(pjoin(path, "info.json"))['category']
    if category == 'armour':
        new_category = 'nsb_armour'; prefix = 'NSB_'; keyword = "TANK_"
    elif category == 'naval':
        new_category = 'mtgnaval'; prefix = 'MTG_'; keyword = "SHIP_"
    elif category == 'air_techs':
        new_category = 'bba_air_techs'; prefix = 'BBA_'; keyword = "AIR_"
    else:
        new_category = None; prefix = None
    if new_category:
        new_tech = prefix + tech
        CopyFolder(path, pjoin("resources", "technologies", new_tech), rm=True)
        data = LoadJson(pjoin("resources", "technologies", new_tech, "info.json"))
        data['category'] = new_category
        for path in dup_gen('path'):
            if path in data:
                if "leads_to_tech" in data[path]:
                    assert (data[path]["leads_to_tech"].startswith("TECHNOLOGY_")), f"leads_to_tech should start with TECHNOLOGY_ in {path}"
                    data[path]["leads_to_tech"] = "TECHNOLOGY_" + prefix + data[path]["leads_to_tech"][11:]
            else:
                break
        
        if 'dependencies' in data:
            data['dependencies'] = {
                (("TECHNOLOGY_"+prefix+k[11:]) if k.startswith("TECHNOLOGY_"+keyword) else k)
                :v for k,v in data['dependencies'].items()
            }
        
        # if tech == 'SHIP_ANCIENT':
        #     assert ('if' in data) and ('limit' in data['if']) and ('NOT' in data['if']['limit'])
        #     data['if']['limit'] = data['if']['limit']['NOT']
        
        SaveJson(data, pjoin("resources", "technologies", new_tech, "info.json"), indent=4)

# Then add all the technologies
for tech in TQDM(ListFolders(pjoin("resources","technologies")), desc='Building technologies...'):
    path = pjoin("resources", "technologies", tech)
    AddTechnology(path, translate=False)

# %%
# Next, let's get the oob of all countries, which includes: division names, division templates, and initial armies.
AddDivisions(pjoin("resources", "divisions"))

# %%
# Finally, let's add the initial armies for all countries.
N_COUNTRIES = 37
for country in TQDM(range(0,N_COUNTRIES), desc='Building countries...'):
    path = pjoin("resources", "countries", f"C{country:02d}")
    AddInitialArmy(path)