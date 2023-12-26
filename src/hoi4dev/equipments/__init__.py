from ..utils import *
from ..translation import AddLocalisation

def AddArchetype(path, translate=True):
    '''
    Add an equipment archetype to the mod.
    Args:
        path: str. The path of the resource files of the archetype. The resources should include the archetype icon, the archetype definition and the localisation.
        translate: bool. Whether to translate the localisation of the archetype.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'is_archetype': True,
        'is_buildable': False,
        'active': True,
        'group_by': 'archetype',
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    
    # Add archetype localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"ARCHETYPE_{tag}", translate=translate)
    
    # Initialize archetype definition
    Edit(F(pjoin("data","common","units","equipment",f"ARCHETYPE_{tag}.json")), {'equipments': {f"ARCHETYPE_{tag}": info}})

def CreateDefaultArchetype(path, info=dict()):
    '''
    Create a default archetype resource folder from the given image.
    Args:
        path: str. The path of the target resource folder of the archetype.
        info: Dict. The archetype definition.
    Return:
        None
    '''
    CreateFolder(path)
    SaveJson(info, pjoin(path,"info.json"), indent=4)
    CreateFile(pjoin(path,"locs.txt"))
    if 'name' in info:
        with open(pjoin(path,"locs.txt"), "w") as f:
            f.write(f"[en.@NAME]\n{info['name']}\n")

def AddEquipment(path, translate=True, debug=False):
    '''
    Add an equipment to the mod.
    Args:
        path: str. The path of the resource files of the equipment. The resources should include the equipment icon, the equipment definition and the localisation.
        translate: bool. Whether to translate the localisation of the equipment.
        debug: bool. If in debug mode, the equipment is always active.
    Return:
        None
    In the definition, you can set 'alpha_global' as a parameter, which is the scaling factor of the equipment's stats compared to its parent. This works only when the 'parent' attribute is set and the corresponding stat is missing in the equipment definition. Notice that the parent should be compiled before the current equipment. If not set, the `alpha_global` is 0.0 by default.
    Specifically, the scaling of an equipment's stats is done by the following principles:
    - Scaled by (1+alpha):
        - build_cost_ic
        - soft_attack
        - hard_attack
        - air_attack
        - ap_attack
        - breakthrough
        - defense
        - armor_value
    - Directly inherited:
        - archetype
        - lend_lease_cost
        - can_license
        - is_convertable
        - reliability
        - hardness
        - maximum_speed
        - entrenchment
        - recon
    - Add by 1:
        - priority
        - visual_level
    - Others not inherited
    After scaling, you can further use 'alpha' or 'delta' scope of the definition to further modify the stats.
    Each stat, whether set or inherited, would first be scaled by (1+alpha) then increased by delta.
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'picture': f"EQUIPMENT_{tag}",
        'is_archetype': False,
        'group_by': 'type',
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    
    # Scaling of stats
    if 'parent' in info:
        alpha = info.pop('alpha_global', 0.0)
        data = LoadJson(F(pjoin("data","common","units","equipment",f"{info['parent']}.json")))['equipments'][info['parent']]
        info = merge_dicts([{
            'archetype': data['archetype'],
            'priority': data['priority']+1,
            'visual_level': data['visual_level']+1,
            
            'build_cost_ic': data['build_cost_ic']*(1+alpha),
            'lend_lease_cost': data['lend_lease_cost'],
            'can_license': data['can_license'],
            'is_convertable': data['is_convertable'],
            'reliability': data['reliability'],
            
            'soft_attack': data['soft_attack']*(1+alpha),
            'hard_attack': data['hard_attack']*(1+alpha),
            'air_attack': data['air_attack']*(1+alpha),
            'ap_attack': data['ap_attack']*(1+alpha),
            'breakthrough': data['breakthrough']*(1+alpha),
            
            'defense': data['defense']*(1+alpha),
            'armor_value': data['armor_value']*(1+alpha),
            'hardness': data['hardness'],
            
            'maximum_speed': data['maximum_speed'],
            'entrenchment': data['entrenchment'],
            'recon': data['recon'],
        },info])
    if 'alpha' in info:
        for stat in info['alpha']:
            if stat in info:
                info[stat] = info[stat]*(1+info['alpha'][stat])
        info.pop('alpha')
    if 'delta' in info:
        for stat in info['delta']:
            if stat in info:
                info[stat] = info[stat]+info['delta'][stat]
        info.pop('delta')
    if debug:
        info['active'] = True
    
    # Add equipment localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"EQUIPMENT_{tag}", translate=translate)
    
    # Initialize equipment definition
    Edit(F(pjoin("data","common","units","equipment",f"EQUIPMENT_{tag}.json")), {'equipments': {f"EQUIPMENT_{tag}": info}})
    
    # Add equipment pictures
    scales = get_mod_config('img_scales'); w, h = scales['equipment_medium']
    icon = ImageZoom(ImageFind(pjoin(path,"default")), w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","interface","equipments",f"EQUIPMENT_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","equipments",f"EQUIPMENT_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_EQUIPMENT_{tag}_medium", "texturefile": pjoin("gfx","interface","equipments",f"EQUIPMENT_{tag}.dds")}}})

class EquipmentNode:
    def __init__(self, path):
        self.d = LoadJson(pjoin(path,"info.json"))
        self.path = path
        self.parent = None
        self.children = []

def topo_sort(nodes):
    b = {k:0 for k in nodes}
    q = [p for k, p in nodes.items() if len(p.children)==b[k]]; s = 0
    while s < len(q):
        p = q[s]; s += 1; k = p.d['parent'] if 'parent' in p.d else None
        if k:
            b[k] += 1
            if b[k] == len(p.parent.children):
                q.append(p.parent)
    return list(reversed(q))

def AddEquipments(path, translate=True, debug=False):
    '''
    Add all the equipments.
    Args:
        path: str. The path of the resource folder of all the equipments.
        translate: bool. Whether to translate the localisation of the equipment.
        debug: bool. If in debug mode, all the equipments are always active.
    Return:
        None
    '''
    nodes = {f"EQUIPMENT_{folder}":EquipmentNode(pjoin(path,folder)) for folder in ListFolders(path)}
    for k,n in nodes.items():
        if 'parent' in n.d:
            n.parent = nodes[n.d['parent']]
            n.parent.children.append(n)
    nodes_list = topo_sort(nodes)
    for p in nodes_list:
        AddEquipment(p.path, translate=translate, debug=debug)

def CreateDefaultEquipment(path, img, info=dict()):
    '''
    Create a default equipment resource folder from the given image.
    Args:
        path: str. The path of the target resource folder of the equipment.
        img: image.Image. A `wand` image object.
        info: Dict. The equipment definition.
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
            f.write(f"[en.@short]\n{info['name']}\n")