# ======================================== #
# ==== CHAPTER 11: Add Intel Agencies ==== #
# ======================================== #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# Init the intel agencies
InitIntelAgencies()

# %%
# Let's first add all intel agencies. The resources of the intel agencies are located in `resources/intel_agencies`.
for intel_agency in TQDM(ListFolders("resources/intel_agencies", ordered=True), desc='Building intel agencies...'):
    path = pjoin("resources", "intel_agencies", intel_agency)
    AddIntelAgency(path, translate=False)