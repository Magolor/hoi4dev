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

def AddEquipment(path, translate=True, debug=False):
    '''
    Add an equipment to the mod. Notice that the equipment will not take effect until it is compiled using `AddEquipments` function.
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
        - air_defence
        - air_ground_attack
        - air_bombing
        - naval_strike_attack
        - naval_strike_targetting
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
        - air_range
        - air_agility
        - air_superiority
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
        data = LoadJson(F(pjoin("data","equipments",f"{info['parent']}.json")))['equipments'][info['parent']]
        info = {k:v for k,v in merge_dicts([{
            'archetype': data['archetype'],
            'priority': data['priority']+1,
            'visual_level': data['visual_level']+1,
            
            'build_cost_ic': data['build_cost_ic']*(1+alpha),
            'lend_lease_cost': data['lend_lease_cost'],
            'can_license': data['can_license'],
            'is_convertable': data['is_convertable'],
            'reliability': data['reliability'],
            
            'soft_attack': data['soft_attack']*(1+alpha) if 'soft_attack' in data else None,
            'hard_attack': data['hard_attack']*(1+alpha) if 'hard_attack' in data else None,
            'air_attack': data['air_attack']*(1+alpha) if 'air_attack' in data else None,
            'ap_attack': data['ap_attack']*(1+alpha) if 'ap_attack' in data else None,
            'breakthrough': data['breakthrough']*(1+alpha) if 'breakthrough' in data else None,
            
            'defense': data['defense']*(1+alpha) if 'defense' in data else None,
            'armor_value': data['armor_value']*(1+alpha) if 'armor_value' in data else None,
            'hardness': data['hardness'] if 'hardness' in data else None,
            
            'air_defence': data['air_defence']*(1+alpha) if 'air_defence' in data else None,
            'air_ground_attack': data['air_ground_attack']*(1+alpha) if 'air_ground_attack' in data else None,
            'air_bombing': data['air_bombing']*(1+alpha) if 'air_bombing' in data else None,
            'naval_strike_attack': data['naval_strike_attack']*(1+alpha) if 'naval_strike_attack' in data else None,
            'naval_strike_targetting': data['naval_strike_targetting']*(1+alpha) if 'naval_strike_targetting' in data else None,
            
            'air_range': data['air_range'] if 'air_range' in data else None,
            'air_agility': data['air_agility'] if 'air_agility' in data else None,
            'air_superiority': data['air_superiority'] if 'air_superiority' in data else None,
            
            'maximum_speed': data['maximum_speed'],
            'entrenchment': data['entrenchment'] if 'entrenchment' in data else None,
            'recon': data['recon'] if 'recon' in data else None,
        },info]).items() if v is not None}
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
    Edit(F(pjoin("data","equipments",f"EQUIPMENT_{tag}.json")), {'equipments': {f"EQUIPMENT_{tag}": info}})
    
    # Add equipment pictures
    scales = get_mod_config('img_scales'); w, h = scales['equipment_medium']
    icon = ImageFind(pjoin(path,"default"))
    if icon is None:
        icon = ImageLoad(F(pjoin("hoi4dev_settings", "imgs", "default_equipment.png")))
    icon = ImageZoom(icon, w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","interface","equipments",f"EQUIPMENT_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","equipments",f"EQUIPMENT_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_EQUIPMENT_{tag}_medium", "texturefile": pjoin("gfx","interface","equipments",f"EQUIPMENT_{tag}.dds")}}})

class EquipmentNode:
    def __init__(self, path, name):
        self.d = LoadJson(pjoin(path,"info.json"))
        self.name = name
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
    Add all the equipments and compile them.
    Args:
        path: str. The path of the resource folder of all the equipments.
        translate: bool. Whether to translate the localisation of the equipment.
        debug: bool. If in debug mode, all the equipments are always active.
    Return:
        None
    '''
    nodes = {f"EQUIPMENT_{folder}":EquipmentNode(pjoin(path,folder),f"EQUIPMENT_{folder}") for folder in ListFolders(path)}
    for k,n in nodes.items():
        if 'parent' in n.d:
            n.parent = nodes[n.d['parent']]
            n.parent.children.append(n)
    nodes_list = topo_sort(nodes)
    for p in nodes_list:
        AddEquipment(p.path, translate=translate, debug=debug)
    equipments = [LoadJson(F(pjoin("data","equipments",f"{p.name}.json"))) for p in nodes_list]
    Edit(F(pjoin("data","common","units","equipment",f"new_equipments.json")), merge_dicts(equipments))
