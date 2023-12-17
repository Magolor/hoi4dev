from ..utils import *
from ..translation import AddLocalisation

def AddCountry(path, translate=True):
    '''
    Add a country to the mod.
    Args:
        path: str. The path of the resource files of the country. The resources should include the country flag, the country definition and the localisation.
        translate: bool. Whether to translate the localisation of the country.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'graphical_culture': 'eastern_european_gfx',
        'graphical_culture_2d': 'eastern_european_2d',
    },LoadJson(pjoin(path,"info.json"))])
    name = info['name']; info.pop('name')
    history = info['history']; info.pop('history')
    info['color'] = "rgb { "+' '.join([str(x) for x in info['rgb']])+ " }"; info.pop('rgb')
    if 'ruling_party' not in info:
        info['ruling_party'] = max(info['popularities'], key=lambda k: info['popularities'][k])
    
    # Add country tag
    Edit(F(pjoin("data","common","country_tags","00_countries.json")), {tag: f"countries/{tag}.txt"})
    
    # Add country color
    Edit(F(pjoin("data","common","countries","colors.json")), {tag: {'color': info['color'], 'color_ui': info['color']}})
    
    # Add country localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"COUNTRY_{tag}", translate=translate)
    
    # Initialize country definition
    Edit(F(pjoin("data","common","countries",f"{tag}.json")), info)
    
    # Initialize country history
    Edit(F(pjoin("data","history","countries",f"{tag}.json")), history)
    
    # Add country flags
    for flag_file in ListFiles(pjoin(path,"flags")):
        flag = ImageFind(pjoin(path,"flags",flag_file)); scales = get_mod_config('img_scales')
        w_l, h_l = scales['flag_large']; flag_large = ImageZoom(flag, w=w_l, h=h_l)
        w_m, h_m = scales['flag_medium']; flag_medium = ImageZoom(flag, w=w_m, h=h_m)
        w_s, h_s = scales['flag_small']; flag_small = ImageZoom(flag, w=w_s, h=h_s)
        ImageSave(flag_large, F(pjoin("gfx","flags",flag_file.split('.')[0])), format='dds')
        ImageSave(flag_medium, F(pjoin("gfx","flags","medium",flag_file.split('.')[0])), format='dds')
        ImageSave(flag_small, F(pjoin("gfx","flags","small",flag_file.split('.')[0])), format='dds')

def CreateDefaultCountry(path, img=ImageLoad(find_resource('imgs/default_flag.png')), info=dict()):
    '''
    Create a default country resource folder from the given image.
    Args:
        img: image.Image. A `wand` image object.
        path: str. The path of the resource files of the country.
        info: dict. The country definition.
    Return:
        None
    '''
    CreateFolder(path); CreateFolder(pjoin(path,"flags"))
    ImageSave(img, pjoin(path,"flags","default"), format='png')
    SaveJson(info, pjoin(path,"info.json"), indent=4)
    CreateFile(pjoin(path,"locs.txt"))
    if 'name' in info:
        with open(pjoin(path,"locs.txt"), "w") as f:
            f.write(f"[en.@NAME]\n{info['name']}\n")