from ..utils import *
from ..translation import PopulateLocs

def AddDivisions(path):
    '''
    Add divisions for all countries to the mod.
    Args:
        path: str. The path of the resource files of the divisions. The resources should include the divisions definition and a global localisation template for each country, in which `<TYPE>` is replaced for different divisions.
    Return:
        None
    Notice the division names will only take effect for the primary language, thus no translation is needed.
    '''
    division_files = [f for f in ListFiles(path) if f.endswith('.json')]
    divisions = [LoadJson(pjoin(path, f)) for f in division_files if f.endswith('.json')]
    locs_file = pjoin(path,"locs.txt")
    locs = ReadTxtLocs(locs_file) if ExistFile(locs_file) else {}
    language = get_mod_config('languages')[0]
    for key in locs:
        if key.startswith('TYPE_'): continue
        template = locs[key][language]
        en_template = locs[key]['en']
        names_groups = []; division_templates = []; division_templates_not_loaded = []
        for division, file in zip(divisions, division_files):
            div = deepcopy(division)
            name = div.pop('name', None)
            load = div.pop('load', True)
            tag = "NAMES_GROUP_" + '_'.join([key,file.split('.')[0]]).upper()
            loc = locs["TYPE_"+file.split('.')[0]][language]
            en_loc = locs["TYPE_"+file.split('.')[0]]['en']
            designation = template.replace("<TYPE>", loc)
            en_designation = en_template.replace("<TYPE>", en_loc)
            name = f"{designation.split('%d')[0]} ({en_designation.split(' %d')[0]})"
            regiments = div.pop('regiments')
            support = div.pop('support')
            division_types = list(set([s for row in regiments for s in row] + [s for row in support for s in row]))
            names_group = { tag: {
                "name": name,
                "for_countries": [key],
                "can_use": {"always": True},
                "division_types": division_types,
                "fallback_name": f"{designation} ({en_designation})",
            } }
            division_template = { "division_template": merge_dicts([{
                "name": name,
                "regiments": merge_dicts([
                    {s: {"x": i, "y": j}}
                    for i, row in enumerate(regiments)
                    for j, s in enumerate(row)
                ], d=True),
                "support": merge_dicts([
                    {s: {"x": i, "y": j}}
                    for i, row in enumerate(support)
                    for j, s in enumerate(row)
                ], d=True),
                "division_names_group": tag,
            }, div]) }
            names_groups.append(names_group)
            if load:
                division_templates.append(division_template)
            else:
                division_templates_not_loaded.append(division_template)
        SaveJson(merge_dicts(names_groups, d=True), F(pjoin("data", "common", "units", "names_divisions", f"{key}.json")), indent=4)
        SaveJson(merge_dicts(division_templates, d=True), F(pjoin("data", "history", "units", f"{key}.json")), indent=4)
        SaveJson(merge_dicts(division_templates_not_loaded, d=True), F(pjoin("data", "history", "units", f"{key}_hidden.json")), indent=4)

def AddInitialArmy(path):
    '''
    Add initial army for a country to the mod.
    Args:
        path: str. The path of the resource files of the country. The resources should include the 'units.json' file.
    Return:
        None
    Notice that the country's unit history should be compiled before adding initial army. That is, the `data/history/units/<tag>.json` should exist.
    '''
    tag = path.strip('/').split('/')[-1].upper()
    if not ExistFile(pjoin(path,"units.json")):
        return
    history = merge_dicts([
        LoadJson(F(pjoin("data","history","units",f"{tag}.json"))),
        LoadJson(F(pjoin("data","history","units",f"{tag}_hidden.json")))
    ], d=True)
    mapping = {}
    for key in history:
        if find_ori(key)=='division_template':
            mapping[history[key]['division_names_group']] = history[key]['name']
    units = LoadJson(pjoin(path,"units.json"))
    initial_army = []
    for key in units:
        for i, div in enumerate(units[key]):
            division_names_group = f"NAMES_GROUP_{tag}_{key.upper()}"
            initial_army.append({'division': {
                "division_name": {
                    "is_name_ordered": True,
                    "name_order": i+1,
                },
                "division_template": mapping[division_names_group],
            } | div})
    Edit(
        F(pjoin("data","history","units",f"{tag}.json")),
        {'$units': merge_dicts(initial_army, d=True)}, d=True
    )