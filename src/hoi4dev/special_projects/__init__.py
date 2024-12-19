from ..utils import *
from ..translation import AddLocalisation

def AddSPReward(path, translate=True):
    '''
    Add a special project prototype reward to the mod.
    Args:
        path: str. The path of the resource files of the special project prototype reward. The resources should include the special project prototype reward definition and the localisation.
        translate: bool. Whether to translate the localisation of the special project prototype reward.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        "fire_only_once": False,
        "threshold": {
            "min": 0,
            "max": 100
        }
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    if 'options' in info:
        options = info.pop('options')
        for o in options:
            info[find_dup('option', info)] = o
    for o in info:
        if find_ori(o)=='option':
            c = find_idx(o)
            if 'token' not in info[o]:
                info[o]['token'] = f"SP_REWARD_{tag}_o{c}"
    
    # Add special project prototype reward localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"SP_REWARD_{tag}", translate=translate)
    
    # Initialize special project prototype reward definition
    Edit(F(pjoin("data","common","special_projects","prototype_rewards",f"SP_REWARD_{tag}.json")), {f"SP_REWARD_{tag}": info})

def AddSP(path, translate=True):
    '''
    Add a special project to the mod.
    Args:
        path: str. The path of the resource files of the special project. The resources should include the special project icon, the special project definition and the localisation.
        translate: bool. Whether to translate the localisation of the special project.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'icon': f"GFX_SP_{tag}",
        "complexity": "sp_complexity.large",
        "prototype_time": "sp_time.prototype.long",
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    
    # Add special project prototype reward localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"SP_{tag}", translate=translate)
    
    # Initialize special project definition
    Edit(F(pjoin("data","common","special_projects","projects",f"SP_{tag}.json")), {f"SP_{tag}": info})
    
    # Add special project icons
    scales = get_mod_config('img_scales'); w, h = scales['special_project']
    icon = ImageFind(pjoin(path,"default"))
    if icon is None:
        icon = ImageFind(pjoin(path,"raw"))
        if icon is not None:
            kwargs = LoadJson(pjoin(path,"bp_args.json")) if ExistFile(pjoin(path,"bp_args.json")) else (
                LoadJson(pjoin(path, "..", "bp_args.json")) if ExistFile(pjoin(path, "..", "bp_args.json")) else {}
            )
            icon = CreateBlueprintImage(icon, color='white', bg_color='transparent', **kwargs)
            ImageSave(icon, pjoin(path,"default"), format='png')
    icon = ImageFind(pjoin(path,"default"))
    if icon is None:
        icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_sp")), find_default=False)
        assert (icon is not None), "The default special project icon is not found!"
    icon = ImageZoom(icon, w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","interface","special_project","project_icons",f"SP_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","special_projects",f"SP_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_SP_{tag}", "texturefile": pjoin("gfx","interface","special_project","project_icons",f"SP_{tag}.dds")}}})