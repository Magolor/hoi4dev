# ================================== #
# ==== CHAPTER 1: Build The Map ==== #
# ================================== #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# The map is already copied to the mod, so we can use them directly.
# First convert all our states to json. Then build the adjacency graph.
ConvertStates("resources/states")
BuildAdjacencyGraph(force=False)
...

# %%
# Also we need to conver the strategic regions to json.
ConvertStrategicRegions("resources/strategicregions")

# %%
# First we define the continents.
state_continent_tags = (
    [(x, 1) for x in [369,]] +
    [(x, 2) for x in [69,]] +
    [(x, 3) for x in [478,]] +
    [(x, 4) for x in [772,]] +
    [(x, 5) for x in [288,]] +
    [(x, 6) for x in [228,]] +
    [(x, 7) for x in [252, 372, 866,]]
)
# After defining the state-tags pair, we can populate the owner tags to all the states.
StateContinentsFlooding(state_continent_tags)
# But a few states are assigned incorrectly, let's manually fix them by limiting the flooding depth = 0 (not flooding, single point modification).
state_continent_corrections = (
    [(x, 1, 0) for x in [432,  46, 336,  37, 376, 360, 364, 355, 409,  52, 418, 386, 522, 581,]] +
    [(x, 2, 0) for x in [502,]]
)
StateContinentsFlooding(state_continent_corrections)

