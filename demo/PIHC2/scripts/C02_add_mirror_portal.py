# ======================================= #
# ==== CHAPTER 2: Add Mirror Portals ==== #
# ======================================= #
# %%
# Sometimes writing some code may be necessary~
# The PIHC mod has mirror portals as a feature, so we write some code to support it.
from hoi4dev import *
import itertools
import pandas as pd
MIRROR_PROVINCES = [
    4359, # Foreverfree Forest
    14927, # Storm King Island
    1133, # Dragonland
    15080, # Yaks and Reindeers
    5800, # Cloud Sea
    5772, # Windigo
    3688, # Crystal Empire
    15094, # Tartarus
]

# %%
def AddMirrorPortals():
    adjs = pd.read_csv(F("map/adjacencies_backup.csv"), sep=';')
    adjs = adjs.drop(adjs.tail(1).index)
    for s, t in itertools.permutations(MIRROR_PROVINCES, 2):
        new_row = pd.DataFrame([[s, t, 'sea', s, -1, -1, -1, -1, '', 'MirrorPortal']], columns=adjs.columns)
        adjs = pd.concat([adjs, new_row], ignore_index=True)
    adjs.to_csv(F("map/adjacencies.csv"), sep=';', index=False, lineterminator='\r\n')
    with open(F("map/adjacencies.csv"), 'a') as f:
        f.write('-1;-1;;-1;-1;-1;-1;-1;-1') 
        
    provs = pd.read_csv(F("map/definition_backup.csv"), sep=';', header=None)
    provs[5] = provs[5].astype('str')
    for s in MIRROR_PROVINCES:
        for i, r in provs.iterrows():
            provs.at[i, 5] = r[5].lower()
    for s in MIRROR_PROVINCES:
        for i, r in provs.iterrows():
            if r[0] == s:
                provs.at[i, 6] = 'mirrors_terrain'
    provs.to_csv(F("map/definition.csv"), sep=';', index=False, header=False, lineterminator='\r\n')

# %%
AddMirrorPortals()

# The Mirror portals come with a new terrain, it is contained in the `resources/copies/data/common/terrain` folder.