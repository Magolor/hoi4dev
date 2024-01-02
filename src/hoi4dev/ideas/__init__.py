from ..utils import *
from ..translation import AddLocalisation

def AddIdea(path, translate=True):
    '''
    Add an idea to the mod.
    Args:
        path: str. The path of the resource files of the idea. The resources should include the idea icon, the idea definition and the localisation.
        translate: bool. Whether to translate the localisation of the idea.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'category': 'country',
        'picture': tag,
        'removal_cost': -1,
        'modifier': {},
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    category = info['category']; info.pop('category')
    
    # Add idea localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"IDEA_{tag}", translate=translate)
    
    # Initialize idea definition
    Edit(F(pjoin("data","common","ideas",f"IDEA_{tag}.json")), {'ideas': {category: {f"IDEA_{tag}": info}}})
    
    # Add idea icons
    scales = get_mod_config('img_scales'); w, h = scales['idea']
    icon = ImageFind(pjoin(path,"default"))
    if icon is None:
        icon = ImageLoad(F(pjoin("hoi4dev_settings", "imgs", "default_equipment.png")))
    icon = ImageZoom(icon, w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","interface","ideas",f"IDEA_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","ideas",f"IDEA_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_idea_{tag}", "texturefile": pjoin("gfx","interface","ideas",f"IDEA_{tag}.dds")}}})