# %%
# Similarly, we can define the country each state belongs.
# Now, define the geographically important states for each of the countries.
# Here, we have 31 countries with tag from 1 to 31, we select the states for each of them
state_tags = (
    [(x, "C01") for x in [369, 459,  24, 367, 431, 487, 439, 434,]] +
    [(x, "C02") for x in [504, 500, 545, 567, 514, 235, 565,]] +
    [(x, "C03") for x in [410, 441, 426, 446, 436, 400,]] +
    [(x, "C04") for x in [336, 376,  37,]] +
    [(x, "C05") for x in [528,]] +
    [(x, "C06") for x in [450, 888, 518, 506,   4, 415, 401, 665,]] +
    [(x, "C07") for x in [102, 562, 544, 647, 694,]] +
    [(x, "C08") for x in [375,  34, 344, 361, 362, 413, 391, 402, 403, 404,]] +
    [(x, "C09") for x in [449, 409, 447, 482, 418, 386,  52, 355, 364, 491, 475,]] +
    [(x, "C10") for x in [486, 517, 494, 539, 470, 520,]] +
    [(x, "C11") for x in [ 69,  99, 600, 425, 593,  88, 534,]] +
    [(x, "C12") for x in [635, 686,]] +
    [(x, "C13") for x in [242,  12, 609, 695,]] +
    [(x, "C14") for x in [190,]] +
    [(x, "C15") for x in [  3, 303, 351, 277, 282, 317, 322, 295, 299, 285, 249, 880,   2,]] +
    [(x, "C16") for x in [522, 531, 581, 526,]] +
    [(x, "C17") for x in [ 80,]] +
    [(x, "C18") for x in [772,]] +
    [(x, "C19") for x in [478, 538]] +
    [(x, "C20") for x in [673,]] +
    [(x, "C21") for x in [ 21, 297, 304,]] +
    [(x, "C22") for x in [ 56,  97, 428, 463, 884, 885, 886,  64,]] +
    [(x, "C23") for x in [252, 866, 164, 778, 757, 146, 187, 176, 150, 738,]] +
    [(x, "C24") for x in [860, 155,]] +
    [(x, "C25") for x in [843, 703, 198, 167,  59, 178, 882, 166,  79,  85,  89, 889, 182, 109, 229, 147,  62, 887,  91, 124, 130, 134, 120, 162]] +
    [(x, "C26") for x in [170,  16,  25, 255,   9, 250,  22, 245, 239,  28, 222, 218, 248, 851,  19,  36,  13,  18,  23, 314,]] +
    [(x, "C27") for x in [196, 783,]] +
    [(x, "C28") for x in [895, 863, 371, 216,]] +
    [(x, "C29") for x in [372,]] +
    [(x, "C30") for x in [740, 631, 122, 704,]]
)
# After defining the state-tags pair, we can populate the owner tags to all the states.
StateCountriesFlooding(state_tags, keys=['owner', 'add_core_of'])
# But a few states are assigned incorrectly, let's manually fix them by limiting the flooding depth = 0 (not flooding, single point modification).
state_tag_corrections = (
    [(x, "C00", 0) for x in [299, 319,  34, 344, 362, 243, 236, 270, 872, 194, 862, 846, 247, 237, 189, 841, 836, 806, 802, 803, 158, 728, 138, 106, 143, 159, 750, 136, 768, 148, 724, 761, 791, 814, 125, 135, 763, 776, 753, 799, 114, 794, 104, 127, 655, 749, 726, 337, 854, 168, 808, 738, 643,  29, 714, 145, 707, 175,  78, 861, ]] +
    [(x, "C01", 0) for x in [369, 404]] +
    [(x, "C02", 0) for x in [504, 590]] +
    [(x, "C03", 0) for x in [412]] +
    [(x, "C04", 0) for x in [336]] +
    [(x, "C05", 0) for x in [528, 546, 524, 215, 565, 48]] +
    [(x, "C06", 0) for x in [888, 585, 606, 619]] +
    [(x, "C07", 0) for x in [562, 694]] +
    [(x, "C08", 0) for x in [389]] +
    [(x, "C09", 0) for x in [432]] +
    [(x, "C10", 0) for x in [539]] +
    [(x, "C11", 0) for x in [ 69, 502]] +
    [(x, "C12", 0) for x in [601, 582, 558, 544, 624, 644, 652, 563]] +
    [(x, "C13", 0) for x in [718, 680]] +
    [(x, "C14", 0) for x in [190, 577, 589, 587,  86, 599]] +
    [(x, "C15", 0) for x in [  3, 315, 348]] +
    [(x, "C16", 0) for x in [561, 44]] +
    [(x, "C17", 0) for x in [ 80]] +
    [(x, "C18", 0) for x in [772, 883]] +
    [(x, "C19", 0) for x in [478, 570, 292, 420, 460, 516, 65]] +
    [(x, "C20", 0) for x in [673]] +
    [(x, "C21", 0) for x in [309]] +
    [(x, "C22", 0) for x in [ 56]] +
    [(x, "C23", 0) for x in [252]] +
    [(x, "C24", 0) for x in [197, 233, 870, 866, 199, 823, 172]] +
    [(x, "C25", 0) for x in [843, 200, 204]] +
    [(x, "C26", 0) for x in [ 45, 786, 850]] +
    [(x, "C27", 0) for x in [196]] +
    [(x, "C28", 0) for x in [863, 897, 271]] +
    [(x, "C29", 0) for x in [372]] +
    [(x, "C30", 0) for x in [740, 737, 152, 893, 141, 760, 160,   8, 785, 830, 757]] +
    [(x, "C31", 0) for x in [610, 609, 611, 666, 722, 649]] +
    
    [(x, "C33", 0) for x in [411, 361, 403]] +
    [(x, "C34", 0) for x in [775, 735, 121, 767, 670, 227]] +
    [(x, "C35", 0) for x in [752, 747, 149, 150, 154, 733, 58, 778, 176, 774, 161, 634, 800, 195, 807, 805, 188, 193, 835, 790, 789, 795, 786, 796, 804, 832, 824, 822, 827, 829, 825, 852, 838, 897, 755, 769, 818]] +
    [(x, "C36", 0) for x in [164]] +
    [(x, "C39", 0) for x in [890, 658, 663]] +
    [(x, "C40", 0) for x in [633]] +
    [(x, "C41", 0) for x in [38, 151]] +
    [(x, "C42", 0) for x in [659]] +
    [(x, "C43", 0) for x in [647, 661, 688, 694, 748]]
)
StateCountriesFlooding(state_tag_corrections, keys=['owner', 'add_core_of'])

# %%
# As PIHC map is already assigned with buildings, we don't generate new buildings
# GenerateBuildings()

