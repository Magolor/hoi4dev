from ..utils import *
from ..translation import AddLocalisation
from ..ideologies import get_ideologies

def sort_history_priority(key):
    return sort_priority(key, [
        'capital',
        'set_popularities',
        'set_politics',
        'create_faction',
        'add_to_faction',
        'set_technology',
        'if',
        'oob',
        'recruit_character',
        'activate_advisor',
        'add_ideas',
        'set_power_balance',
        'add_power_balance_modifier'
    ])

def AddCountry(path, translate=True, force=True):
    '''
    Add a country to the mod.
    Args:
        path: str. The path of the resource files of the country. The resources should include the country flag, the country definition and the localisation.
        translate: bool. Whether to translate the localisation of the country.
        force: bool. Whether to force the overwriting of the existing cached images.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'graphical_culture': 'eastern_european_gfx',
        'graphical_culture_2d': 'eastern_european_2d',
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    history = info['history']; info.pop('history')
    ai = info.pop('ai', None)
    info['color'] = "rgb { "+' '.join([str(x) for x in info['rgb']])+ " }"; info.pop('rgb')
    if 'oob' not in history:
        history['oob'] = tag
    for key in [k for k in history.keys() if k.endswith("_batch")]:
        for value in history[key]:
            history[find_dup(key[:-6], history)] = value
        history.pop(key)
    history = {k: v for k, v in sorted(history.items(), key=lambda item: sort_history_priority(item[0]))}
    
    # Add country tag
    Edit(F(pjoin("data","common","country_tags","00_countries.json")), {tag: f"countries/{tag}.txt"}, clear=False)
    
    # Add country color
    Edit(F(pjoin("data","common","countries","colors.json")), {tag: {'color': info['color'], 'color_ui': info['color']}}, clear=False)
    
    # Add country localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"COUNTRY_{tag}", translate=translate)
    
    # Initialize country definition
    Edit(F(pjoin("data","common","countries",f"{tag}.json")), info)
    
    # Initialize country history
    Edit(F(pjoin("data","history","countries",f"{tag}.json")), history)
    
    # Add country ai
    if ai is not None:
        ai_strategy_plans_name = ai['name'] if 'name' in ai else 'default'
        Edit(F(pjoin("data","common","ai_strategy_plans",f"{tag}_{ai_strategy_plans_name}.json")), {f"{tag}_{ai_strategy_plans_name}": ai})
    
    # Add country flags
    ideologies = list(set(list(get_ideologies().keys())  + ['default']))
    scales = get_mod_config('img_scales')
    for ideology in ideologies:
        flag_name = f"{tag}{'_'+ideology if ideology!='default' else ''}"
        flag = hoi4dev_auto_image(
            path = pjoin(path,"flags"),
            searches = [ideology, "default"],
            resource_type = "flag",
            scale = 'flag_large',
            cache_key = flag_name,
            force = force
        )
        w_l, h_l = scales['flag_large']; flag_large = ImageZoom(flag, w=w_l, h=h_l); ImageSave(flag_large, F(pjoin("gfx","flags",flag_name)), format='tga')
        w_m, h_m = scales['flag_medium']; flag_medium = ImageZoom(flag, w=w_m, h=h_m); ImageSave(flag_medium, F(pjoin("gfx","flags","medium",flag_name)), format='tga')
        w_s, h_s = scales['flag_small']; flag_small = ImageZoom(flag, w=w_s, h=h_s); ImageSave(flag_small, F(pjoin("gfx","flags","small",flag_name)), format='tga')
    
    # Add cosmetic flags
    cosmetic_path = pjoin(path, "flags", "cosmetic")
    if ExistFolder(cosmetic_path):
        for cosmetic in ListResourceFolders(cosmetic_path):
            for ideology in ideologies:
                flag_name = f"{cosmetic}{'_'+ideology if ideology!='default' else ''}"
                flag = hoi4dev_auto_image(
                    path = cosmetic_path,
                    searches = [ideology, "default"],
                    resource_type = "flag",
                    scale = 'flag_large',
                    cache_key = flag_name,
                    force = force
                )
                w_l, h_l = scales['flag_large']; flag_large = ImageZoom(flag, w=w_l, h=h_l); ImageSave(flag_large, F(pjoin("gfx","flags",flag_name)), format='tga')
                w_m, h_m = scales['flag_medium']; flag_medium = ImageZoom(flag, w=w_m, h=h_m); ImageSave(flag_medium, F(pjoin("gfx","flags","medium",flag_name)), format='tga')
                w_s, h_s = scales['flag_small']; flag_small = ImageZoom(flag, w=w_s, h=h_s); ImageSave(flag_small, F(pjoin("gfx","flags","small",flag_name)), format='tga')
