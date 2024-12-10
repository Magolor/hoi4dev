from ..utils import *
from ..translation import AddLocalisation

def CreateDefaultFocusTree(path, info=dict()):
    '''
    Create a default focus tree resource folder.
    Args:
        path: str. The path of the target resource folder of the focus tree.
        info: Dict. The focus tree definition.
    Return:
        None
    '''
    CreateFolder(path)
    SaveJson(merge_dicts([{
        "default": "no",
        "continuous_focus_position": {
            "x": 0, "y": 0,
        },
    }, info]), pjoin(path,"info.json"), indent=4)

def AddNationalFocus(path, tree, translate=True):
    '''
    Add a focus to a given national focus tree. The focus 'parent' (None if it is the root of the focus tree) and focus 'tree' should be specified in the focus definition. Notice that the 'parent' should be the parent in geometric position, not the focus tree. Use 'prerequisites' to refer to the parent in the focus tree as in HoI4.
    Args:
        path: str. The path of the resource files of the focus. The resources should include the focus icon, the focus definition and the localisation.
        tree: str. The id of the focus tree to which the focus belongs.
        translate: bool. Whether to translate the localisation of the focus.
    Return:
        None
    Please note that the added national focus is not automatically compiled. Explicitly invoking `AddFocusTree()` for the focus tree it belongs is required to make the national focus work.
    Thhe focus's positioning is automatically adjusted within the focus tree. You can use 'dx' and 'dy' to adjust the relative position AFTER the automatical positioning (that is, the entire subtree will be shifted by 'dx' and 'dy'). Or use 'x' and 'y' to force the focus to be placed at the given position ('x' and 'y' must be specified simultaneously), which is recommended for the root. You can also use 'dw' or 'dc' to adjust the width of the subtree of this focus. You can use 'priority' to adjust the priority of the focus (the higher the priority, the more likely the focus will be placed on the left among its siblings).
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        "id": f"FOCUS_{tag}",
        "icon": f"GFX_FOCUS_{tag}_icon",
        "ai_will_do": {"factor": 1},
        "x": None, "y": None,
        "dx": 0, "dy": 0, "dw": 0,
        "px": 0, "py": 0, "pw": 0,
        "dc": 0,
        "priority": 0,
        "parent": None,
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    tree = info.pop('tree', tree)
    assert not((info['x'] is None)^(info['y'] is None)), "If specified, the focus's x and y should be specified simultaneously!"
    
    # Add focus localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"FOCUS_{tag}", translate=translate)
    
    # Initialize focus definition (A default focus tree is added if not exists)
    tree_path = F(pjoin("data","focus_trees",tree))
    if not ExistFile(pjoin(tree_path, "info.json")):
        CreateDefaultFocusTree(tree_path, {'id': tree})
    Edit(F(pjoin("data","focus_trees",tree,f"FOCUS_{tag}.json")), info)
    
    # Add focus icons
    scales = get_mod_config('img_scales'); w, h = scales['focus']
    icon = ImageFind(pjoin(path,"default"))
    if icon is None:
        icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_focus")), find_default=False)
        assert (icon is not None), "The default focus icon is not found!"
    icon = ImageZoom(icon, w=w, h=h)
    ImageSave(icon, F(pjoin("gfx","interface","goals",f"FOCUS_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","focuses",f"FOCUS_{tag}.json")), {'spriteTypes': {
        'spriteType': {
            "name": f"GFX_FOCUS_{tag}_icon",
            "texturefile": pjoin("gfx","interface","goals",f"FOCUS_{tag}.dds")
        },
        'spriteType__D1': {
            "name": f"GFX_FOCUS_{tag}_icon_shine",
            "texturefile": pjoin("gfx","interface","goals",f"FOCUS_{tag}.dds"),
            "effectFile": "gfx/FX/buttonstate.lua",
            "animation": {
                "animationmaskfile": pjoin("gfx","interface","goals",f"FOCUS_{tag}.dds"),
                "animationtexturefile": "gfx/interface/goals/shine_overlay.dds",
                "animationrotation": -90.0,
                "animationlooping": False,
                "animationtime": 0.75,
                "animationdelay": 0,
                "animationblendmode": "add",
                "animationtype": "scrolling",
                "animationrotationoffset": {
                    "x": 0.0,
                    "y": 0.0
                },
                "animationtexturescale": {
                    "x": 2.0,
                    "y": 1.0
                },
            },
            "animation__D1": {
                "animationmaskfile": pjoin("gfx","interface","goals",f"FOCUS_{tag}.dds"),
                "animationtexturefile": "gfx/interface/goals/shine_overlay.dds",
                "animationrotation": 90.0,
                "animationlooping": False,
                "animationtime": 0.75,
                "animationdelay": 0,
                "animationblendmode": "add",
                "animationtype": "scrolling",
                "animationrotationoffset": {
                    "x": 0.0,
                    "y": 0.0
                },
                "animationtexturescale": {
                    "x": 1.0,
                    "y": 1.0
                }
            },
            "legacy_lazy_load": False,
        },
    }})

class FocusNode:
    def __init__(self, path):
        self.d = LoadJson(path)
        self.parent = None
        self.children = []
        self.depth = 0

    def position(self, x=0, y=0):
        if self.d['x']!=None and self.d['y']!=None:
            self.d['px'] = self.d['x']; self.d['py'] = self.d['y']
        else:
            self.d['px'] = x+self.d['dx']; self.d['py'] = y+self.d['dy']
        x_ = self.d['px']-self.d['dw']//2+self.d['dc']; y_ = self.d['py']+1
        for c in sorted(self.children, key=lambda c: (-c.d['priority'],c.d['id'])):
            c.position(x_, y_); x_ += c.d['pw']
    
    def final(self):
        return {k:v for k,v in self.d.items() if k not in ['x','y','px','py','pw','dx','dy','dw','dc','parent','priority']} | {'x':self.d['px']+self.d['pw']//2,'y':self.d['py']}

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

def CompileFocusTree(path):
    '''
    Compile the focus tree.
    Args:
        path: str. The path of the resource folder of the focus tree.
    Return:
        None
    '''
    tree = path.strip('/').split('/')[-1].upper()
    nodes = {Prefix(file):FocusNode(pjoin(path,file)) for file in ListFiles(path) if file.endswith('.json') and file!='info.json'}
    roots = []
    for k,n in nodes.items():
        if n.d['parent']:
            n.parent = nodes[n.d['parent']]
            n.parent.children.append(n)
        else:
            roots.append(n)
    nodes_list = topo_sort(nodes)
    for p in nodes_list:
        for c in p.children:
            c.depth = p.depth + 1
    for p in reversed(nodes_list):
        p.d['pw'] = max(2, sum([c.d['pw'] for c in p.children])+p.d['dw'] )
    for r in roots: r.position()
    
    info = LoadJson(pjoin(path,"info.json"))
    if 'id' not in info:
        info['id'] = tree
    focus_tree = merge_dicts([info] + [
        {'focus': n.final()} for n in nodes_list
    ], d=True)
    SaveJson({'focus_tree':focus_tree}, F(pjoin("data","common","national_focus",f"{tree}.json")), indent=4)

def AddFocusTree(path, translate=True):
    '''
    Add a focus tree and then compile it.
    Args:
        path: str. The path of the resource files of the focus tree. The resources should include the focus tree definition and the localisation.
        translate: bool. Whether to translate the localisation of the focus tree.
    Return:
        None
    '''
    tree = path.strip('/').split('/')[-1].upper()
    SaveJson(LoadJson(pjoin(path,"info.json")), F(pjoin("data","focus_trees",tree,"info.json")), indent=4)
    for focus in ListFolders(path):
        if not focus.startswith('__'):
            AddNationalFocus(pjoin(path, focus), tree=tree, translate=translate)
    tree_path = F(pjoin("data","focus_trees",tree)); CreateFolder(tree_path)
    CompileFocusTree(tree_path)