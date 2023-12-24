from ..utils import *
from ..translation import AddLocalisation

def AddCharacter(path, translate=True):
    '''
    Add a character to the mod.
    Args:
        path: str. The path of the resource files of the character. The resources should include the character portrait, the character definition and the localisation.
        translate: bool. Whether to translate the localisation of the character.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'name': f"CHARACTER_{tag}_NAME",
        'portraits': {
            'civilian': {
                'large': f"gfx/leaders/CHARACTER_{tag}.dds",
                'small': f"gfx/leaders/CHARACTER_{tag}_small.dds",
            },
            'army': {
                'large': f"gfx/leaders/CHARACTER_{tag}_army.dds",
                'small': f"gfx/leaders/CHARACTER_{tag}_army_small.dds",
            },
            'navy': {
                'large': f"gfx/leaders/CHARACTER_{tag}_navy.dds",
                'small': f"gfx/leaders/CHARACTER_{tag}_navy_small.dds",
            },
        },
        'gender': 'female'
    },LoadJson(pjoin(path,"info.json"))])
    # name = info.pop('name', None)
    info['name'] = f"CHARACTER_{tag}_NAME"
    if 'country_leader' in info:
        info['country_leader'] = merge_dicts([{
            'desc': f"CHARACTER_{tag}_DESC",
            'traits': [],
        }, info['country_leader']])
    if 'advisor' in info:
        info['advisor'] = merge_dicts([{
            'idea_token': f"IDEA_CHARACTER_{tag}",
            'traits': [],
            'ledger': "all",
            'can_be_fired': True,
            'cost': 150,
            'removal_cost': 150,
        }, info['advisor']])
    
    # Add character localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"CHARACTER_{tag}", translate=translate)
    
    # Initialize character definition
    Edit(F(pjoin("data","common","characters",f"CHARACTER_{tag}.json")), {'characters': {f"CHARACTER_{tag}": info}})
    
    # Add character portraits
    for portrait_file in ['default', 'army', 'navy']:
        portrait = ImageFind(pjoin(path,"portraits",portrait_file))
        if portrait is None:
            portrait = ImageLoad(F(pjoin("hoi4dev_settings", "imgs", "default_portrait.png")))
        scales = get_mod_config('img_scales'); w_l, h_l = scales['leader_portrait']
        suffix = '' if portrait_file == 'default' else f"_{portrait_file}"
        ImageSave(ImageZoom(portrait, w=w_l, h=h_l), F(pjoin("gfx","leaders",f"CHARACTER_{tag}{suffix}")), format='dds')
        ImageSave(CreateAdvisorImage(portrait), F(pjoin("gfx","leaders",f"CHARACTER_{tag}{suffix}_small")), format='dds')

def CreateDefaultCharacter(path, img, info=dict()):
    '''
    Create a default character resource folder from the given image.
    Args:
        path: str. The path of the target resource folder of the character.
        img: image.Image. A `wand` image object.
        info: Dict. The character definition.
    Return:
        None
    '''
    CreateFolder(path); CreateFolder(pjoin(path,"portraits"))
    if img is None:
        img = ImageLoad(F(pjoin("hoi4dev_settings", "imgs", "default_portrait.png")))
    ImageSave(img, pjoin(path,"portraits","default"), format='png')
    SaveJson(info, pjoin(path,"info.json"), indent=4)
    CreateFile(pjoin(path,"locs.txt"))
    if 'name' in info:
        with open(pjoin(path,"locs.txt"), "w") as f:
            f.write(f"[en.@NAME]\n{info['name']}\n")