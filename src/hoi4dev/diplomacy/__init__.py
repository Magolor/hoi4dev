from ..utils import *
from ..translation import AddLocalisation

def AddOpinionModifier(path, translate=True):
    '''
    Add an opinion modifier to the mod.
    Args:
        path: str. The path of the resource files of the opinion modifier. The resources should include the opinion modifier definition and the localisation.
        translate: bool. Whether to translate the localisation of the opinion modifier.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    assert ('value' in info), f"Value of opinion modifier {tag} not found."

    # Add decision localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"OPINION_{tag}", translate=translate)
    
    # Initialize opinion modifier definition
    Edit(F(pjoin("data","common","opinion_modifiers",f"OPINION_{tag}.json")), {'opinion_modifiers': {f"OPINION_{tag}": info}})
