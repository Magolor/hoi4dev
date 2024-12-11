# %%
from hoi4dev import *

TYPE_MAPPING = {
    'city': {
        'zh': '城市',
        'en': 'City',
    },
    'port': {
        'zh': '港口',
        'en': 'Port',
    },
    'mine': {
        'zh': '矿山',
        'en': 'Mine',
    },
    'farm': {
        'zh': '农场',
        'en': 'Farm',
    },
    'wood': {
        'zh': '木材',
        'en': 'Wood',
    }
}

state_names = LoadJson("../../resources/state_names.json")

locs = {}
for state_id, state_data in state_names.items():
    for type in ['city', 'port', 'mine', 'farm', 'wood']:
        locs[f'HUB_NAME_STATE_{state_id}_{type}'] = {
            'zh': state_data['chinese'] + ' - ' + TYPE_MAPPING[type]['zh'],
            'en': state_data['english'] + ' - ' + TYPE_MAPPING[type]['en'],
        }
        locs[f'HUB_DESC_STATE_{state_id}'] = {
            'zh': state_data['chinese'],
            'en': state_data['english'],
        }

SaveTxtLocs(locs, "vic3_state_names.txt")
# %%
