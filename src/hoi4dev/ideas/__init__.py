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
    designer = info.pop('designer', False)
    category = info['category']; info.pop('category')
    if 'allowed_civil_war' not in info:
        info['allowed_civil_war'] = {'always': True} # Default to always available for all sides on civil war
    
    # Add idea localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"IDEA_{tag}", translate=translate)
    
    # Initialize idea definition
    data = {f"IDEA_{tag}": info} | ({'designer': True} if designer else dict())
    Edit(F(pjoin("data","common","ideas",f"IDEA_{tag}.json")), {'ideas': {category: data}})
    
    # Add idea icons
    scales = get_mod_config('img_scales'); w, h = scales['idea']
    icon = ImageFind(pjoin(path,"default"))
    if icon is None:
        icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_idea")), find_default=False)
        assert (icon is not None), "The default idea icon is not found!"
    icon = ImageZoom(icon, w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","interface","ideas",f"IDEA_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","ideas",f"IDEA_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_idea_{tag}", "texturefile": pjoin("gfx","interface","ideas",f"IDEA_{tag}.dds")}}})

def AddIdeaCategory(path, translate=True):
    '''
    Add a category of ideas to the mod.
    Args:
        path: str. The path of the resource files of the category. The resources should include the category definition, the localisation, and the ideas folder.
        translate: bool. Whether to translate the localisation of the category.
    Return:
        None
    '''
    
    # Add category localisation
    category_tag = path.strip('/').split('/')[-1].upper()
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"IDEA_CATEGORY_{category_tag}", translate=translate)

    # Initialize category definition
    info = merge_dicts([{
        'level': True
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    level = info.pop('level', True)
    
    ideas = []
    for idea_folder in ListFolders(path, ordered=True):
        tag = pjoin(path, idea_folder).strip('/').split('/')[-1].upper()
        AddIdea(pjoin(path, idea_folder), translate=translate)
        data = LoadJson(F(pjoin("data","common","ideas",f"IDEA_{tag}.json")))['ideas']
        assert (len(data) == 1), "The idea should belong to only one category!"
        idea = list(data.values())[0]; ideas.append(idea)
        assert (len(idea) == 1), "The idea should have only one tag!"
        Delete(F(pjoin("data","common","ideas",f"IDEA_{tag}.json")), rm=True)
    
    # Adjacency Constraints
    for i, idea in enumerate(ideas):
        tag = list(idea.keys())[0]
        if level:
            idea[tag]['level'] = len(ideas)-i
        # if ((prev_idea is not None) or (next_idea is not None)) and ('available' not in idea[tag]):
        #     idea[tag]['available'] = dict()
        # if (prev_idea is not None) and (next_idea is not None):
        #     or_cond = find_dup("OR", idea[tag]['available'])
        #     idea[tag]['available'][or_cond] = dict()
        #     or_field = idea[tag]['available'][or_cond]
        #     or_field[find_dup('has_idea',or_field)] = f"{list(next_idea.keys())[0]}"
        #     or_field[find_dup('has_idea',or_field)] = f"{list(prev_idea.keys())[0]}"
        # elif (prev_idea is not None):
        #     idea[tag]['available'][find_dup('has_idea',idea[tag]['available'])] = f"{list(prev_idea.keys())[0]}"
        # elif (next_idea is not None):
        #     idea[tag]['available'][find_dup('has_idea',idea[tag]['available'])] = f"{list(next_idea.keys())[0]}"
        
        
    idea_category = {f"IDEA_CATEGORY_{category_tag}": info | merge_dicts(ideas, d=False)}
    Edit(F(pjoin("data","common","ideas",f"IDEA_CATEGORY_{category_tag}.json")), {'ideas': idea_category})