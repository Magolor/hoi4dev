# =================================== #
# ==== CHAPTER 5: Add Characters ==== #
# =================================== #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# First add all traits. The resources of the traits are located in `resources/traits`.
for trait in TQDM(ListFolders("resources/traits"), desc='Building traits...'):
    path = pjoin("resources", "traits", trait)
    if ExistFolder(path) and ExistFile(pjoin(path,"info.json")):
        AddTrait(path, translate=False)

# %%
# Now add all characters. The resources of the characters are located in `resources/characters`.
for character in TQDM(ListFolders("resources/characters"), desc='Building characters...'):
    path = pjoin("resources", "characters", character)
    if ExistFolder(path) and ExistFile(pjoin(path,"info.json")):
        AddCharacter(path, translate=False)
