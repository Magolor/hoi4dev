from ..utils import *
from ..translation import AddLocalisation

def AddEvent(path, space, translate=True):
    '''
    Add a event to the mod.
    Args:
        path: str. The path of the resource files of the event. The resources should include the event icon (optional), the event definition and the localisation.
        space: str. The space of the event.
        translate: bool. Whether to translate the localisation of the country.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].split('-')[0]
    assert (tag.isdigit()), f"Event tag should be numeric, but got {tag}."
    tag = int(tag)
    info = merge_dicts([{
        'id': f"{space}.{tag}",
        'picture': f"GFX_EVENT_{space}_{tag}",
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    category = info.pop('category', 'country')
    if 'title' not in info:
        info['title'] = f"EVENT_{space}_{tag}"
    if 'desc' not in info:
        info['desc'] = f"EVENT_{space}_{tag}_desc"
    if 'options' in info:
        options = info.pop('options')
        for o in options:
            info[find_dup('option', info)] = o
    for o in info:
        if find_ori(o)=='option':
            c = find_idx(o)
            if 'name' not in info[o]:
                info[o]['name'] = f"EVENT_{space}_{tag}_o{c}"

    # Add event localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"EVENT_{space}_{tag}", translate=translate)
    
    # Initialize event definition (An empty event space folder is added if not exists)
    space_path = F(pjoin("data","event_spaces",space)); CreateFolder(space_path)
    Edit(F(pjoin("data","event_spaces",f"{space}",f"EVENT_{space}_{tag}.json")), {f"{category}_event": info})
    
    # Add event picture
    scales = get_mod_config('img_scales'); w, h = scales[f"{category}_event"]
    picture = ImageFind(pjoin(path,"default"))
    if picture is None:
        picture = ImageLoad(F(pjoin("hoi4dev_settings", "imgs", f"default_event.png")))
    if category == 'country':
        picture = CreateCountryEventImage(picture)
    else:
        picture = ImageZoom(picture, w=w, h=h)
    ImageSave(picture, F(pjoin("gfx","event_pictures",f"EVENT_{space}_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","events",f"EVENT_{space}_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_EVENT_{space}_{tag}", "texturefile": pjoin("gfx","event_pictures",f"EVENT_{space}_{tag}.dds")}}})

def AddEventSpace(path, translate=True):
    '''
    Add a event space and all events inside it.
    Args:
        path: str. The path of the resource files of the event space. The resources should include a list of folders, each representing a event.
        translate: bool. Whether to translate the localisation of the event.
    Return:
        None
    '''
    space = path.strip('/').split('/')[-1].upper()
    for event in ListFolders(path):
        if not event.startswith('__'):
            AddEvent(pjoin(path, event), space=space, translate=translate)
    event_space_path = F(pjoin("data","event_spaces",space))
    event_files = [file for file in ListFiles(event_space_path) if file.endswith('.json')]
    events = [LoadJson(pjoin(event_space_path,file)) for file in sorted(event_files, key=lambda x: int(Prefix(x).split('_')[-1]))]
    event_space = merge_dicts([{"add_namespace": space}] + events, d=True)
    SaveJson(event_space, F(pjoin("data","events",f"{space}.json")), indent=4)