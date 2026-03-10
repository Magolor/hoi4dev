from ..utils import *
from ..translation import AddLocalisation
import re
import os
from collections import defaultdict

def AddTechnology(path, translate=True, force=True):
    '''
    Add a technology to the mod.
    Args:
        path: str. The path of the resource files of the technology. The technology should include the technology icon, the technology definition and the localisation.
        translate: bool. Whether to translate the localisation of the technology.
        force: bool. Whether to force the overwriting of the existing cached images.
    Return:
        None
    Use 'category' to specify the category of the technology. The category should be one of the following (unless manually added): `infantry`, `support`, `armour`, `nsb_armour`, `artillery`, `naval`, `mtgnaval`, `mtgnavalsupport`, `air_techs`, `ba_air_techs`, `industry`, `electronics`.
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
        },
        'force_use_small_tech_layout': (size=='small'),
    }, info])
    
    # Add technology localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"TECHNOLOGY_{tag}", translate=translate)
    
    # Initialize technology definition
    Edit(F(pjoin("data","common","technologies",f"TECHNOLOGY_{tag}.json")), {'technologies': {f"TECHNOLOGY_{tag}": info}})
    
    # Add technology icons (notice that the gfx should always be named '_medium' even if the size is small)
    icon = hoi4dev_auto_image(
        path = path,
        resource_type = "technology",
        resource_default = "equipment",
        scale = f"equipment_{size}",
        force = force
    )
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

def AddDoctrine(path, translate=True, force=True):
    '''
    Add a doctrine to the mod. A doctrine has slightly different settings compared to a technology.
    !!! Please note one important difference: CURRENTLY, doctrine does not support automatic change of the `countrydoctrineview.gui` file, you need to manually add the root doctrines to make them appear in the game. !!!
    Args:
        path: str. The path of the resource files of the doctrine. The doctrine should include the doctrine icon, the doctrine definition and the localisation.
        translate: bool. Whether to translate the localisation of the doctrine.
        force: bool. Whether to force the overwriting of the existing cached images.
    Return:
        None
    Use 'category' to specify the category of the doctrine. The category should be one of the following (unless manually added): `land`, `naval`, `air`, `special_forces`.
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        'doctrine': True,
        'doctrine_name': f"DOCTRINE_{tag}",
        "xp_unlock_cost": 100,
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    assert ('category' in info), "The category should be specified in the doctrine definition!"
    category = info.pop('category')
    x = info.pop('x', 0); y = info.pop('y', 0)
    mapping = {'land': 'army', 'naval': 'navy', 'air': 'air', 'special_forces': 'special_forces'}
    info = merge_dicts([{
        'folder': {
            'name': f"{category}_doctrine_folder",
            'position': { 'x': x, 'y': y },
        },
        'xp_research_type': f"{mapping[category]}",
    }, info])
    
    # Add doctrine localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"DOCTRINE_{tag}", translate=translate)
    
    # Initialize technology definition
    Edit(F(pjoin("data","common","technologies",f"{category}_doctrine.json")), {'$technologies': {f"DOCTRINE_{tag}": info}}, d=True)
    
    # Add doctrine icons (notice that the gfx should always be named '_medium' even if the size is small)
    icon = hoi4dev_auto_image(
        path = path,
        resource_type = "doctrine",
        resource_default = "equipment",
        scale = "equipment_small",
        force = force
    )
    ImageSave(icon, F(pjoin("gfx","interface","technologies",f"DOCTRINE_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","technologies",f"DOCTRINE_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_DOCTRINE_{tag}_medium", "texturefile": pjoin("gfx","interface","technologies",f"DOCTRINE_{tag}.dds")}}})

DOCTRINE_META_KEYS = {
    'category',
    'x',
    'y',
    'categories',
    'research_cost',
    'ai_research_weights',
    'xp_unlock_cost',
    'ai_will_do',
    'doctrine',
    'doctrine_name',
    'folder',
    'xp_research_type',
    'force_use_small_tech_layout',
    'size',
    'is_root',
    'root_x',
    'root_y',
    'width',
    'height',
    'format',
    'name',
}

DOCTRINE_NODE_PATTERN = re.compile(r'^(?P<group>[A-Za-z]+_\d+)_(?P<stage>\d+[A-Za-z]?)(?:_(?P<suffix>.+))?$')
DOCTRINE_STAGE_PATTERN = re.compile(r'^(?P<idx>\d+)(?P<tail>[A-Za-z]?)$')

