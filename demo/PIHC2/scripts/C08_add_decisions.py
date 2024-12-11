# ================================== #
# ==== CHAPTER 8: Add Decisions ==== #
# ================================== #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# PIHC has a core decision for every central equestria region. Let's add them.
# from scripts.central_equestria_script_legacy import gen_central_equestria_core_decisions
# gen_central_equestria_core_decisions()

# %%
# Let's add all decision categories. The resources of the decisions are located in `resources/decisions`.
for category in TQDM(ListFolders("resources/decisions", ordered=True), desc='Building decisions...'):
    path = pjoin("resources", "decisions", category)
    AddDecisionCategory(path, translate=False)