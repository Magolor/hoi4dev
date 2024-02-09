from ..utils import *
from ..translation import AddLocalisation

def AddBoP(path, translate=True):
    '''
    Add a balance of power to the mod.
    Args:
        path: str. The path of the resource files of the bop. The resources should include the left side icon, right side icon, the bop definition and the localisation.
        translate: bool. Whether to translate the localisation of the bop.
    Return:
        None
    It is recommended to use 'sides' to define the sides of the bop, which is a dictionary mapping from the side name to the side. 'left' and 'right' are reserved for the left and right side of the bop.
    Any side definition using 'side' instead of 'sides' will NOT be processed by this function.
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'left_side': f'BOP_{tag}_LEFT_SIDE',
        'right_side': f'BOP_{tag}_RIGHT_SIDE',
        'initial_value': 0.0,
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    sides = info.pop('sides', list())
    modifiers = info.pop('modifiers', list())
    for s in sides:
        S = s.upper()
        sides[s] = merge_dicts([{
            'id': f'BOP_{tag}_{S}_SIDE',
            'icon': f'GFX_BOP_{tag}_{S}_SIDE',
        },sides[s]])
        for i, key in enumerate(dup_gen('range')):
            if key in sides[s]:
                sides[s][key] = merge_dicts([{
                    'id': f'BOP_{tag}_{S}_SIDE_r{i}',
                },sides[s][key]])
            else:
                break
    for s in sides:
        info[find_dup('side', info)] = sides[s]
    
    # Add bop localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"BOP_{tag}", translate=translate)
    
    # Initialize bop definition
    Edit(F(pjoin("data","common","bop",f"BOP_{tag}.json")), {f"BOP_{tag}": info})
    
    # Add bop modifiers
    if modifiers: Edit(F(pjoin("data","common","modifiers",f"BOP_{tag}.json")), modifiers)
    
    # Add bop icons
    scales = get_mod_config('img_scales'); w, h = scales['bop']
    sprites = []
    for s in sides:
        S = s.upper()
        icon = ImageFind(pjoin(path,"icons",s))
        if icon is None:
            icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "default_bop")), find_default=False)
            assert (icon is not None), "The default balance of power icon is not found!"
        icon = ImageZoom(icon, w=w, h=h)
        ImageSave(icon, F(pjoin("gfx","interface","bop",f"BOP_{tag}_{S}_SIDE")), format='dds')
        sprites.append({'spriteType': {"name": f"GFX_BOP_{tag}_{S}_SIDE", "texturefile": pjoin("gfx","interface","bop",f"BOP_{tag}_{S}_SIDE.dds")}})
    Edit(F(pjoin("data","interface","bop",f"BOP_{tag}.json")), {'spriteTypes': merge_dicts(sprites,d=True)})
