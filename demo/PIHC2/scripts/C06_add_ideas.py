# ============================== #
# ==== CHAPTER 6: Add Ideas ==== #
# ============================== #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# Let's add all ideas. The resources of the ideas are located in `resources/ideas`.
for idea in TQDM(ListFolders("resources/ideas", ordered=True), desc='Building ideas...'):
    path = pjoin("resources", "ideas", idea)
    if ExistFolder(path) and ExistFile(pjoin(path,"info.json")):
        AddIdea(path, translate=False)

# %%
# Also, category ideas require a different treatment.
for category in TQDM(ListFolders("resources/idea_categories", ordered=True), desc='Building category ideas...'):
    path = pjoin("resources", "idea_categories", category)
    if ExistFolder(path) and ExistFile(pjoin(path,"info.json")):
        AddIdeaCategory(path, translate=False)

# %%
# Static modifiers with icons
for modifier in TQDM(ListFolders("resources/modifiers", ordered=True), desc='Building static modifiers...'):
    path = pjoin("resources", "modifiers", modifier)
    if ExistFolder(path) and ExistFile(pjoin(path,"info.json")):
        AddModifier(path, translate=False)