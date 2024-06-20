from ..utils import *
from ..translation import AddLocalisation

def AddModifier(path, translate=True):
    '''
    Add a modifier to the mod.
    Args:
        path: str. The path of the resource files of the modifier. The resources should include the modifier icon, the modifier definition and the localisation.
        translate: bool. Whether to translate the localisation of the modifier.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = LoadJson(pjoin(path,"info.json"))
    name = info.pop('name', None)
    
    # Add modifier localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"MODIFIER_{tag}", translate=translate)
    
    # Initialize modifier definition
    Edit(F(pjoin("data","common","modifiers",f"MODIFIER_{tag}.json")), {f"MODIFIER_{tag}": info})
    
    # Add modifier icons
    scales = get_mod_config('img_scales'); w, h = scales['modifier']
    icon = ImageFind(pjoin(path,"default"))
    if icon is None:
        icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_modifier")), find_default=False)
        assert (icon is not None), "The default modifier icon is not found!"
    icon = ImageZoom(icon, w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","interface","modifiers",f"MODIFIER_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","modifiers",f"MODIFIER_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_modifiers_MODIFIER_{tag}_icon", "texturefile": pjoin("gfx","interface","modifiers",f"MODIFIER_{tag}.dds")}}})

    gui_file = F(pjoin("data","interface","countrystateview.json"))
    assert ExistFile(gui_file), f"The `countrystateview.json` must be created for adding modifiers!"
    gui = LoadJson(gui_file); custom_icon_container = find_gui_scope(gui, scope='containerWindowType', func=lambda x: x['name']=='custom_icon_container')
    custom_icon_container[find_dup('iconType', custom_icon_container)] = {"name": f"MODIFIER_{tag}_icon", 'spriteType': f"GFX_modifiers_MODIFIER_{tag}_icon", "position": {"x": 0, "y": 0}, "Orientation": "UPPER_LEFT"}
    SaveJson(gui, gui_file, indent=4)