LAND_TRACK_DEFINITIONS = {
    'infantry': {
        'name': 'DOCTRINE_TRACK_INFANTRY',
        'background': 'GFX_grand_battleplan_bg',
        'icon': 'GFX_doctrine_milestone_infantry_land',
        'icon_frame': 'GFX_doctrine_decor_land',
        'mastery': {
            'multiplier': 1.0,
            'categories': [
                'category_all_infantry'
            ]
        }
    },
    'combat_support': {
        'name': 'DOCTRINE_TRACK_COMBAT_SUPPORT',
        'background': 'GFX_sup_firepower_bg',
        'icon': 'GFX_doctrine_milestone_artillery_land',
        'icon_frame': 'GFX_doctrine_decor_land',
        'mastery': {
            'multiplier': 8.0,
            'categories': [
                'category_line_artillery',
                'category_artillery',
                'category_support_battalions'
            ]
        }
    },
    'armor': {
        'name': 'DOCTRINE_TRACK_ARMOR',
        'background': 'GFX_mob_warfare_bg',
        'icon': 'GFX_doctrine_milestone_armored_land',
        'icon_frame': 'GFX_doctrine_decor_land',
        'mastery': {
            'multiplier': 10.0,
            'categories': [
                'category_tanks',
                'category_all_armor'
            ],
            'sub_units': [
                'armored_car'
            ]
        }
    },
    'operations': {
        'name': 'DOCTRINE_TRACK_OPERATIONS',
        'background': 'GFX_tac_operation_bg',
        'icon': 'GFX_doctrine_milestone_operations_land',
        'icon_frame': 'GFX_doctrine_decor_land',
        'mastery': {
            'multiplier': 0.7,
            'categories': [
                'category_all_infantry',
                'category_line_artillery',
                'category_artillery',
                'category_tanks',
                'category_all_armor'
            ]
        }
    }
}

AIR_TRACK_DEFINITIONS = {
    'fighter_aircraft': {
        'name': 'DOCTRINE_TRACK_FIGHTER_AIRCRAFT',
        'background': 'GFX_air_superiority_bg',
        'icon': 'GFX_doctrine_milestone_fighter_air',
        'icon_frame': 'GFX_doctrine_decor_air',
        'mastery': {
            'multiplier': 8.0,
            'equipment': [
                'fighter',
                'interceptor'
            ]
        }
    },
    'strike_aircraft': {
        'name': 'DOCTRINE_TRACK_STRIKE_AIRCRAFT',
        'background': 'GFX_battlefield_destruction_bg',
        'icon': 'GFX_doctrine_milestone_striker_air',
        'icon_frame': 'GFX_doctrine_decor_air',
        'mastery': {
            'multiplier': 8.0,
            'equipment': [
                'cas',
                'naval_bomber',
                'suicide'
            ]
        }
    },
    'medium_aircraft': {
        'name': 'DOCTRINE_TRACK_MEDIUM_AIRCRAFT',
        'background': 'GFX_operational_destruction_bg',
        'icon': 'GFX_doctrine_milestone_medium_air',
        'icon_frame': 'GFX_doctrine_decor_air',
        'mastery': {
            'multiplier': 8.0,
            'equipment': [
                'tactical_bomber',
                'heavy_fighter',
                'scout_plane'
            ]
        }
    },
    'heavy_aircraft': {
        'name': 'DOCTRINE_TRACK_HEAVY_AIRCRAFT',
        'background': 'GFX_strategic_destruction_bg',
        'icon': 'GFX_doctrine_milestone_heavy_air',
        'icon_frame': 'GFX_doctrine_decor_air',
        'mastery': {
            'multiplier': 8.0,
            'equipment': [
                'strategic_bomber',
                'maritime_patrol_plane'
            ]
        }
    }
}

