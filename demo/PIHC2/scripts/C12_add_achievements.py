# ======================================== #
# ==== CHAPTER 12: Add Achievements   ==== #
# ======================================== #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# Let's first add all achievements. The resources of the achievements are located in `resources/achievements`.
for achievement in TQDM(ListFolders("resources/achievements", ordered=True), desc='Building achievements and ribbons...'):
    path = pjoin("resources", "achievements", achievement)
    AddAchievement(unique_id="pihc_3154495198", path=path, translate=False)
# %%
