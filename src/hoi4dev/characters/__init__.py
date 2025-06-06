from ..utils import *
from ..translation import AddLocalisation
import numpy as np

def AddCharacter(path, translate=True, force=True):
    '''
    Add a character to the mod.
    Args:
        path: str. The path of the resource files of the character. The resources should include the character portrait, the character definition and the localisation.
        translate: bool. Whether to translate the localisation of the character.
        force: bool. Whether to force the overwriting of the existing cached images.
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
    CreateFolder(pjoin(path,"portraits"))
    for f in ListFiles(pjoin(path,"portraits")):
        if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.dds'):
            portraits.append(f.split('.')[0])
    portraits = list(set(portraits))
    
    spriteTypes = dict()
    for portrait_file in portraits:
        suffix = '' if portrait_file == 'default' else f"_{portrait_file}"
        need_portrait = force or (not ExistFile(pjoin(path, "portraits", ".cache", f"{portrait_file}_leader.dds"))) or (not ExistFile(pjoin(path, "portraits", ".cache", f"{portrait_file}_advisor.dds")))
        if need_portrait:
            portrait = hoi4dev_auto_image(
                path = pjoin(path,"portraits"),
                searches = [portrait_file, 'default'],
                resource_type = "portrait",
                cache_key = portrait_file,
                force = force
            )
        if (not force) and ExistFile(pjoin(path, "portraits", ".cache", f"{portrait_file}_leader.dds")):
            leader_portrait = ImageLoad(pjoin(path, "portraits", ".cache", f"{portrait_file}_leader.dds"))
        else:
            leader_portrait = CreateLeaderImage(portrait)
            ImageSave(leader_portrait, pjoin(path, "portraits", ".cache", f"{portrait_file}_leader.dds"))
        if (not force) and ExistFile(pjoin(path, "portraits", ".cache", f"{portrait_file}_advisor.dds")):
            advisor_portrait = ImageLoad(pjoin(path, "portraits", ".cache", f"{portrait_file}_advisor.dds"))
        else:
            advisor_portrait = CreateAdvisorImage(portrait)
            ImageSave(advisor_portrait, pjoin(path, "portraits", ".cache", f"{portrait_file}_advisor.dds"))
        ImageSave(leader_portrait, F(pjoin("gfx","leaders",f"CHARACTER_{tag}{suffix}")), format='dds')
        ImageSave(advisor_portrait, F(pjoin("gfx","leaders",f"CHARACTER_{tag}{suffix}_small")), format='dds')
        spriteTypes = merge_dicts([spriteTypes, {
            'spriteType': {"name": f"GFX_CHARACTER_{tag}_portrait{suffix}", "texturefile": pjoin("gfx","leaders",f"CHARACTER_{tag}{suffix}.dds")}
        }], d=True)
        spriteTypes = merge_dicts([spriteTypes, {
            'spriteType': {"name": f"GFX_CHARACTER_{tag}_portrait{suffix}_small", "texturefile": pjoin("gfx","leaders",f"CHARACTER_{tag}{suffix}_small.dds")}
        }], d=True)
    Edit(F(pjoin("data","interface","portraits",f"CHARACTER_{tag}.json")), {'spriteTypes': spriteTypes})

    # Add Gfx just in case one needs to change portraits

def AddRandomCharacters(path, force=True):
    '''
    Add random character portraits to the mod.
    Args:
        path: str. The path of the resource files of the character. The resources should include folders of character portraits.
        force: bool. Whether to force the overwriting of the existing cached images.
    Return:
        None
        
    TODO: Currently this does not handle adding these to `portraits`, you need to manually arrange the GFX files in `portraits/*.json` files.
    For example, if character portrait is at `ponies/001.png`, then it should be referred to as `GFX_RANDOM_CHARACTER_PONIES_001_portrait` in `portraits/*.json`.
    '''
    for category in ListResourceFolders(path):
        spriteTypes = dict()
        for f in ListFiles(pjoin(path, category)):
            if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.dds'):
                tag = f"{category.upper()}_{f.split('.')[0].upper()}"
                need_portrait = force or (not ExistFile(pjoin(path, ".cache", f"{tag}_leader.dds"))) or (not ExistFile(pjoin(path, ".cache", f"{tag}_advisor.dds")))
                if need_portrait:
                    portrait = ImageFind(pjoin(path, category, f))
                # id, labels = f.split('.')[0].split('-'); labels = labels.split('_'); tag = f"{category.upper()}_{id.upper()}"
                # add_to_portraits(f"GFX_RANDOM_CHARACTER_{tag}_portrait", labels)
                if (not force) and ExistFile(pjoin(path, ".cache", f"{tag}_leader.dds")):
                    leader_portrait = ImageLoad(pjoin(path, ".cache", f"{tag}_leader.dds"))
                else:
                    leader_portrait = CreateLeaderImage(portrait)
                    ImageSave(leader_portrait, pjoin(path, ".cache", f"{tag}_leader.dds"))
                if (not force) and ExistFile(pjoin(path, ".cache", f"{tag}_advisor.dds")):
                    advisor_portrait = ImageLoad(pjoin(path, ".cache", f"{tag}_advisor.dds"))
                else:
                    advisor_portrait = CreateAdvisorImage(portrait)
                    ImageSave(advisor_portrait, pjoin(path, ".cache", f"{tag}_advisor.dds"))
                ImageSave(leader_portrait, F(pjoin("gfx","leaders",f"RANDOM_CHARACTER_{tag}")), format='dds')
                ImageSave(advisor_portrait, F(pjoin("gfx","leaders",f"RANDOM_CHARACTER_{tag}_small")), format='dds')
                spriteTypes = merge_dicts([spriteTypes, {
                    'spriteType': {"name": f"GFX_RANDOM_CHARACTER_{tag}_portrait", "texturefile": pjoin("gfx","leaders",f"RANDOM_CHARACTER_{tag}.dds")}
                }], d=True)
                spriteTypes = merge_dicts([spriteTypes, {
                    'spriteType': {"name": f"GFX_RANDOM_CHARACTER_{tag}_portrait_small", "texturefile": pjoin("gfx","leaders",f"RANDOM_CHARACTER_{tag}_small.dds")}
                }], d=True)
        Edit(F(pjoin("data","interface","portraits",f"RANDOM_CHARACTER_{category}.json")), {'spriteTypes': spriteTypes})


def GetRandomCorpsCommander(quality=8, traits_pool=list(), seed=42):
    '''
    Generate a random corps commander.
    Args:
        quality: int. The quality of the corps commander.
        traits_pool: list. The pool of traits that the corps commander can have.
        seed: int. The seed for the random number generator
    Return:
        dict. The corps commander definition.
    '''
    np.random.seed(seed)
    skills = [
        "attack_skill",
        "defense_skill",
        "planning_skill",
        "logistics_skill",
    ]
    assert (quality >= len(skills)), f"Quality too low! Expected quality >= {len(skills)}."
    assert (quality <= len(skills)*6), f"Quality too high! Expected quality <= {len(skills)*6}."
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

def GetRandomScientist(mode="random", specializations_pool=list(), traits_pool=list(), seed=42):
    '''
    Generate a random scientist.
    Args:
        mode: str. The mode of the scientist. Can be "single" (meaning a 2 point skill on one specialization), "multi" (meaning a 2 point skill on one specialization and a 1 point skill on another specialization), "expert" (meaning a 3 point skill on one specialization), "newbie" (meaning a 1 point skill on one specializations), "davinci" (meaning a 1 point skill on all specializations), or "random" (meaning a random mode selected from the above, by default it has a 50% chance of being "single", 25% chance of being "multi", 5% chance of being "expert", and 19% chance of being "newbie", and 1% chance of being "davinci"). Or, you can choose mode as a specialization that is in the specializations_pool, which forces the scientist to have a 2 point skill on that specialization.
        specializations_pool: list. The pool of specializations that the scientist can have.
        traits_pool: list. The pool of traits that the scientist can have.
        seed: int. The seed for the random number generator
    Return:
        dict. The scientist definition.
    '''
    np.random.seed(seed)
    if mode == "random":
        mode = np.random.choice(["single", "multi", "expert", "newbie", "davinci"], p=[0.5, 0.25, 0.05, 0.19, 0.01])
    if mode == "single":
        skills = {
            np.random.choice(specializations_pool): 2
        }
    elif mode == "multi":
        major = np.random.choice(specializations_pool)
        minor = np.random.choice([s for s in specializations_pool if s != major])
        skills = {
            major: 2,
            minor: 1
        }
    elif mode == "expert":
        skills = {
            np.random.choice(specializations_pool): 3
        }
    elif mode == "newbie":
        skills = {
            s: 1 for s in specializations_pool
        }
    elif mode == "davinci":
        skills = {
            s: 1 for s in specializations_pool
        }
    elif mode in specializations_pool:
        skills = {
            mode: 2
        }
    else:
        raise ValueError(f"Invalid mode: {mode}. Expected one of 'single', 'multi', 'expert', 'newbie', 'davinci', or 'random', or a specialization in the specializations_pool ({','.join(sp for sp in specializations_pool)}).")
    return {
        "generate_scientist_character": {
            "skills": skills,
            "traits": [np.random.choice(traits_pool)] if traits_pool and np.random.rand()>0.7 else [],
        }
    }