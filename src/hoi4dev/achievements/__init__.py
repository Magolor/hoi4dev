from ..utils import *
from ..translation import AddLocalisation

def AddAchievement(unique_id, path, translate=True):
    '''
    Add an achievement to the mod.
    Args:
        unique_id: str. The unique id of your entire mod.
        path: str. The path of the resource files of the achievement. The resources should include the achievement icon, the achievement definition and the localisation.
        translate: bool. Whether to translate the localisation of the achievement.
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
    scales = get_mod_config('img_scales'); w, h = scales['achievement']
    icon = ImageFind(pjoin(path,"default"))
    if icon is None:
        icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_achievement")), find_default=False)
        assert (icon is not None), "The default achievement icon is not found!"
    icon = ImageZoom(icon, w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","achievements",f"ACHIEVEMENT_{tag}")), format='dds')
    
    grey_icon = icon.clone()
    grey_icon.type = "grayscale"
    ImageSave(grey_icon, F(pjoin("gfx","achievements",f"ACHIEVEMENT_{tag}_grey")), format='dds')
    
    not_eligible_icon = icon.clone()
    X = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "X")), find_default=False)
    X = ImageZoom(X, w=int(w*0.9), h=int(h*0.9))
    assert (icon is not None), "The default achievement not eligible icon is not found!"
    not_eligible_icon.composite(X, gravity='center')
    ImageSave(not_eligible_icon, F(pjoin("gfx","achievements",f"ACHIEVEMENT_{tag}_not_eligible")), format='dds')
