from ..utils import *
from ..translation import AddLocalisation

def AddTrait(path, translate=True):
    '''
    Add a trait to the mod.
    Args:
        path: str. The path of the resource files of the trait. The resources should include the trait definition and the localisation.
        translate: bool. Whether to translate the localisation of the trait.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'random': False,
        "ai_will_do": {"factor": 1},
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    
    # Add trait localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"TRAIT_{tag}", translate=translate)
    
    # Initialize trait definition
    Edit(F(pjoin("data","common","country_leader",f"TRAIT_{tag}.json")), {'leader_traits': {f"TRAIT_{tag}": info}})
