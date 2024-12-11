# ======================================== #
# ==== CHAPTER 14: Add State Lores    ==== #
# ======================================== #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
def AddStateLore(path, translate=True):
    '''
    Add a state lore to the mod.
    Args:
        path: str. The path of the resource files of the lore. The resources should include the lore localisation and the triggers. The triggers should be an ordered list, representing `STATE_LORE_xxx_0`, `STATE_LORE_xxx_1`, etc. If there is no trigger, only the default `STATE_LORE_xxx` will be used.
        translate: bool. Whether to translate the localisation of the state lore.
    Return:
        None
    '''
    info = LoadJson(pjoin(path,"info.json"))['triggers'] if ExistFile(pjoin(path,"info.json")) else []
    tag = int(path.strip('/').split('/')[-1])
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"STATE_LORE_{tag}", translate=translate)
    
    state_lores = F(pjoin("data","common","scripted_localisation","PIHC_STATE_LORES.json"))
    if ExistFile(state_lores):
        scripted_localisation = LoadJson(state_lores)
    else:
        scripted_localisation = {
            "defined_text": {
                "name": "GetCurentStateLoreName",
            },
            "defined_text__D1": {
                "name": "GetCurentStateLoreDesc",
            },
        }
    for idx, trigger in enumerate(info):
        scripted_localisation["defined_text__D1"] = merge_dicts([scripted_localisation["defined_text__D1"],
            {"text": {"trigger": merge_dicts([{"check_variable": { "state_lore_text_state_id": f"{tag}.id" }}, trigger], d=True), "localization_key": f"STATE_LORE_{tag}_{idx}"}}
        ], d=True)
    scripted_localisation["defined_text"] = merge_dicts([scripted_localisation["defined_text"],
        {"text": {"trigger": {"check_variable": { "state_lore_text_state_id": f"{tag}.id" }}, "localization_key": f"[{tag}.GetName]"}}
    ], d=True)
    scripted_localisation["defined_text__D1"] = merge_dicts([scripted_localisation["defined_text__D1"],
        {"text": {"trigger": {"check_variable": { "state_lore_text_state_id": f"{tag}.id" }}, "localization_key": f"STATE_LORE_{tag}"}}
    ], d=True)
    SaveJson(scripted_localisation, state_lores, indent=4)
    
    on_action = F(pjoin("data","common","on_actions","PIHC_STATE_LORES.json"))
    if ExistFile(on_action):
        on_action_data = LoadJson(on_action)
    else:
        on_action_data = {
            "on_actions": {
                "on_startup": {
                    "effect": {
                        "clear_array": "global.states_with_lore"
                    }
                }
            }
        }
    on_action_data["on_actions"]["on_startup"]["effect"] = merge_dicts([on_action_data["on_actions"]["on_startup"]["effect"],
        {"add_to_array": {"global.states_with_lore": f"{tag}.id"}}
    ], d=True)
    SaveJson(on_action_data, on_action, indent=4)

# %%
# Let's first add all state lores. The resources of the state lores are located in `resources/state_lores`.
if ExistFile(pjoin("data","common","scripted_localisation","STATE_LORES.json")):
    Delete(pjoin("data","common","scripted_localisation","STATE_LORES.json"), rm=True)
if ExistFile(pjoin("data","common","on_actions","PIHC_STATE_LORES.json")):
    Delete(pjoin("data","common","on_actions","PIHC_STATE_LORES.json"), rm=True)
for lores in TQDM(ListFolders("resources/state_lores", ordered=True), desc='Building state lores...'):
    path = pjoin("resources", "state_lores", lores)
    AddStateLore(path=path, translate=False)
# %%
