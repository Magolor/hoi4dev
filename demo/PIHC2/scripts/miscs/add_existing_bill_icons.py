# %%
from hoi4dev import *
ideas_size = (74, 74)

# %%
source = "../../hoi4dev_settings/imgs/bills/military"
target = "../../resources/copies/gfx/interface/ideas"
CreateFolder(target)

for f in ListFiles(source):
    if f.endswith(".png"):
        img = ImageLoad(pjoin(source, f))
        img = ImageZoom(img, w=ideas_size[0], h=ideas_size[1])
        ImageSave(img, AsFormat(pjoin(target, f), "dds"), format="dds")

# %%
source = "../../hoi4dev_settings/imgs/bills/trade"
target = "../../resources/copies/gfx/interface/ideas"
CreateFolder(target)

for f in ListFiles(source):
    if f.endswith(".png"):
        img = ImageLoad(pjoin(source, f))
        img = ImageZoom(img, w=ideas_size[0], h=ideas_size[1])
        ImageSave(img, AsFormat(pjoin(target, f), "dds"), format="dds")

# %%
source = "../../hoi4dev_settings/imgs/bills/economy"
target = "../../resources/copies/gfx/interface/ideas"
CreateFolder(target)

for f in ListFiles(source):
    if f.endswith(".png"):
        img = ImageLoad(pjoin(source, f))
        img = ImageZoom(img, w=ideas_size[0], h=ideas_size[1])
        ImageSave(img, AsFormat(pjoin(target, f), "dds"), format="dds")

# %%
source = "../../hoi4dev_settings/imgs/bills/designer/default.png"
target = "../../resources/copies/gfx/interface/add_pol_idea_button.dds"
img = ImageLoad(source)
img = ImageZoom(img, w=ideas_size[0], h=ideas_size[1])
ImageSave(img, AsFormat(target, "dds"), format="dds")

# %%
