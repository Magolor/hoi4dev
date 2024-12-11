# ================================ #
# ==== CHAPTER 10: Add Events ==== #
# ================================ #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# Let's first add all events. The resources of the events are located in `resources/events`.
for event in TQDM(ListFolders("resources/events", ordered=True), desc='Building events...'):
    path = pjoin("resources", "events", event)
    AddEventSpace(path, translate=False)

# %%
# Then add all super events. The resources of the super events are located in `resources/superevents`.
InitSuperEvent()
for super_event in TQDM(ListFolders("resources/superevents", ordered=True), desc='Building super events...'):
    path = pjoin("resources", "superevents", super_event)
    AddSuperEvent(path, translate=False)
AddEventSpace_("SUPER"); AddEventSpace_("SUPER_NEWS")