DOCTRINE_FOLDERS_FALLBACK = {
    'land': {
        'allowed': {
            'always': True
        },
        'name': 'land_doctrine_folder',
        'ledger': 'army',
        'ledger_gfx': 'GFX_land_doctrine_folder_icon',
        'tab_gfx': 'GFX_landdoctrine_tab_large',
        'color_frame': 1,
        'sound': 'ui_doctrine_tab_land'
    },
    'naval': {
        'allowed': {
            'always': True
        },
        'name': 'naval_doctrine_folder',
        'ledger': 'navy',
        'ledger_gfx': 'GFX_naval_doctrine_folder_icon',
        'tab_gfx': 'GFX_navaldoctrine_tab_large',
        'color_frame': 2,
        'sound': 'ui_doctrine_tab_naval'
    },
    'air': {
        'allowed': {
            'always': True
        },
        'name': 'air_doctrine_folder',
        'ledger': 'air',
        'ledger_gfx': 'GFX_air_doctrine_folder_icon',
        'tab_gfx': 'GFX_airdoctrine_tab_large',
        'color_frame': 3,
        'sound': 'ui_doctrine_tab_air'
    }
}

NAVAL_FORK_REQUIRED_FILES = [
    pjoin("common", "doctrines", "folders", "doctrine_folders.txt"),
    pjoin("common", "doctrines", "tracks", "sea_doctrine_tracks.txt"),
    pjoin("common", "doctrines", "grand_doctrines", "sea_grand_doctrines.txt"),
    pjoin("common", "doctrines", "subdoctrines", "sea", "navy_screen_doctrines.txt"),
    pjoin("common", "doctrines", "subdoctrines", "sea", "navy_submarine_doctrines.txt"),
    pjoin("common", "doctrines", "subdoctrines", "sea", "navy_capital_subdoctrines.txt"),
    pjoin("common", "doctrines", "subdoctrines", "sea", "navy_carrier_doctrines.txt"),
]


def _slugify(value):
    slug = re.sub(r'[^A-Za-z0-9]+', '_', str(value)).strip('_').lower()
    slug = re.sub(r'_+', '_', slug)
    return slug if slug else 'x'


def _parse_doctrine_node(folder):
    matched = DOCTRINE_NODE_PATTERN.match(folder)
    if matched is None:
        return None
    group = matched.group('group').upper()
    stage = matched.group('stage').upper()
    suffix = (matched.group('suffix') if matched.group('suffix') else stage).upper()
    return group, stage, suffix


def _stage_sort_key(stage):
    matched = DOCTRINE_STAGE_PATTERN.match(str(stage).upper())
    if matched is None:
        return (10**9, str(stage))
    idx = int(matched.group('idx'))
    tail = matched.group('tail').upper() if matched.group('tail') else ''
    tail_idx = 0 if tail == '' else (ord(tail) - ord('A') + 1)
    return (idx, tail_idx)


def _load_doctrine_nodes(path):
    nodes = dict()
    nodes_by_group = defaultdict(dict)
    for folder in ListFolders(path, ordered=True):
        if folder.startswith('.') or folder.startswith('_'):
            continue
        info_file = pjoin(path, folder, "info.json")
        if not ExistFile(info_file):
            continue
        parsed = _parse_doctrine_node(folder)
        if parsed is None:
            continue

        group, stage, suffix = parsed
        tag = f"DOCTRINE_{folder.upper()}"
        info = LoadJson(info_file)
        locs_file = pjoin(path, folder, "locs.txt")
        locs = ReadTxtLocs(locs_file, scope=tag) if ExistFile(locs_file) else {}

        if stage in nodes_by_group[group]:
            raise ValueError(f"Duplicate doctrine stage `{group}:{stage}` between `{nodes_by_group[group][stage]['folder']}` and `{folder}`.")

        node = {
            'folder': folder,
            'folder_path': pjoin(path, folder),
            'tag': tag,
            'group': group,
            'stage': stage,
            'suffix': suffix,
            'category': info.get('category', None),
            'info': info,
            'locs_file': locs_file,
            'locs': locs,
        }
        nodes[tag] = node
        nodes_by_group[group][stage] = node
    return nodes, nodes_by_group


def _get_path_targets(info):
    targets = []
    for key, value in info.items():
        if key.startswith('path') and isinstance(value, dict) and ('leads_to_tech' in value):
            targets.append(value['leads_to_tech'])
    return targets


