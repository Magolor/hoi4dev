# ========================================= #
# ==== CHAPTER 9: Add National Focuses ==== #
# ========================================= #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# Let's add all focus trees. The resources of the focus trees are located in `resources/focuses`.
no_focus_flush = False
for tree in TQDM(ListFolders("resources/focuses", ordered=True), desc='Building focus trees...'):
    path = pjoin("resources", "focuses", tree); tag = tree.split('_')[0]
    # PIHC wants to support a special feature that when country flag "PIHC_COUNTRY_FLAG_NO_FOCUS" is set, the country can not proceed any focus, therefore we need to add this trigger to all focuses.
    if no_focus_flush:
        for focus in ListFolders(path):
            info_path = pjoin(path, focus, "info.json")
            info = LoadJson(info_path)
            if 'available' not in info:
                info['available'] = dict()
            trigger = {
                'limit': {
                    'has_country_flag': 'PIHC_COUNTRY_FLAG_NO_FOCUS'
                },
                'custom_trigger_tooltip': {
                    'tooltip': 'PIHC_COUNTRY_FLAG_NO_FOCUS_TOOLTIP',
                    'always': 'no',
                }
            }
            for n in dup_gen('if'):
                if n not in info['available']:
                    info['available'][n] = trigger
                    break
                if ((n in info['available']) and (info['available'][n] == trigger)):
                    break
            SaveJson(info, info_path, indent=4)
    AddFocusTree(path, translate=False)