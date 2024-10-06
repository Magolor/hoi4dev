# ================================== #
# ==== CHAPTER 4: Add Countries ==== #
# ================================== #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# PIHC has 37 countries. Let's add them all. The resources of the countries are located in `resources/countries`.
N_COUNTRIES = 37
for country in TQDM(list(range(N_COUNTRIES)), desc='Building countries...'):
    path = pjoin("resources", "countries", f"C{country:02d}")
    if ExistFolder(path) and ExistFile(pjoin(path,"info.json")):
        AddCountry(path, translate=False)

# %%
# Let's initialize the relation grid between countries. `relation_grid[A][B]` is the delta of opinion of A towards B.
relation_grid = LoadJson(pjoin("resources", "relation_grid.json"))

for src in relation_grid:
    for tgt in relation_grid[src]:
        CreateFolder(pjoin("resources", "opinions", f"{src}_{tgt}_BASE"))
        with open(pjoin("resources", "opinions", f"{src}_{tgt}_BASE", "locs.txt"), "w", encoding='utf-8', errors='ignore') as f:
            f.write(f"[zh.@]\n基础关系修正\n\n[en.@]\nBase Opinion Correction\n\n")
        SaveJson({"value": relation_grid[src][tgt]}, pjoin("resources", "opinions", f"{src}_{tgt}_BASE", "info.json"))
        Edit(F(pjoin("data","history","countries",f"{src}.json")), {
            "add_opinion_modifier": {
                "target": tgt,
                "modifier": f"OPINION_{src}_{tgt}_BASE",
            },
        }, d=True, clear=False)
for tgt in range(1,N_COUNTRIES):
    tag = f"C{tgt:02d}"
    CreateFolder(pjoin("resources", "opinions", f"C00_{tag}_BASE"))
    with open(pjoin("resources", "opinions", f"C00_{tag}_BASE", "locs.txt"), "w", encoding='utf-8', errors='ignore') as f:
        f.write(f"[zh.@]\n基础关系修正\n\n[en.@]\nBase Opinion Correction\n\n")
    SaveJson({"value": -200}, pjoin("resources", "opinions", f"C00_{tag}_BASE", "info.json"))
    Edit(F(pjoin("data","history","countries","C00.json")), {
        "add_opinion_modifier": {
            "target": tag,
            "modifier": f"OPINION_C00_{tag}_BASE",
        },
    }, d=True, clear=False)
    CreateFolder(pjoin("resources", "opinions", f"{tag}_C00_BASE"))
    with open(pjoin("resources", "opinions", f"C00_{tag}_BASE", "locs.txt"), "w", encoding='utf-8', errors='ignore') as f:
        f.write(f"[zh.@]\n基础关系修正\n\n[en.@]\nBase Opinion Correction\n\n")
    SaveJson({"value": -200}, pjoin("resources", "opinions", f"{tag}_C00_BASE", "info.json"))
    Edit(F(pjoin("data","history","countries",f"{tag}.json")), {
        "add_opinion_modifier": {
            "target": "C00",
            "modifier": f"OPINION_{tag}_C00_BASE",
        },
    }, d=True, clear=False)

# %%
# Remember to add all the opinion modifiers. The opinion modifiers are located in `resources/opinions`.
for opinion in TQDM(ListFolders(pjoin("resources","opinions")), desc='Building opinion modifiers...'):
    path = pjoin("resources", "opinions", opinion)
    AddOpinionModifier(path, translate=False)

# %%
# Here we can also add the bops of the countries. The bops are located in `resources/bops`.
for bop in TQDM(ListFolders(pjoin("resources","bops")), desc='Building bops...'):
    path = pjoin("resources", "bops", bop)
    if ExistFolder(path) and ExistFile(pjoin(path,"info.json")):
        AddBoP(path, translate=False)