def _lint_doctrine_graph(nodes):
    errors = []
    adjacency = defaultdict(list)

    for tag, node in nodes.items():
        for target in _get_path_targets(node['info']):
            adjacency[tag].append(target)
            if target not in nodes:
                errors.append(f"`{tag}` points to missing doctrine `{target}`.")

    for tag, node in nodes.items():
        xor_list = node['info'].get('xor', [])
        if xor_list is None:
            xor_list = []
        if not isinstance(xor_list, list):
            errors.append(f"`{tag}` has non-list `xor` definition.")
            continue
        for peer in xor_list:
            if peer not in nodes:
                errors.append(f"`{tag}` has `xor` pointing to missing doctrine `{peer}`.")
                continue
            peer_xor = nodes[peer]['info'].get('xor', [])
            if not isinstance(peer_xor, list) or (tag not in peer_xor):
                errors.append(f"`xor` mismatch: `{tag}` lists `{peer}`, but reverse link is missing.")

    visit_state = dict()
    stack = []

    def dfs(cur):
        visit_state[cur] = 1
        stack.append(cur)
        for nxt in adjacency.get(cur, []):
            if nxt not in nodes:
                continue
            state = visit_state.get(nxt, 0)
            if state == 0:
                dfs(nxt)
            elif state == 1:
                if nxt in stack:
                    cycle = stack[stack.index(nxt):] + [nxt]
                    errors.append("Cycle detected: " + " -> ".join(cycle))
                else:
                    errors.append(f"Cycle detected involving `{cur}` and `{nxt}`.")
        stack.pop()
        visit_state[cur] = 2

    for tag in nodes:
        if visit_state.get(tag, 0) == 0:
            dfs(tag)

    return errors


def _resolve_doctrine_mapping(nodes_by_group, nodes, mapping):
    errors = []
    groups_spec = mapping.get('groups', {})
    category_tracks = mapping.get('category_tracks', {})
    category_xp_type = mapping.get('category_xp_type', {})

    if not isinstance(groups_spec, dict) or len(groups_spec) == 0:
        errors.append("Mapping file must define `groups`.")

    expected_total = mapping.get('expected_total_nodes', None)
    if expected_total is not None and expected_total != len(nodes):
        errors.append(f"Expected `{expected_total}` doctrine nodes, found `{len(nodes)}`.")

    known_groups = set(nodes_by_group.keys())
    mapped_groups = set(groups_spec.keys())

    missing_groups = sorted(known_groups - mapped_groups)
    unknown_groups = sorted(mapped_groups - known_groups)

    if missing_groups:
        errors.append("Missing group mappings: " + ", ".join(missing_groups))
    if unknown_groups:
        errors.append("Unknown mapped groups: " + ", ".join(unknown_groups))

    mapped_node_counts = {tag: 0 for tag in nodes}
    resolved = dict()

    for group_name, group_spec in groups_spec.items():
        if group_name not in nodes_by_group:
            continue

        category = group_spec.get('category', None)
        if category not in category_tracks:
            errors.append(f"`{group_name}` uses unknown category `{category}`.")
            continue
        if category not in category_xp_type:
            errors.append(f"`category_xp_type` is missing entry for category `{category}`.")
            continue

        track_order = category_tracks[category]
        stage_map = nodes_by_group[group_name]
        grand_stage = str(group_spec.get('grand_stage', '0')).upper()
        if grand_stage not in stage_map:
            errors.append(f"`{group_name}` is missing configured grand stage `{grand_stage}`.")
            continue

        root_node = stage_map[grand_stage]
        mapped_node_counts[root_node['tag']] += 1
        used_stages = {grand_stage}

        tracks_spec = group_spec.get('tracks', {})
        resolved_tracks = dict()

        for track_name in track_order:
            if track_name not in tracks_spec:
                errors.append(f"`{group_name}` is missing track mapping for `{track_name}`.")
                continue
            raw_track_spec = tracks_spec[track_name]
            options = dict()

            if isinstance(raw_track_spec, dict) and 'stages' in raw_track_spec:
                options['core'] = [str(x).upper() for x in raw_track_spec['stages']]
            elif isinstance(raw_track_spec, dict) and 'options' in raw_track_spec:
                for option_name, option_stages in raw_track_spec['options'].items():
                    options[_slugify(option_name)] = [str(x).upper() for x in option_stages]
            else:
                errors.append(f"`{group_name}:{track_name}` must define either `stages` or `options`.")
                continue

            if len(options) == 0:
                errors.append(f"`{group_name}:{track_name}` has no options.")
                continue

            resolved_options = dict()
            for option_name, stage_tokens in options.items():
                if len(stage_tokens) == 0:
                    errors.append(f"`{group_name}:{track_name}:{option_name}` has no stages.")
                    continue
                option_nodes = []
                for stage in stage_tokens:
                    if stage not in stage_map:
                        errors.append(f"`{group_name}` references missing stage `{stage}`.")
                        continue
                    if stage in used_stages:
                        errors.append(f"`{group_name}` maps stage `{stage}` more than once.")
                        continue
                    used_stages.add(stage)
                    mapped_node_counts[stage_map[stage]['tag']] += 1
                    option_nodes.append(stage_map[stage])
                if len(option_nodes) > 0:
                    option_nodes = sorted(option_nodes, key=lambda node: _stage_sort_key(node['stage']))
                    resolved_options[option_name] = option_nodes

            if len(resolved_options) > 0:
                resolved_tracks[track_name] = resolved_options

        unmapped_stages = sorted(set(stage_map.keys()) - used_stages, key=_stage_sort_key)
        if len(unmapped_stages) > 0:
            errors.append(f"`{group_name}` has unmapped stages: {', '.join(unmapped_stages)}.")

        resolved[group_name] = {
            'category': category,
            'xp_type': category_xp_type[category],
            'track_order': track_order,
            'root': root_node,
            'tracks': resolved_tracks,
        }

    unmapped_nodes = sorted([tag for tag, cnt in mapped_node_counts.items() if cnt == 0])
    duplicate_nodes = sorted([tag for tag, cnt in mapped_node_counts.items() if cnt > 1])

    if len(unmapped_nodes) > 0:
        errors.append("Unmapped doctrine nodes: " + ", ".join(unmapped_nodes))
    if len(duplicate_nodes) > 0:
        errors.append("Nodes mapped multiple times: " + ", ".join(duplicate_nodes))

    if len(errors) > 0:
        raise ValueError("Doctrine mapping validation failed:\n- " + "\n- ".join(errors))

    return resolved


