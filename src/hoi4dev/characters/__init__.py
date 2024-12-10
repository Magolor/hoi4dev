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
    for key in dup_gen('country_leader'):
        if key in info:
            info[key] = merge_dicts([{
                'desc': f"CHARACTER_{tag}_DESC",
                'traits': [],
            }, info[key]])
        else:
            break
    for key in dup_gen('advisor'):
        if key in info:
            info[key] = merge_dicts([{
                'idea_token': f"CHARACTER_{tag}",
                'desc': f"CHARACTER_{tag}_DESC",
                'traits': [],
                'ledger': "all",
                'can_be_fired': True,
                'cost': 150,
                'removal_cost': 150,
            }, info[key]])
        else:
            break
    
    # Add character localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"CHARACTER_{tag}", translate=translate)
    
    # Initialize character definition
    Edit(F(pjoin("data","common","characters",f"CHARACTER_{tag}.json")), {'characters': {f"CHARACTER_{tag}": info}})
    
    # Add character portraits
    portraits = ['default', 'army', 'navy']
    for f in ListFiles(pjoin(path,"portraits")):
        if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.dds'):
            portraits.append(f.split('.')[0])
    portraits = list(set(portraits))
    
    spriteTypes = dict()
    for portrait_file in portraits:
        portrait = ImageFind(pjoin(path,"portraits",portrait_file))
        if portrait is None:
            portrait = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_portrait")), find_default=False)
            assert (portrait is not None), "The default portrait is not found!"
        suffix = '' if portrait_file == 'default' else f"_{portrait_file}"
        ImageSave(CreateLeaderImage(portrait), F(pjoin("gfx","leaders",f"CHARACTER_{tag}{suffix}")), format='dds')
        ImageSave(CreateAdvisorImage(portrait), F(pjoin("gfx","leaders",f"CHARACTER_{tag}{suffix}_small")), format='dds')
        spriteTypes = merge_dicts([spriteTypes, {
            'spriteType': {"name": f"GFX_CHARACTER_{tag}_portrait{suffix}", "texturefile": pjoin("gfx","leaders",f"CHARACTER_{tag}{suffix}.dds")}
        }], d=True)
        spriteTypes = merge_dicts([spriteTypes, {
            'spriteType': {"name": f"GFX_CHARACTER_{tag}_portrait{suffix}_small", "texturefile": pjoin("gfx","leaders",f"CHARACTER_{tag}{suffix}_small.dds")}
        }], d=True)
    Edit(F(pjoin("data","interface","portraits",f"CHARACTER_{tag}.json")), {'spriteTypes': spriteTypes})

    # Add Gfx just in case one needs to change portraits

def AddRandomCharacters(path):
    '''
    Add random character portraits to the mod.
    Args:
        path: str. The path of the resource files of the character. The resources should include folders of character portraits.
    Return:
        None
        
    TODO: Currently this does not handle adding these to `portraits`, you need to manually arrange the GFX files in `portraits/*.json` files.
    For example, if character portrait is at `ponies/001.png`, then it should be referred to as `GFX_RANDOM_CHARACTER_PONIES_001_portrait` in `portraits/*.json`.
    '''
    for category in ListFolders(path):
        spriteTypes = dict()
        for f in ListFiles(pjoin(path, category)):
            if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.dds'):
                portrait = ImageFind(pjoin(path, category, f))
                tag = f"{category.upper()}_{f.split('.')[0].upper()}"
                # id, labels = f.split('.')[0].split('-'); labels = labels.split('_'); tag = f"{category.upper()}_{id.upper()}"
                # add_to_portraits(f"GFX_RANDOM_CHARACTER_{tag}_portrait", labels)                
                ImageSave(CreateLeaderImage(portrait), F(pjoin("gfx","leaders",f"RANDOM_CHARACTER_{tag}")), format='dds')
                ImageSave(CreateAdvisorImage(portrait), F(pjoin("gfx","leaders",f"RANDOM_CHARACTER_{tag}_small")), format='dds')
                spriteTypes = merge_dicts([spriteTypes, {
                    'spriteType': {"name": f"GFX_RANDOM_CHARACTER_{tag}_portrait", "texturefile": pjoin("gfx","leaders",f"RANDOM_CHARACTER_{tag}.dds")}
                }], d=True)
                spriteTypes = merge_dicts([spriteTypes, {
                    'spriteType': {"name": f"GFX_RANDOM_CHARACTER_{tag}_portrait_small", "texturefile": pjoin("gfx","leaders",f"RANDOM_CHARACTER_{tag}_small.dds")}
                }], d=True)
        Edit(F(pjoin("data","interface","portraits",f"RANDOM_CHARACTER_{category}.json")), {'spriteTypes': spriteTypes})


def GetRandomCorpsCommander(quality=8, traits_pool=list()):
    '''
    Generate a random corps commander.
    Args:
        quality: int. The quality of the corps commander.
        traits_pool: list. The pool of traits that the corps commander can have.
    Return:
        dict. The corps commander definition.
    '''
    skills = [
        "attack_skill",
        "defense_skill",
        "planning_skill",
        "logistics_skill",
    ]
    assert (quality >= len(skills)), f"Quality too low! Expected quality >= {len(skills)}."
    assert (quality <= len(skills)*6), f"Quality too high! Expected quality <= {len(skills)*6}."
    import numpy as np
    def random_partition(quality):
        parts = [quality//len(skills) for _ in range(len(skills))]
        if sum(parts) < quality:
            parts[np.random.randint(len(skills))] += quality - sum(parts)
        for t in range(32):
            i = np.random.randint(len(skills))
            if parts[i] > 1:
                j = np.random.randint(len(skills))
                if i != j and parts[j] < 6:
                    parts[i] -= 1
                    parts[j] += 1
        np.random.shuffle(parts)
        return {k: v for k, v in zip(skills, parts)}
    return {
        "corps_commander": random_partition(quality) | {
            "skill": max(1, quality//3) + (np.random.rand()>0.9),
            "traits": [np.random.choice(traits_pool)] if traits_pool and np.random.rand()>0.7 else [],
        }
    }