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
    if ('module_slots' in info) and (info['module_slots'] != 'inherit'):
        module_slot_gui = LoadJson(F(pjoin("hoi4dev_settings", "configs", "equipmentdesigner.json")))
        module_slot_template_path = F(pjoin("hoi4dev_settings", "configs", "equipmentdesigner_window.json"))
        module_slot_special_template_path = F(pjoin("hoi4dev_settings", "configs", "equipmentdesigner_window_special.json"))
        for slot_name in info['module_slots']:
            special = info['module_slots'][slot_name].pop('special', False) if isinstance(info['module_slots'][slot_name], dict) else False
            slot_gfx = info['module_slots'][slot_name].pop('gfx', "TM_light_tank_chassis_turret_type_slot") if isinstance(info['module_slots'][slot_name], dict) else "TM_light_tank_chassis_turret_type_slot"
            if special:
                data = LoadJson(module_slot_special_template_path)
                data['containerWindowType']['name'] = data['containerWindowType']['name'].replace("<slot_name>", slot_name)
            else:
                data = LoadJson(module_slot_template_path)
                data['containerWindowType']['name'] = data['containerWindowType']['name'].replace("<slot_name>", slot_name)
                data['containerWindowType']['containerWindowType']['name'] = data['containerWindowType']['containerWindowType']['name'].replace("<slot_name>", slot_name)
                data['containerWindowType']['containerWindowType__D1']['name'] = data['containerWindowType']['containerWindowType__D1']['name'].replace("<slot_name>", slot_name)
                data['containerWindowType']['containerWindowType__D1']['iconType']['spriteType'] = data['containerWindowType']['containerWindowType__D1']['iconType']['spriteType'].replace("<slot_gfx>", f"GFX_{slot_gfx}")
            module_slot_gui['guiTypes']['containerWindowType']['containerWindowType'] = merge_dicts([module_slot_gui['guiTypes']['containerWindowType']['containerWindowType'], data], d=True)
        module_slot_gui['guiTypes']['containerWindowType']['name'] = module_slot_gui['guiTypes']['containerWindowType']['name'].replace('<equipment_name>', f"ARCHETYPE_{tag}")
        module_slot_gui['guiTypes']['containerWindowType']['iconType']['spriteType'] = module_slot_gui['guiTypes']['containerWindowType']['iconType']['spriteType'].replace('<equipment_gfx>', f"GFX_ARCHETYPE_{tag}_designer")
        Edit(F(pjoin("data","interface","equipmentdesigner",f"ARCHETYPE_DESIGNER_{tag}.json")), module_slot_gui)
        # slot_mapping = [0, 1, 6, 7, 8, 2, 3, 4, 5] + [9] * max(0, len(info['module_slots'])-9)
        # info['module_slots'] = {k:v for r,(k,v) in sorted(zip(slot_mapping, info['module_slots'].items()))}
    if 'module_count_limit_batch' in info:
        lims = info.pop('module_count_limit_batch', list())
        for lim in lims:
            info[find_dup('module_count_limit',info)] = lim
    if 'duplicates' in info:
        duplicates = info.pop('duplicates', dict())
        duplicates_data = {"duplicate_archetypes": {
            f"ARCHETYPE_{k}": merge_dicts([{'archetype': f"ARCHETYPE_{tag}"}, v]) for k,v in duplicates.items()
        }}
    else:
        duplicates = dict()
        duplicates_data = dict()
    
    # Add archetype localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"ARCHETYPE_{tag}", translate=translate)
    
    # Initialize archetype definition
    data = merge_dicts([{'equipments': {f"ARCHETYPE_{tag}": info}}, duplicates_data])
    Edit(F(pjoin("data","common","units","equipment",f"ARCHETYPE_{tag}.json")), data)
    
    # Add designer pictures
    if 'module_slots' in info:
        scales = get_mod_config('img_scales'); w, h = scales['equipment_designer']
        designer_icon = ImageFind(pjoin(path,"designer"))
        if designer_icon is None:
            designer_icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_equipment")), find_default=False)
            assert (designer_icon is not None), "The default equipment icon is not found!"
        designer_icon = ImageZoom(designer_icon, w=w, h=h)
        ImageSave(designer_icon, F(pjoin("gfx","interface","equipments",f"ARCHETYPE_{tag}_designer")), format='dds')
        Edit(F(pjoin("data","interface","equipments",f"ARCHETYPE_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_ARCHETYPE_{tag}_designer", "texturefile": pjoin("gfx","interface","equipments",f"ARCHETYPE_{tag}_designer.dds")}}})

    # Update script_enums
    script_enums = LoadJson(F(pjoin("data","common","script_enums.json")))
    script_enum_equipment_bonus_type = set(script_enums['script_enum_equipment_bonus_type'])
    script_enum_equipment_bonus_type.add(f"ARCHETYPE_{tag}")
    for key in duplicates:
        script_enum_equipment_bonus_type.add(f"ARCHETYPE_{key}")
    script_enums['script_enum_equipment_bonus_type'] = list(script_enum_equipment_bonus_type)
    SaveJson(script_enums, F(pjoin("data","common","script_enums.json")), indent=4)

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
        - lg_armor_piercing
        - lg_attack
        - hg_armor_piercing
        - hg_attack
        - torpedo_attack
        - anti_air_attack
        - shore_bombardment
        - sub_attack
    - Directly inherited:
        - archetype
        - lend_lease_cost
        - can_license
        - is_convertable
        - reliability
        - hardness
        - max_strength
        - maximum_speed
        - entrenchment
        - recon
        - air_range
        - air_agility
        - air_superiority
        - weight
        - thrust
        - naval_speed
        - surface_detection
        - sub_detection
        - surface_visibility
        - sub_visibility
        - naval_range
        - naval_torpedo_damage_reduction_factor
        - naval_torpedo_enemy_critical_chance_factor
        - naval_weather_penalty_factor
        - port_capacity_usage
        - search_and_destroy_coordination
        - convoy_raiding_coordination
        - module_slots
        - default_modules
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
            'archetype': data['archetype'] if 'archetype' in data else None,
            'priority': data['priority']+1 if 'priority' in data else 0,
            'visual_level': data['visual_level']+1 if 'visual_level' in data else 0,
            
            'build_cost_ic': data['build_cost_ic']*(1+alpha) if 'build_cost_ic' in data else None,
            'lend_lease_cost': data['lend_lease_cost'] if 'lend_lease_cost' in data else None,
            'can_license': data['can_license'] if 'can_license' in data else None,
            'is_convertable': data['is_convertable'] if 'is_convertable' in data else None,
            'reliability': data['reliability'] if 'reliability' in data else None,
            
            'soft_attack': data['soft_attack']*(1+alpha) if 'soft_attack' in data else None,
            'hard_attack': data['hard_attack']*(1+alpha) if 'hard_attack' in data else None,
            'air_attack': data['air_attack']*(1+alpha) if 'air_attack' in data else None,
            'ap_attack': data['ap_attack']*(1+alpha) if 'ap_attack' in data else None,
            'breakthrough': data['breakthrough']*(1+alpha) if 'breakthrough' in data else None,
            
            'defense': data['defense']*(1+alpha) if 'defense' in data else None,
            'armor_value': data['armor_value']*(1+alpha) if 'armor_value' in data else None,
            'hardness': data['hardness'] if 'hardness' in data else None,
            'max_strength': data['max_strength'] if 'max_strength' in data else None,
            
            'air_defence': data['air_defence']*(1+alpha) if 'air_defence' in data else None,
            'air_ground_attack': data['air_ground_attack']*(1+alpha) if 'air_ground_attack' in data else None,
            'air_bombing': data['air_bombing']*(1+alpha) if 'air_bombing' in data else None,
            'naval_strike_attack': data['naval_strike_attack']*(1+alpha) if 'naval_strike_attack' in data else None,
            'naval_strike_targetting': data['naval_strike_targetting']*(1+alpha) if 'naval_strike_targetting' in data else None,
            
            'air_range': data['air_range'] if 'air_range' in data else None,
            'air_agility': data['air_agility'] if 'air_agility' in data else None,
            'air_superiority': data['air_superiority'] if 'air_superiority' in data else None,
            'weight': data['weight'] if 'weight' in data else None,
            'thrust': data['thrust'] if 'thrust' in data else None,
            
            'naval_speed': data['naval_speed'] if 'naval_speed' in data else None,
            'lg_armor_piercing': data['lg_armor_piercing']*(1+alpha) if 'lg_armor_piercing' in data else None,
            'lg_attack': data['lg_attack']*(1+alpha) if 'lg_attack' in data else None,
            'hg_armor_piercing': data['hg_armor_piercing']*(1+alpha) if 'hg_armor_piercing' in data else None,
            'hg_attack': data['hg_attack']*(1+alpha) if 'hg_attack' in data else None,
            'torpedo_attack': data['torpedo_attachk']*(1+alpha) if 'torpedo_attachk' in data else None,
            'anti_air_attack': data['anti_air_attack']*(1+alpha) if 'anti_air_attack' in data else None,
            'shore_bombardment': data['shore_bombardment']*(1+alpha) if 'shore_bombardment' in data else None,
            'sub_attack': data['sub_attack']*(1+alpha) if 'sub_attack' in data else None,
            'surface_detection': data['surface_detection'] if 'surface_detection' in data else None,
            'sub_detection': data['sub_detection'] if 'sub_detection' in data else None,
            'surface_visibility': data['surface_visibility'] if 'surface_visibility' in data else None,
            'sub_visibility': data['sub_visibility'] if 'sub_visibility' in data else None,
            'naval_range': data['naval_range'] if 'naval_range' in data else None,
            'naval_torpedo_damage_reduction_factor': data['naval_torpedo_damage_reduction_factor'] if 'naval_torpedo_damage_reduction_factor' in data else None,
            'naval_torpedo_enemy_critical_chance_factor': data['naval_torpedo_enemy_critical_chance_factor'] if 'naval_torpedo_enemy_critical_chance_factor' in data else None,
            'naval_weather_penalty_factor': data['naval_weather_penalty_factor'] if 'naval_weather_penalty_factor' in data else None,
            'port_capacity_usage': data['port_capacity_usage'] if 'port_capacity_usage' in data else None,
            'search_and_destroy_coordination': data['search_and_destroy_coordination'] if 'search_and_destroy_coordination' in data else None,
            'convoy_raiding_coordination': data['convoy_raiding_coordination'] if 'convoy_raiding_coordination' in data else None,
            'module_slots': data['module_slots'] if 'module_slots' in data else None,
            'default_modules': data['default_modules'] if 'default_modules' in data else None,
            
            'maximum_speed': data['maximum_speed'] if 'maximum_speed' in data else None,
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
    if ('module_slots' in info) and (info['module_slots'] != 'inherit'):
        module_slot_gui = LoadJson(F(pjoin("hoi4dev_settings", "configs", "equipmentdesigner.json")))
        module_slot_template_path = F(pjoin("hoi4dev_settings", "configs", "equipmentdesigner_window.json"))
        module_slot_special_template_path = F(pjoin("hoi4dev_settings", "configs", "equipmentdesigner_window_special.json"))
        for slot_name in info['module_slots']:
            special = info['module_slots'][slot_name].pop('special', False) if isinstance(info['module_slots'][slot_name], dict) else False
            slot_gfx = info['module_slots'][slot_name].pop('gfx', "TM_light_tank_chassis_turret_type_slot") if isinstance(info['module_slots'][slot_name], dict) else "TM_light_tank_chassis_turret_type_slot"
            if special:
                data = LoadJson(module_slot_special_template_path)
                data['containerWindowType']['name'] = data['containerWindowType']['name'].replace("<slot_name>", slot_name)
            else:
                data = LoadJson(module_slot_template_path)
                data['containerWindowType']['name'] = data['containerWindowType']['name'].replace("<slot_name>", slot_name)
                data['containerWindowType']['containerWindowType']['name'] = data['containerWindowType']['containerWindowType']['name'].replace("<slot_name>", slot_name)
                data['containerWindowType']['containerWindowType__D1']['name'] = data['containerWindowType']['containerWindowType__D1']['name'].replace("<slot_name>", slot_name)
                data['containerWindowType']['containerWindowType__D1']['iconType']['spriteType'] = data['containerWindowType']['containerWindowType__D1']['iconType']['spriteType'].replace("<slot_gfx>", f"GFX_{slot_gfx}")
            module_slot_gui['guiTypes']['containerWindowType']['containerWindowType'] = merge_dicts([module_slot_gui['guiTypes']['containerWindowType']['containerWindowType'], data], d=True)
        module_slot_gui['guiTypes']['containerWindowType']['name'] = module_slot_gui['guiTypes']['containerWindowType']['name'].replace('<equipment_name>', f"EQUIPMENT_{tag}")
        module_slot_gui['guiTypes']['containerWindowType']['iconType']['spriteType'] = module_slot_gui['guiTypes']['containerWindowType']['iconType']['spriteType'].replace('<equipment_gfx>', f"GFX_EQUIPMENT_{tag}_designer")
        Edit(F(pjoin("data","interface","equipmentdesigner",f"EQUIPMENT_DESIGNER_{tag}.json")), module_slot_gui)
        # slot_mapping = [0, 1, 6, 7, 8, 2, 3, 4, 5] + [9] * max(0, len(info['module_slots'])-9)
        # info['module_slots'] = {k:v for r,(k,v) in sorted(zip(slot_mapping, info['module_slots'].items()))}
    if 'module_count_limit_batch' in info:
        lims = info.pop('module_count_limit_batch', list())
        for lim in lims:
            info[find_dup('module_count_limit',info)] = lim
    if debug:
        info['active'] = True
    
    # Add equipment localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"EQUIPMENT_{tag}", translate=translate)
    
    # Initialize equipment definition
    Edit(F(pjoin("data","equipments",f"EQUIPMENT_{tag}.json")), {'equipments': {f"EQUIPMENT_{tag}": info}})

    # Update script_enums
    script_enums = LoadJson(F(pjoin("data","common","script_enums.json")))
    script_enum_equipment_bonus_type = set(script_enums['script_enum_equipment_bonus_type'])
    script_enum_equipment_bonus_type.add(f"EQUIPMENT_{tag}")
    script_enums['script_enum_equipment_bonus_type'] = list(script_enum_equipment_bonus_type)
    SaveJson(script_enums, F(pjoin("data","common","script_enums.json")), indent=4)
    
    # Add equipment pictures
    scales = get_mod_config('img_scales'); w, h = scales['equipment_medium']
    icon = ImageFind(pjoin(path,"default"))
    if icon is None:
        icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_equipment")), find_default=False)
        assert (icon is not None), "The default equipment icon is not found!"
    icon = ImageZoom(icon, w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","interface","equipments",f"EQUIPMENT_{tag}")), format='dds')
    sprite_data = {'spriteTypes': {'spriteType': {"name": f"GFX_EQUIPMENT_{tag}_medium", "texturefile": pjoin("gfx","interface","equipments",f"EQUIPMENT_{tag}.dds")}}}
    if 'module_slots' in info:
        scales = get_mod_config('img_scales'); w, h = scales['equipment_designer']
        designer_icon = ImageFind(pjoin(path,"designer"))
        if designer_icon is None:
            designer_icon = icon.clone()
        designer_icon = ImageZoom(designer_icon, w=w, h=h)
        ImageSave(designer_icon, F(pjoin("gfx","interface","equipments",f"EQUIPMENT_{tag}_designer")), format='dds')
        sprite_data['spriteTypes']['spriteType__D1'] = {"name": f"GFX_EQUIPMENT_{tag}_designer", "texturefile": pjoin("gfx","interface","equipments",f"EQUIPMENT_{tag}_designer.dds")}
    Edit(F(pjoin("data","interface","equipments",f"EQUIPMENT_{tag}.json")), sprite_data)

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
    Edit(F(pjoin("data","common","units","equipment",f"zz_all_equipments.json")), merge_dicts(equipments))


def AddModules(module_type, path, translate=True):
    '''
    Add all modules to the mod.
    Args:
        module_type: str. The type of the modules (currently support `tank`, `ship` or `plane`), it only affects the dlc requirement.
        path: str. The path of the resource files of the modules. Each module resources should include the module icon, the module definition and the localisation.
        translate: bool. Whether to translate the localisation of the module.
    Return:
        None
    '''
    modules = {
	    "limit": {
	    	"has_dlc": {
                "tank": "No Step Back",
                "ship": "Man the Guns",
                "plane":"By Blood Alone"
            }[module_type]
	    }
    }
    for category in ListFolders(path, ordered=True):
        if ExistFile(pjoin(path, category, "locs.txt")):
            AddLocalisation(pjoin(path, category, "locs.txt"), scope=f"EQ_MOD_CAT_{category}_TITLE", translate=translate)
        scales = get_mod_config('img_scales'); w, h = scales[f'equipment_small']
        cat_icon = ImageFind(pjoin(path, category, "default"))
        if cat_icon is None:
            cat_icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_equipment")), find_default=False)
            assert (cat_icon is not None), "The default equipment icon is not found!"
        cat_icon = ImageZoom(cat_icon, w=w, h=h)
        ImageSave(cat_icon, F(pjoin("gfx","interface","modules",f"GFX_EMI_{category}")), format='dds')
        Edit(F(pjoin("data","interface","modules",f"GFX_EMI_{category}.json")), {'spriteTypes': {
            'spriteType': {"name": f"GFX_EMI_{category}", "texturefile": pjoin("gfx","interface","modules",f"GFX_EMI_{category}.dds"), "legacy_lazy_load": False},
        }})
        
        for tag in ListFolders(pjoin(path, category), ordered=True):
            module_path = pjoin(path, category, tag)
            info = merge_dicts([{
                'category': category,
                'sfx': 'sfx_ui_sd_module_engine'
            },LoadJson(pjoin(module_path,"info.json"))])
            name = info.pop('name', None)
    
            # Add module localisation
            AddLocalisation(pjoin(module_path,"locs.txt"), scope=f"MODULE_{tag}", translate=translate)
            
            modules = merge_dicts([modules, {f"MODULE_{tag}": info}])
            
            # Add module icons
            scales = get_mod_config('img_scales'); w, h = scales[f'equipment_small']
            icon = ImageFind(pjoin(module_path,"default"))
            if icon is None:
                icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_equipment")), find_default=False)
                assert (icon is not None), "The default equipment icon is not found!"
            icon = ImageZoom(icon, w=w, h=h)
            ImageSave(icon, F(pjoin("gfx","interface","modules",f"MODULE_{tag}")), format='dds')
            Edit(F(pjoin("data","interface","modules",f"MODULE_{tag}.json")), {'spriteTypes': {
                'spriteType': {"name": f"GFX_MODULE_{tag}", "texturefile": pjoin("gfx","interface","modules",f"MODULE_{tag}.dds")},
                'spriteType__D1': {"name": f"GFX_EMI_MODULE_{tag}", "texturefile": pjoin("gfx","interface","modules",f"MODULE_{tag}.dds"), "legacy_lazy_load": False},
            }})
    
    # Initialize modules definition
    file_name = f"00_{module_type}_modules.json"
    Edit(F(pjoin("data","common","units","equipment","modules",file_name)), {"equipment_modules": modules}, clear=False)