def _extract_doctrine_effects(info):
    effects = dict()
    for key, value in info.items():
        if key in DOCTRINE_META_KEYS:
            continue
        if key.startswith('path'):
            continue
        if key == 'xor':
            continue
        effects[key] = value
    return effects


def _get_node_localisation(node):
    name = node['locs'].get(node['tag'], {})
    desc = node['locs'].get(f"{node['tag']}_DESC", {})
    if len(desc) == 0:
        desc = node['locs'].get(f"{node['tag']}_desc", {})
    return name, desc


def _add_reward_localisation(all_reward_locs, sub_key, reward_key, node):
    reward_loc_key = f"{sub_key}_{reward_key}"
    reward_desc_key = f"{reward_loc_key}_desc"
    name_locs, desc_locs = _get_node_localisation(node)

    if reward_loc_key not in all_reward_locs:
        all_reward_locs[reward_loc_key] = {}
    if reward_desc_key not in all_reward_locs:
        all_reward_locs[reward_desc_key] = {}

    for language, value in name_locs.items():
        all_reward_locs[reward_loc_key][language] = value
    for language, value in desc_locs.items():
        all_reward_locs[reward_desc_key][language] = value

    fallback = node['suffix'].replace('_', ' ').title()
    if len(all_reward_locs[reward_loc_key]) == 0:
        all_reward_locs[reward_loc_key]['en'] = fallback
    if len(all_reward_locs[reward_desc_key]) == 0:
        all_reward_locs[reward_desc_key]['en'] = fallback


def _build_milestone(variable_name):
    return {
        'effect': {
            'if': {
                'limit': {
                    'NOT': {
                        'has_variable': variable_name
                    }
                },
                'set_variable': {
                    variable_name: 1
                }
            },
            'else': {
                'add_to_variable': {
                    variable_name: 1
                }
            }
        }
    }


def _register_doctrine_icon(node, sprite_name, sprite_defs, force):
    icon = hoi4dev_auto_image(
        path=node['folder_path'],
        resource_type="doctrine",
        resource_default="equipment",
        scale="equipment_small",
        force=force
    )
    texture_name = sprite_name.replace('GFX_', '')
    texture_relpath = pjoin("gfx", "interface", "doctrines", f"{texture_name}.dds")
    ImageSave(icon, F(pjoin("gfx", "interface", "doctrines", texture_name)), format='dds')
    sprite_defs.append({
        'spriteType': {
            'name': sprite_name,
            'textureFile': texture_relpath
        }
    })


