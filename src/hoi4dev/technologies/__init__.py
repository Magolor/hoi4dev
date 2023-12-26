from ..utils import *
from ..translation import AddLocalisation

def AddTechnology(path, translate=True):
    '''
    Add a technology to the mod.
    Args:
        path: str. The path of the resource files of the technology. The technology should include the technology icon, the technology definition and the localisation.
        translate: bool. Whether to translate the localisation of the technology.
    Return:
        None
    Use 'category' to specify the category of the technology. The category should be one of the following (unless manually added): `infantry`, `support`, `support`, `armour`, `nsb_armour`, `artillery`, `naval`, `mtgnaval`, `mtgnavalsupport`, `air_techs`, `ba_air_techs`, `industry`, `electronics`.
    Notice that adding a root technology could be very tricky. When setting 'is_root' to be true, the `data/interface/countrytechtreeview.json` must be prepared in advance. The root technology should be added to the file with the following structure:
    ```json
    {
        "guiTypes": {
            "containerWindowType": {
                "name": "countrytechtreeview",
                "containerWindowType": {
                    "name": "<category>_folder",
                    ... # root technology added here
                }
            }
        }
    }
    ```
    The `mtgnaval` and `mtgnavalsupport` folder are not connected with `_`, which is handled within the function implementation and no need to worry about.
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'show_equipment_icon': True,
        'size': 'medium'
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    assert ('category' in info), "The category should be specified in the technology definition!"
    assert (info['size'] in ['small', 'medium']), "The size of the technology should be either 'small' or 'medium'!"
    category = info.pop('category')
    size = info.pop('size')
    x = info.pop('x', 0); y = info.pop('y', 0)
    is_root = info.pop('is_root', False)
    root_x = info.pop('root_x', 0)
    root_y = info.pop('root_y', 0)
    root_width = info.pop('width', 70)
    root_height = info.pop('height', 70)
    root_format = info.pop('format', 'LEFT')
    info = merge_dicts([{
        'folder': {
            'name': f"{category}{'' if category in ['mtgnaval', 'mtgnavalsupport'] else '_'}folder",
            'position': { 'x': x, 'y': y },
            'force_use_small_tech_layout': (size=='small'),
        }
    }, info])
    
    # Add technology localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"TECHNOLOGY_{tag}", translate=translate)
    
    # Initialize technology definition
    Edit(F(pjoin("data","common","technologies",f"TECHNOLOGY_{tag}.json")), {'technologies': {f"TECHNOLOGY_{tag}": info}})
    
    # Add technology icons (notice that the gfx should always be named '_medium' even if the size is small)
    scales = get_mod_config('img_scales'); w, h = scales[f'equipment_{size}']
    icon = ImageZoom(ImageFind(pjoin(path,"default")), w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","interface","technologies",f"TECHNOLOGY_{tag}_{size}")), format='dds')
    Edit(F(pjoin("data","interface","technologies",f"TECHNOLOGY_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_TECHNOLOGY_{tag}_medium", "texturefile": pjoin("gfx","interface","technologies",f"TECHNOLOGY_{tag}_{size}.dds")}}})
    
    # Handle root technology
    if is_root:
        assert ExistFile(F(pjoin("data","interface","countrytechtreeview.json"))), "The `data/interface/countrytechtreeview.json` file must be prepared when adding a root technology!"
        countrytechtreeview = LoadJson(F(pjoin("data","interface","countrytechtreeview.json")))
        for find_techtree in dup_gen('containerWindowType'):
            if find_techtree not in countrytechtreeview['guiTypes']:
                raise ValueError("The `data/interface/countrytechtreeview.json` does not contain 'countrytechtreeview', please verify its correctness!")
            if countrytechtreeview['guiTypes'][find_techtree]['name'] == "countrytechtreeview":
                break
        techtree = countrytechtreeview['guiTypes'][find_techtree]
        for find_folder in dup_gen('containerWindowType'):
            if find_folder not in techtree:
                raise ValueError(f"The `data/interface/countrytechtreeview.json` does not contain '{info['folder']['name']}', please verify its correctness!")
            if techtree[find_folder]['name'] == info['folder']['name']:
                break
        folder = techtree[find_folder]
        for key in dup_gen('gridboxtype'):
            if key not in folder:
                break
            if folder[key]['name'] == f"TECHNOLOGY_{tag}_tree":
                print(WARNING(f"The `data/interface/countrytechtreeview.json` already contains 'TECHNOLOGY_{tag}_tree'!")); return
                # raise ValueError()
        countrytechtreeview['guiTypes'][find_techtree][find_folder] = merge_dicts([folder, {
            "gridboxtype": {
                'name': f"TECHNOLOGY_{tag}_tree",
                'position': { 'x': root_x, 'y': root_y },
                'slotsize': { 'width': root_width, 'height': root_height },
                'format': root_format,
            },
        }], d=True)
        SaveJson(countrytechtreeview, F(pjoin("data","interface","countrytechtreeview.json")), indent=4)

def CreateDefaultTechnology(path, img, info=dict()):
    '''
    Create a default technology resource folder from the given image.
    Args:
        path: str. The path of the target resource folder of the technology.
        img: image.Image. A `wand` image object.
        info: Dict. The technology definition.
    Return:
        None
    '''
    CreateFolder(path)
    if img is None:
        img = ImageLoad(F(pjoin("hoi4dev_settings", "imgs", "default_equipment.png")))
    ImageSave(img, pjoin(path,"default"), format='png')
    SaveJson(info, pjoin(path,"info.json"), indent=4)
    CreateFile(pjoin(path,"locs.txt"))
    if 'name' in info:
        with open(pjoin(path,"locs.txt"), "w") as f:
            f.write(f"[en.@]\n{info['name']}\n")