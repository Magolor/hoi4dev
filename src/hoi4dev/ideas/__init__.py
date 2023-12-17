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
        'picture': f"IDEA_{tag}",
        'removal_cost': -1,
        'modifier': {},
    },LoadJson(pjoin(path,"info.json"))])
    name = info['name'] if 'name' in info else None; info.pop('name')
    category = info['category']; info.pop('category')
    
    # Add idea localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"IDEA_{tag}", translate=translate)
    
    # Initialize idea definition
    Edit(F(pjoin("data","common","ideas",f"IDEA_{tag}.json")), {'ideas': {category: {f"IDEA_{tag}": info}}})
    
    # Add idea icons
    scales = get_mod_config('img_scales'); w, h = scales['idea']
    icon = ImageZoom(ImageFind(pjoin(path,"default")), w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","interface","ideas",f"IDEA_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","ideas",f"IDEA_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"IDEA_{tag}", "texturefile": pjoin("gfx","interface","ideas",f"IDEA_{tag}.dds")}}})

def CreateDefaultIdea(path, img, info=dict()):
    '''
    Create a default idea resource folder from the given image.
    Args:
        path: str. The path of the resource files of the idea.
        img: image.Image. A `wand` image object.
        info: dict. The idea definition.
    Return:
        None
    '''
    CreateFolder(path)
    ImageSave(img, pjoin(path,"default"), format='png')
    SaveJson(info, pjoin(path,"info.json"), indent=4)
    CreateFile(pjoin(path,"locs.txt"))
    if 'name' in info:
        with open(pjoin(path,"locs.txt"), "w") as f:
            f.write(f"[en.@NAME]\n{info['name']}\n")