# %%
# PIHC now uses a delta file to fine-tune the buildings.
delta = LoadJson(pjoin("resources", "buildings_delta.json"))
for building_type in delta:
    for state_prov_id in delta[building_type]:
        if '-' in state_prov_id:
            state_id, prov_id = state_prov_id.split('-')
        else:
            state_id, prov_id = state_prov_id, None
        state_data = LoadJson(pjoin(F("data/map/converted_states"),f"{state_id}.json"))
        if 'buildings' not in state_data['state']['history']:
            state_data['state']['history']['buildings'] = dict()
        if state_data['state']['history']['buildings'] == list():
            state_data['state']['history']['buildings'] = dict()
        buildings = state_data['state']['history']['buildings']
        if prov_id is not None:
            if prov_id not in buildings:
                buildings[prov_id] = dict()
            building_scope = buildings[prov_id]
        else:
            building_scope = buildings
        building_scope[building_type] = delta[building_type][state_prov_id] + (0 if building_type not in building_scope else building_scope[building_type])
        if building_scope[building_type] <= 0:
            building_scope.pop(building_type)
        SaveJson(state_data, pjoin(F("data/map/converted_states"),f"{state_id}.json"), indent=4)

# %%
# The old PIHC map has a different resource distribution than the current mod, so we would like to generate new resources (manually).
# for state in ListFiles(F("data/map/converted_states")):
#     state_id = int(state.split('.')[0])
#     state_data = LoadJson(pjoin(F("data/map/converted_states"),f"{state_id}.json"))
#     state_data['state']['resources'] = list()
#     SaveJson(state_data, pjoin(F("data/map/converted_states"),f"{state_id}.json"), indent=4)
# GenerateResources()

# %%
# PIHC now uses a delta file to fine-tune the resources.
delta = LoadJson(pjoin("resources", "resources_delta.json"))
for resource_type in delta:
    for state_id in delta[resource_type]:
        state_data = LoadJson(pjoin(F("data/map/converted_states"),f"{state_id}.json"))
        if state_data['state']['resources'] == list():
            state_data['state']['resources'] = dict()
        state_data['state']['resources'][resource_type] = max(0, delta[resource_type][state_id] + (0 if resource_type not in state_data['state']['resources'] else state_data['state']['resources'][resource_type]))
        if state_data['state']['resources'][resource_type] == 0:
            state_data['state']['resources'].pop(resource_type)
        SaveJson(state_data, pjoin(F("data/map/converted_states"),f"{state_id}.json"), indent=4)

# Let's add weather to strategic regions.
# As PIHC is a story with Windidos taking important roles, there will be snow more frequently.
# Temporarily, we directly take the stats from Southern Norway and apply it to all strategic regions.
for sr in ListFiles(F("data/map/converted_strategicregions")):
    data = LoadJson(pjoin(F("data/map/converted_strategicregions"), sr))
    data['strategic_region']['weather'] = LoadJson(pjoin("resources", "weather.json"))['weather']
    SaveJson(data, pjoin(F("data/map/converted_strategicregions"), sr), indent=4)

# Victory Points re-distirbution
prov2state = LoadJson(pjoin(F("data/map"), "prov2state.json"))
with open("resources/delta_vic.txt","r") as f:
    for line in f:
        values = line.strip().split()
        if values[0] == '+':
            assert (len(values)==3)
            vp, prov_id = values[1], values[2]
            state_id = prov2state[prov_id]
            state_data = LoadJson(pjoin(F("data/map/converted_states"),f"{state_id}.json"))
            for key in dup_gen('victory_points'):
                if key not in state_data['state']['history']:
                    state_data['state']['history'][key] = [prov_id, vp]; break
                elif int(prov_id) == int(state_data['state']['history'][key][0]):
                    state_data['state']['history'][key] = [prov_id, vp]; break
            SaveJson(state_data, pjoin(F("data/map/converted_states"),f"{state_id}.json"), indent=4)
        if values[0] == '-':
            assert (len(values)==2)
            prov_id = values[1]
            state_id = prov2state[prov_id]
            state_data = LoadJson(pjoin(F("data/map/converted_states"),f"{state_id}.json"))
            vic_points = []
            for key in dup_gen('victory_points'):
                if key not in state_data['state']['history']:
                    break
                else:
                    if int(prov_id) != int(state_data['state']['history'][key][0]):
                        vic_points.append(state_data['state']['history'][key])
                    del state_data['state']['history'][key]
            for vic_point in vic_points:
                state_data['state']['history'][find_dup('victory_points', state_data['state']['history'])] = vic_point
            SaveJson(state_data, pjoin(F("data/map/converted_states"),f"{state_id}.json"), indent=4)

