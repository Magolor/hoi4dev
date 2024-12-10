from ..utils import *
from ..translation import AddLocalisation

def AddDecision(path, category, translate=True):
    '''
    Add a decision to the mod.
    Args:
        path: str. The path of the resource files of the decision. The resources should include the decision icon (optional), the decision definition and the localisation.
        category: str. The category of the decision.
        translate: bool. Whether to translate the localisation of the country.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        "fixed_random_seed": False,
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    category = info.pop('category', category)
    icon = ImageFind(pjoin(path,"default"))
    if ('icon' not in info) and (icon is not None):
        info['icon'] = f"{tag}"

    # Add decision localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"DECISION_{tag}", translate=translate)
    
    # Initialize decision definition
    Edit(F(pjoin("data","common","decisions",f"DECISION_{tag}.json")), {category: {f"DECISION_{tag}": info}})
    
    # Add decision icon
    scales = get_mod_config('img_scales'); w, h = scales['decision']
    if icon is not None:
        icon = ImageZoom(icon, w=w, h=h)
        ImageSave(icon, F(pjoin("gfx","interface","decisions",f"DECISION_{tag}")), format='dds')
        Edit(F(pjoin("data","interface","decisions",f"DECISION_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_decision_DECISION_{tag}", "texturefile": pjoin("gfx","interface","decisions",f"DECISION_{tag}.dds")}}})

def AddDecisionCategory(path, translate=True):
    '''
    Add a decision category and all decisions inside it.
    Args:
        path: str. The path of the resource files of the decision category. The resources should include the category definition and the localisation.
        translate: bool. Whether to translate the localisation of the decision category.
    Return:
        None
    '''
    category = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'icon': f"{category}",
        'picture': "GFX_decision_category_picture",
    },LoadJson(pjoin(path,"info.json")) if ExistFile(pjoin(path,"info.json")) else {}])
    for decision in ListFolders(path):
        if not decision.startswith('__'):
            AddDecision(pjoin(path, decision), category=f"DECISION_CATEGORY_{category}", translate=translate)
    
    # Add decision category localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"DECISION_CATEGORY_{category}", translate=translate)
    
    # Add decision category icon
    icon = ImageFind(pjoin(path,"icon"))
    scales = get_mod_config('img_scales'); w, h = scales['decision']
    if icon is not None:
        icon = ImageZoom(icon, w=w, h=h)
        ImageSave(icon, F(pjoin("gfx","interface","decisions",f"DECISION_CATEGORY_{category}")), format='dds')
        Edit(F(pjoin("data","interface","decisions",f"DECISION_CATEGORY_{category}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_decision_category_{category}", "texturefile": pjoin("gfx","interface","decisions",f"DECISION_CATEGORY_{category}.dds")}}})
    
    # Add decision category picture
    # picture = ImageFind(pjoin(path,"picture"))
    
    SaveJson({f"DECISION_CATEGORY_{category}":info}, F(pjoin("data","common","decisions","categories",f"DECISION_CATEGORY_{category}.json")), indent=4)