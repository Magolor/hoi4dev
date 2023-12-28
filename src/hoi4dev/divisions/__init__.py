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
    divisions = [LoadJson(pjoin(path, f)) for f in division_files]
    locs_file = pjoin(path,"locs.txt")
    locs = ReadTxtLocs(locs_file) if ExistFile(locs_file) else {}
    language = get_mod_config('languages')[0]
    for key in locs:
        if key.startswith('TYPE_'): continue
        template = locs[key][language]
        names_groups = []; division_templates = []
        for division, file in zip(divisions, division_files):
            div = deepcopy(division)
            name = div.pop('name', None)
            tag = "NAMES_GROUP_" + '_'.join([key,file.split('.')[0]]).upper()
            loc = locs["TYPE_"+file.split('.')[0]][language]
            designation = template.replace("<TYPE>", loc)
            regiments = div.pop('regiments')
            support = div.pop('support')
            division_types = list(set([s for row in regiments for s in row] + [s for row in support for s in row]))
            names_group = { tag: {
                "name": '"' + designation.split('%d')[0] + '"',
                "for_countries": [key],
                "can_use": {"always": True},
                "division_types": division_types,
                "fallback_name": '"' + designation + '"',
            } }
            division_template = { "division_template": merge_dicts([{
                "name": '"' + designation.split('%d')[0] + '"',
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
            division_templates.append(division_template)
        SaveJson(merge_dicts(names_groups, d=True), F(pjoin("data", "common", "units", "names_divisions", f"{key}.json")), indent=4)
        SaveJson(merge_dicts(division_templates, d=True), F(pjoin("data", "history", "units", f"{key}.json")), indent=4)
        