# Category re-distribution
# zh_cat_mapping = {
#     '飞地': 'enclave',
#     '荒地': 'wasteland',
#     '小岛': 'tiny_island',
#     '小岛屿': 'small_island',
#     '田园': 'pastoral',
#     '农村': 'rural',
#     '城镇': 'town',
#     '大城镇': 'large_town',
#     '城市': 'city',
#     '大城市': 'large_city',
#     '大都会': 'metropolis',
#     '特大都会': 'megalopolis',
# }
# with open("resources/delta_category.txt","r") as f:
#     for line in f:
#         values = [v for v in line.strip().split() if v]
#         assert ((len(values) > 1) and (values[-1] in zh_cat_mapping)), f"Invalid line: {line}"
#         for v in values[:-1]:
#             state_id = int(v)
#             state_data = LoadJson(pjoin(F("data/map/converted_states"),f"{state_id}.json"))
#             state_data['state']['state_category'] = zh_cat_mapping[values[-1]]
#             SaveJson(state_data, pjoin(F("data/map/converted_states"),f"{state_id}.json"), indent=4)
# 
# 
# # %%
# # Next let's generate a random state stats according to a given distribution.
# # The random manpower and buildings generation assumes that the state_category is already assigned.
# GenerateManpower()

# %%
# Now let's finish states editing by converting the states back to the CCL. Also we need to convert the strategic regions back to the CCL.
DeployStates()
DeployStrategicRegions()

# %%
# Regarding localisation, PIHC has some predefined state translations, let's convert them to the true localisation.
locs = LoadJson(pjoin("resources", "state_names.json"))
languages = get_mod_config('languages')
num_states = get_num_states()
for i in range(num_states):
    k = f"{i+1}"
    if k not in locs:
        locs[k] = {}
    if 'chinese' in locs[k]:
        locs[k]['zh'] = locs[k].pop('chinese')
    if 'english' in locs[k]:
        locs[k]['en'] = locs[k].pop('english')
    if 'chinese_alt' in locs[k]:
        locs[k].pop('chinese_alt')
    for l in languages:
        if l not in locs[k]:
            locs[k][l] = f"STATE_{i+1}"
locs = {"STATE_"+k: v for k, v in sorted(locs.items(), key=lambda item: int(item[0]))}
SaveLocs(locs, name="state_names", path=F("localisation"))

vp_locs = {}
for i in range(num_states):
    state_data = LoadJson(pjoin(F("data/map/converted_states"), f"{i+1}.json"))
    for key in dup_gen('victory_points'):
        if key in state_data['state']['history']:
            prov_id, vp = state_data['state']['history'][key]
            vp_locs[f"VICTORY_POINTS_{prov_id}"] = locs[f"STATE_{i+1}"]
        else:
            break
SaveLocs(vp_locs, name="victory_points", path=F("localisation"))
# %%
# Similar for strategic regions.
locs = LoadJson(pjoin("resources", "strat_region_names.json"))
languages = get_mod_config('languages')
num_states = get_num_states()
for i in range(num_states):
    k = f"{i+1}"
    if k not in locs:
        locs[k] = {}
    if 'chinese' in locs[k]:
        locs[k]['zh'] = locs[k].pop('chinese')
    if 'english' in locs[k]:
        locs[k]['en'] = locs[k].pop('english')
    if 'chinese_alt' in locs[k]:
        locs[k].pop('chinese_alt')
    for l in languages:
        if l not in locs[k]:
            locs[k][l] = f"STRATEGICREGION_{i+1}"
locs = {"STRATEGICREGION_"+k: v for k, v in sorted(locs.items(), key=lambda item: int(item[0]))}
SaveLocs(locs, name="strategic_region_names", path=F("localisation"))