import PIL
import PIL.Image
from ..utils import *
import pandas as pd
from collections import defaultdict

def ConvertStates(path):
    '''
    Convert the `states` folder to the `converted_states` folder.
    Args:
        path: str. The path to the `states` folder.
    Return:
        None
    '''
    ClearFolder(F("data/map/converted_states"), rm=True)
    CCLConvertBatch(
        src_path = path,
        tgt_path = F("data/map/converted_states"),
        format = 'json',
    )
    provs_table = pd.read_csv(F("map/definition.csv"), header=None, sep=';', dtype=str)
    provs_table.columns = ['Province ID', 'R value', 'G value', 'B value', 'Province type', 'Coastal status', 'Terrain', 'Continent']
    for state_file in [f for f in ListFiles(F("data/map/converted_states")) if f.endswith('.json')]:
        state_data = LoadJson(pjoin(F("data/map/converted_states"),state_file))
        state_data['state']['//Coastal'] = bool(provs_table.loc[state_data['state']['provinces'],'Coastal status'].any())
        state_data['state']['//Terrain'] = provs_table.loc[state_data['state']['provinces'],'Terrain'].value_counts().index[0]
        SaveJson(state_data, pjoin(F("data/map/converted_states"),state_file), indent=4)

def ConvertStrategicRegions(path):
    '''
    Convert the `strategicregions` folder to the `converted_strategicregions` folder.
    Args:
        path: str. The path to the `strategicregions` folder.
    Return:
        None
    '''
    ClearFolder(F("data/map/converted_strategicregions"), rm=True)
    CCLConvertBatch(
        src_path = path,
        tgt_path = F("data/map/converted_strategicregions"),
        format = 'json',
    )

def DeployStates():
    '''
    Deploy the `converted_states` folder to the `states` folder.
    Args:
        None
    Return:
        None
    '''
    CCLConvertBatch(
        src_path = F("data/map/converted_states"),
        tgt_path = F("history/states"),
        format = 'txt',
    )

def DeployStrategicRegions():
    '''
    Deploy the `converted_strategicregions` folder to the `strategicregions` folder.
    Args:
        None
    Return:
        None
    '''
    CCLConvertBatch(
        src_path = F("data/map/converted_strategicregions"),
        tgt_path = F("map/strategicregions"),
        format = 'txt',
    )

def NumStates():
    '''
    Count the number of states in the map. Only the converted states are counted.
    Args:
        None
    Return:
        int. The number of states in the map.
    '''
    return len([f for f in ListFiles(F("data/map/converted_states")) if f.endswith('.json')])

def BuildAdjacencyGraph(force=False):
    '''
    Convert the `provinces.bmp` and `definition.csv` to a graph of state adjacency, represented as a file `state_adjacency_graph.json`.
    Args:
        force: bool. If True, force to regenerate the graph.
    Return:
        None
    '''
    if ExistFile(F("data/map/state_adjacency_graph.json")) and not force:
        return
    img = PIL.Image.open(F("map/provinces.bmp")).convert('RGB')
    definition = pd.read_csv(F("map/definition.csv"), header=None, sep=';')
    color2prov = {(row[1], row[2], row[3]):int(i) for i, row in definition.iterrows()}
    color2type = {(row[1], row[2], row[3]):row[4] for i, row in definition.iterrows()}
    prov2state = {}; adjacency = defaultdict(set)
    for state in ListFiles(F("data/map/converted_states")):
        state_id = int(state.split('.')[0])
        state_data = LoadJson(pjoin(F("data/map/converted_states"),f"{state_id}.json"))
        provs = state_data['state']['provinces']
        for prov_id in provs:
            prov2state[prov_id] = state_id
    SaveJson({repr(k):v for k, v in color2prov.items()}, F("data/map/color2prov.json"), indent=4)
    SaveJson(prov2state, F("data/map/prov2state.json"), indent=4)

    def link_state(x, y, a, b):
        if (x,y)==(a,b) or min(x,y,a,b) < 0 or max(x,a)>=img.size[0] or max(y,b)>=img.size[1]: return
        A = img.getpixel((x,y)); B = img.getpixel((a,b))
        if A==B or color2type[A]!='land' or color2type[B]!='land': return
        pA = color2prov[A]; pB = color2prov[B]
        if pA==pB: return
        sA = prov2state[pA]; sB = prov2state[pB]
        if sA==sB: return
        adjacency[sA].add(sB)
        adjacency[sB].add(sA)

    for x in TQDM(img.size[0], desc='Building adjacency graph...'):
        for y in range(img.size[1]):
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    link_state(x,y,x+dx,y+dy)

    SaveJson(dict(sorted([(v,sorted(list(s))) for v, s in adjacency.items()])),F("data/map/state_adjacency_graph.json"),indent=4)

def StateCountriesFlooding(state_tags, keys=['owner', 'add_core_of']):
    '''
    Flood the country tags to the states. The graph of state adjacency is required to be prepared in advance (`BuildAdjacencyGraph()`).
    Args:
        state_tags: List[Tuple[str,str]] or List[Tuple[str,str,int]]. List of (state_id, country_tag, depth). If omitted the depth will be infinite.
        keys: List[str]. List of keys to be flooded.
    Return:
        None
    '''
    adjacency = {int(k):set(v) for k,v in LoadJson(F("data/map/state_adjacency_graph.json")).items()}
    queue = [(state_tag[0], state_tag[1], (9999999 if len(state_tag)==2 else state_tag[2])) for state_tag in state_tags]
    states = set([tag[0] for tag in state_tags])

    while queue:
        state_id, tag, depth = queue.pop(0)
        state_data = LoadJson(pjoin(F("data/map/converted_states"),f"{state_id}.json"))
        
        for key in keys:
            state_data['state']['history'][key] = tag
        SaveJson(state_data, pjoin(F("data/map/converted_states"),f"{state_id}.json"), indent=4)
        
        if (state_id in adjacency) and (depth>0):
            for n in adjacency[state_id]:
                if n not in states:
                    queue.append((n,tag,depth-1)); states.add(n)

def StateContinentsFlooding(state_tags):
    '''
    Flood the continent tags to the provinces. The graph of state adjacency is required to be prepared in advance (`BuildAdjacencyGraph()`).
    Args:
        state_tags: List[Tuple[str,str]] or List[Tuple[str,str,int]]. List of (state_id, continent_tag, depth). If omitted the depth will be infinite.
    Return:
        None
    '''
    adjacency = {int(k):set(v) for k,v in LoadJson(F("data/map/state_adjacency_graph.json")).items()}
    queue = [(state_tag[0], state_tag[1], (9999999 if len(state_tag)==2 else state_tag[2])) for state_tag in state_tags]
    states = set([tag[0] for tag in state_tags])
    
    provs_table = pd.read_csv(F("map/definition.csv"), header=None, sep=';', dtype=str)
    provs_table.columns = ['Province ID', 'R value', 'G value', 'B value', 'Province type', 'Coastal status', 'Terrain', 'Continent']
    while queue:
        state_id, tag, depth = queue.pop(0)
        state_data = LoadJson(pjoin(F("data/map/converted_states"),f"{state_id}.json"))
        
        provs = state_data['state']['provinces']
        for prov_id in provs:
            provs_table.loc[prov_id,'Continent'] = tag
        
        if (state_id in adjacency) and (depth>0):
            for n in adjacency[state_id]:
                if n not in states:
                    queue.append((n,tag,depth-1)); states.add(n)
    provs_table.to_csv(F("map/definition.csv"), header=None, sep=';', index=False, lineterminator='\r\n')