from ..utils import *
from ..translation import AddLocalisation

def AddAchievement(unique_id, path, translate=True, force=True):
    '''
    Add an achievement to the mod.
    Args:
        unique_id: str. The unique id of your entire mod.
        path: str. The path of the resource files of the achievement. The resources should include the achievement icon, the achievement definition and the localisation.
        translate: bool. Whether to translate the localisation of the achievement.
        force: bool. Whether to force the overwriting of the existing cached images.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    file_name = f"custom_achievements_{unique_id}.json"
    info = LoadJson(pjoin(path,"info.json"))
    name = info.pop('name', None)
    
    # Add idea localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"ACHIEVEMENT_{tag}", translate=translate)
    
    # Initialize achievement definition
    Edit(F(pjoin("data","common","achievements",file_name)), {'unique_id': unique_id, f"ACHIEVEMENT_{tag}": info}, clear=False)
    
    # Add achievement icons
    icon = hoi4dev_auto_image(
        path = path,
        resource_type = "achievement",
        scale = "achievement",
        force = force
    )
    ImageSave(icon, F(pjoin("gfx","achievements",f"ACHIEVEMENT_{tag}")), format='dds')
    
    if (not force) and ExistFile(pjoin(path, ".cache", "grey.dds")):
        grey_icon = ImageLoad(pjoin(path, ".cache", "grey.dds"))
    else:
        grey_icon = icon.clone()
        grey_icon.type = "grayscale"
        ImageSave(grey_icon, F(pjoin(path, ".cache", "grey")), format='dds')
    ImageSave(grey_icon, F(pjoin("gfx","achievements",f"ACHIEVEMENT_{tag}_grey")), format='dds')
    
    if (not force) and ExistFile(pjoin(path, ".cache", "not_eligible.dds")):
        not_eligible_icon = ImageLoad(pjoin(path, ".cache", "not_eligible.dds"))
    else:
        not_eligible_icon = icon.clone()
        X = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "X")), find_default=False)
        X = ImageZoom(X, w=int(icon.size[0]*0.9), h=int(icon.size[1]*0.9))
        not_eligible_icon.composite(X, gravity='center')
        ImageSave(not_eligible_icon, F(pjoin(path, ".cache", "not_eligible")), format='dds')
    ImageSave(not_eligible_icon, F(pjoin("gfx","achievements",f"ACHIEVEMENT_{tag}_not_eligible")), format='dds')
