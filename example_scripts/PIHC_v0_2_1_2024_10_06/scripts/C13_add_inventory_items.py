# ======================================== #
# ==== CHAPTER 13: Add Items          ==== #
# ======================================== #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# Let's first add all inventory items. The resources of the inventory items are located in `resources/inventory_items`.
from .add_inventory_items import AddInventoryItem
for item in TQDM(ListFolders("resources/inventory_items", ordered=True), desc='Building inventory items...'):
    path = pjoin("resources", "inventory_items", item)
    AddInventoryItem(path=path, translate=False)

# Add item to the inventory item list
scanner = F(pjoin("data","common","scripted_effects","PIHC_INVENTORY.json"))
scanner_data = LoadJson(scanner); scan = dict(); debug = dict()
idx_tags = sorted([(int(item.split('-')[0]), item.split('-')[1]) for item in ListFolders("resources/inventory_items")], key=lambda x:x[1], reverse=True)
for idx, tag in idx_tags + [(0, "DEFAULT")]:
    scan = merge_dicts([scan,
        {"if": {
            "limit": {
                "check_variable": {
                    "var": f"VAR_INVENTORY_ITEM_{tag}",
                    "value": 1,
                    "compare": "greater_than_or_equals",
                }
            },
            "add_to_array": {"PIHC_INVENTORY_ARRAY": idx}
        }}
    ], d=True)
    debug = merge_dicts([debug,
        {f"ADD_INVENTORY_ITEM_{tag}_1000": True}
    ], d=True)
scanner_data['INVENTORY_SCAN'] = scan
scanner_data['INVENTORY_DEBUG'] = debug
SaveJson(scanner_data, scanner, indent=4)
