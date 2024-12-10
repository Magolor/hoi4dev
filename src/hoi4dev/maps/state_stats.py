from ..utils import *
import numpy as np

def hard_gaussian(mu, sigma, bound=3):
    return int(
        mu * max(0,np.clip(
            1+sigma*np.random.normal(),
            a_min=1-bound*sigma,
            a_max=1+bound*sigma
        ))
    )

def RandomManpower(state_category):
    '''
    Generate a random manpower for a state.
    Args:
        state_category: str. The category of the state.
    Return:
        int. The manpower of the state.
    
    The default category-to-average-manpower table is stored at `hoi4dev_settings/configs/manpower.json` in the mod folder. You can modify it to change the average manpower of each category type.
    This formula only consider the category of the state, instaed of the size of the state.
    The manpower of the state is generated from a Gaussian distribution with 3x std hard limit.
    '''
    manpower_config = LoadJson(F(pjoin("hoi4dev_settings","configs","manpower.json")))
    return hard_gaussian(manpower_config['mean'][state_category], manpower_config['std'])

def GenerateManpower():
    '''
    Generate random manpower for all states.
    Args:
        None
    Return:
        None
    
    Please refer to `RandomManpower()` for the random generation formula.
    '''
    for state_file in [f for f in ListFiles(F("data/map/converted_states")) if f.endswith('.json')]:
        state_data = LoadJson(pjoin(F("data/map/converted_states"),state_file))
        state_data['state']['manpower'] = RandomManpower(state_data['state']['state_category'])
        SaveJson(state_data, pjoin(F("data/map/converted_states"),state_file), indent=4)

def random_progression(probs):
    for i in range(len(probs)):
        if np.random.rand()<=probs[i]:
            continue
        return i
    else:
        return len(probs)

def RandomBuildings(state_category, is_coastal=False):
    '''
    Generate a random buildings distribution for a state.
    Args:
        state_category: str. The category of the state.
        is_coastal: bool. If True, the state is coastal.
    Return:
        int. The manpower of the state.
    
    The default category-to-buildings table is stored at `hoi4dev_settings/configs/buildings.json` in the mod folder. You can modify it to change the average builings of each category type.
    '''
    buildings_config = LoadJson(F(pjoin("hoi4dev_settings","configs","buildings.json")))
    buildings = dict()
    for building_type, probs in buildings_config['probs'][state_category].items():
        num = random_progression(probs)
        if num: buildings[building_type] = num
    if is_coastal:
        num = random_progression(buildings_config['dockyard'])
        if num: buildings['dockyard'] = num
    return buildings

def GenerateBuildings(behavior='max'):
    '''
    Generate random buildings for all states.
    Args:
        behavior: str. 'max', 'add', or 'replace'. If 'max', the generated buildings will be merged with the existing buildings, and the maximum value will be used. If 'add', the generated buildings will be merged with the existing buildings, and the values will be added. If 'replace', the generated buildings will replace the existing buildings.
    Return:
        None
    
    Please refer to `RandomBuildings()` for the random generation formula.
    '''
    for state_file in [f for f in ListFiles(F("data/map/converted_states")) if f.endswith('.json')]:
        state_data = LoadJson(pjoin(F("data/map/converted_states"),state_file))
        random_buildings = RandomBuildings(state_data['state']['state_category'], is_coastal=state_data['state']['//Coastal'])
        if not state_data['state']['history']['buildings']:
            state_data['state']['history']['buildings'] = dict()
        for k in random_buildings:
            if k not in state_data['state']['history']['buildings']:
                state_data['state']['history']['buildings'][k] = random_buildings[k]
            else:
                state_data['state']['history']['buildings'][k] = {
                    'max': lambda x,y: max(x,y),
                    'add': lambda x,y: x+y,
                    'replace': lambda x,y: y
                }[behavior](random_buildings[k], state_data['state']['history']['buildings'][k])
        SaveJson(state_data, pjoin(F("data/map/converted_states"),state_file), indent=4)

def RandomResources(state_category, state_terrain="unknown"):
    '''
    Generate a random resources distribution for a state.
    Args:
        state_category: str. The category of the state.
        state_terrain: str. The terrain of the state.
    Return:
        int. The manpower of the state.
    
    The default category-to-resources table is stored at `hoi4dev_settings/configs/resources.json` in the mod folder. You can modify it to change the average resources of each category type.
    '''
    resources_config = LoadJson(F(pjoin("hoi4dev_settings","configs","resources.json")))
    resources = dict()
    for resource_type, probs in resources_config['probs'][state_category].items():
        num = random_progression(probs)
        if num: resources[resource_type] = num*resources_config['units'][resource_type]
    for resource_type, probs in resources_config['probs'][state_terrain].items():
        num = random_progression(probs)
        if num: resources[resource_type] = num*resources_config['units'][resource_type] + (resources[resource_type] if resource_type in resources else 0)
    return resources

def GenerateResources(behavior='max'):
    '''
    Generate random resources for all states.
    Args:
        behavior: str. 'max', 'add', or 'replace'. If 'max', the generated resources will be merged with the existing resources, and the maximum value will be used. If 'add', the generated resources will be merged with the existing resources, and the values will be added. If 'replace', the generated resources will replace the existing resources.
    Return:
        None
    
    Please refer to `RandomResources()` for the random generation formula.
    '''
    for state_file in [f for f in ListFiles(F("data/map/converted_states")) if f.endswith('.json')]:
        state_data = LoadJson(pjoin(F("data/map/converted_states"),state_file))
        random_resources = RandomResources(state_data['state']['state_category'], state_terrain=state_data['state']['//Terrain'])
        if not state_data['state']['resources']:
            state_data['state']['resources'] = dict()
        for k in random_resources:
            if k not in state_data['state']['resources']:
                state_data['state']['resources'][k] = random_resources[k]
            else:
                state_data['state']['resources'][k] = {
                    'max': lambda x,y: max(x,y),
                    'add': lambda x,y: x+y,
                    'replace': lambda x,y: y
                }[behavior](random_resources[k], state_data['state']['resources'][k])
        SaveJson(state_data, pjoin(F("data/map/converted_states"),state_file), indent=4)