def BuildDoctrines(path, mapping_path, naval_mode="fork_vanilla", translate=False, force=True):
    '''
    Build doctrine data for the 1.17+ doctrine system (folders/tracks/grand_doctrines/subdoctrines).
    Args:
        path: str. Doctrine resource root (e.g. `resources/doctrines`).
        mapping_path: str. Mapping file path (e.g. `resources/doctrines/_meta/mapping.json`).
        naval_mode: str. Only `fork_vanilla` is currently supported.
        translate: bool. Whether to auto-translate localisations.
        force: bool. Whether to force icon regeneration.
    Return:
        dict. A summary of generated doctrine counts.
    '''
    nodes, nodes_by_group = _load_doctrine_nodes(path)

    graph_errors = _lint_doctrine_graph(nodes)
    if len(graph_errors) > 0:
        raise ValueError("Doctrine graph lint failed:\n- " + "\n- ".join(graph_errors))

    mapping = LoadJson(mapping_path)
    resolved = _resolve_doctrine_mapping(nodes_by_group, nodes, mapping)

    if naval_mode != "fork_vanilla":
        raise NotImplementedError(f"Unsupported naval mode `{naval_mode}`. Only `fork_vanilla` is supported.")

    def _candidate_relpaths(relpath):
        root, ext = os.path.splitext(relpath)
        if ext == '.txt':
            return [relpath, root + '.json']
        if ext == '.json':
            return [relpath, root + '.txt']
        return [relpath, relpath + '.txt', relpath + '.json']

    def _exist_in_mod_or_data(relpath):
        for candidate in _candidate_relpaths(relpath):
            if ExistFile(F(candidate)) or ExistFile(F(pjoin("data", candidate))):
                return True
        return False

    missing_naval_files = [f for f in NAVAL_FORK_REQUIRED_FILES if not _exist_in_mod_or_data(f)]
    if len(missing_naval_files) > 0:
        raise ValueError("Missing vanilla naval doctrine fork files in mod copies:\n- " + "\n- ".join(missing_naval_files))

    if (not _exist_in_mod_or_data(pjoin("common", "doctrines", "folders", "doctrine_folders.txt"))):
        SaveJson(
            DOCTRINE_FOLDERS_FALLBACK,
            F(pjoin("data", "common", "doctrines", "folders", "doctrine_folders.json")),
            indent=4
        )

    # Preserve old per-node doctrine localisation keys.
    for node in nodes.values():
        AddLocalisation(node['locs_file'], scope=node['tag'], translate=translate)

    SaveJson(LAND_TRACK_DEFINITIONS, F(pjoin("data", "common", "doctrines", "tracks", "PIHC_land_doctrine_tracks.json")), indent=4)
    SaveJson(AIR_TRACK_DEFINITIONS, F(pjoin("data", "common", "doctrines", "tracks", "PIHC_air_doctrine_tracks.json")), indent=4)

    grands = {'land': {}, 'air': {}}
    subdoctrines = {'land': {}, 'air': {}}
    reward_locs = dict()
    sprite_defs = []

    for group_name in mapping['groups'].keys():
        if group_name not in resolved:
            continue
        group = resolved[group_name]
        category = group['category']
        track_order = group['track_order']
        root = group['root']

        grand_slug = _slugify(root['suffix'])
        grand_key = f"pihc_{category}_{grand_slug}"
        if grand_key in grands[category]:
            raise ValueError(f"Duplicate grand doctrine key `{grand_key}`.")

        grand_icon = f"GFX_doctrine_{grand_key}_medium"
        _register_doctrine_icon(root, grand_icon, sprite_defs, force=force)

        root_effects = _extract_doctrine_effects(root['info'])
        root_ai = root['info'].get('ai_will_do', {'base': 1})
        root_xp_cost = int(root['info'].get('xp_unlock_cost', 100))

        grand_entry = {
            'folder': category,
            'name': root['tag'],
            'description': f"{root['tag']}_DESC",
            'icon': grand_icon,
            'available': {
                'always': True
            },
            'xp_cost': root_xp_cost,
            'xp_type': group['xp_type'],
            'ai_will_do': root_ai,
            'tracks': track_order,
            'milestones': [
                _build_milestone(f"{grand_key}_{track_name}_milestone_var") for track_name in track_order
            ]
        }
        grand_entry = merge_dicts([grand_entry, root_effects])
        grands[category][grand_key] = grand_entry

        for track_name in track_order:
            if track_name not in group['tracks']:
                continue
            for option_name, option_nodes in group['tracks'][track_name].items():
                first_node = option_nodes[0]
                option_suffix = _slugify(option_name)
                sub_key = f"{grand_key}_{track_name}_{option_suffix}"
                if sub_key in subdoctrines[category]:
                    raise ValueError(f"Duplicate subdoctrine key `{sub_key}`.")

                sub_icon = f"GFX_doctrine_{sub_key}_medium"
                _register_doctrine_icon(first_node, sub_icon, sprite_defs, force=force)

                first_xp_cost = int(first_node['info'].get('xp_unlock_cost', 100))
                first_ai = first_node['info'].get('ai_will_do', {'base': 1})

                if len(option_nodes) == 1:
                    activation_effects = {}
                    reward_nodes = option_nodes
                else:
                    activation_effects = _extract_doctrine_effects(first_node['info'])
                    reward_nodes = option_nodes[1:]

                sub_entry = {
                    'track': track_name,
                    'name': first_node['tag'],
                    'description': f"{first_node['tag']}_DESC",
                    'icon': sub_icon,
                    'xp_cost': first_xp_cost,
                    'xp_type': group['xp_type'],
                    'available': {
                        'always': True
                    },
                    'ai_will_do': first_ai
                }
                sub_entry = merge_dicts([sub_entry, activation_effects])

                rewards = dict()
                for idx, reward_node in enumerate(reward_nodes, start=1):
                    reward_key = _slugify(reward_node['suffix'])
                    if reward_key in rewards:
                        reward_key = f"{reward_key}_{idx}"
                    rewards[reward_key] = _extract_doctrine_effects(reward_node['info'])
                    _add_reward_localisation(reward_locs, sub_key, reward_key, reward_node)
                sub_entry['rewards'] = rewards

                subdoctrines[category][sub_key] = sub_entry

    expected_counts = mapping.get('expected_counts', {})
    if expected_counts.get('grand_land', len(grands['land'])) != len(grands['land']):
        raise ValueError(f"Generated `{len(grands['land'])}` land grands, expected `{expected_counts.get('grand_land')}`.")
    if expected_counts.get('grand_air', len(grands['air'])) != len(grands['air']):
        raise ValueError(f"Generated `{len(grands['air'])}` air grands, expected `{expected_counts.get('grand_air')}`.")
    if expected_counts.get('sub_land', len(subdoctrines['land'])) != len(subdoctrines['land']):
        raise ValueError(f"Generated `{len(subdoctrines['land'])}` land subdoctrines, expected `{expected_counts.get('sub_land')}`.")
    if expected_counts.get('sub_air', len(subdoctrines['air'])) != len(subdoctrines['air']):
        raise ValueError(f"Generated `{len(subdoctrines['air'])}` air subdoctrines, expected `{expected_counts.get('sub_air')}`.")

    SaveJson(grands['land'], F(pjoin("data", "common", "doctrines", "grand_doctrines", "PIHC_land_grand_doctrines.json")), indent=4)
    SaveJson(grands['air'], F(pjoin("data", "common", "doctrines", "grand_doctrines", "PIHC_air_grand_doctrines.json")), indent=4)
    SaveJson(subdoctrines['land'], F(pjoin("data", "common", "doctrines", "subdoctrines", "land", "PIHC_land_subdoctrines.json")), indent=4)
    SaveJson(subdoctrines['air'], F(pjoin("data", "common", "doctrines", "subdoctrines", "air", "PIHC_air_subdoctrines.json")), indent=4)

    if len(sprite_defs) > 0:
        SaveJson(
            {'spriteTypes': merge_dicts(sprite_defs, d=True)},
            F(pjoin("data", "interface", "doctrines", "PIHC_doctrine_icons.json")),
            indent=4
        )

    if len(reward_locs) > 0:
        SaveLocs(
            reward_locs,
            name="PIHC_DOCTRINE_REWARDS",
            path=F(pjoin("data", "localisation")),
            replace=False,
            clear=True
        )

    return {
        'nodes': len(nodes),
        'grand_land': len(grands['land']),
        'grand_air': len(grands['air']),
        'sub_land': len(subdoctrines['land']),
        'sub_air': len(subdoctrines['air']),
    }
