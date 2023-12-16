from ..utils import *

MAIN_DIRECTORIES = ['common', 'gfx', 'history', 'interface', 'music', 'sound']
def CreateMod(name, **kwargs):
    '''
    Initialize a new mod.
    Args:
        name: str. The name of the mod.
        **kwrags: dict. Other arguments.
    Return:
        str. The path of the mod.
    
    For example, the arguments could include:
    - version: str. Version of the mod.
    - languages: List[str]. Supported languages of the mod. The first language will be used as the main language (default language, source of translation, etc.).
    - img_scales: dict. Image scales of the mod. Like {'loadingscreen': (1920,1080), ...}.
    - copies: str. The path to a mod resource, the entire mod will be copied before creating the current mod.
    - replace_paths: list. List of files to be replaced.
    '''
    mods_path = get_config('HOI4_MODS_PATH')
    root = pjoin(mods_path, name)
    if "clear" in kwargs and kwargs['clear']:
        ClearFolder(root, rm=True)
    else:
        CreateFolder(root)
    CreateFolder(pjoin(root, 'data'))
    
    if "copies" in kwargs:
        CopyFolder(kwargs["copies"], root, rm=True)
    
    game_path = get_config('HOI4_GAME_PATH')
    for path in MAIN_DIRECTORIES:
        for folder in ListFolders(pjoin(game_path, path)):
            CreateFolder(pjoin(root, path, folder))
    
    CreateFolder(pjoin(root, 'hoi4dev_settings'))
    settings = merge_dicts([{
        "languages": ["zh", "en", "ru"],
        "version": "0.1.0.0",
        "hoi4_version": "1.13.5",
        "img_scales": {
            "loadingscreen": (1920,1080),
            "mainscreen": (1920,1440),
            "leader_portrait": (156,210),
            "advisor_portrait": (65, 67),
            "flag_large": (82,52),
            "flag_medium": (41,26),
            "flag_small": (10,7),
            "idea": (74, 74),
            "designer": (64, 64),
            "ideology": (68, 68),
            "equipment_small": (64, 64),
            "equipment_medium": (150, 72), #?
            "equipment_large": (150, 150), #?
            "country_event": (210, 176),
            "country_event_image": (640, 360),
            "news_event": (397, 153),
            "news_event_image": (640, 360),
            "super_event": (780, 510),
            "super_event_image": (768, 432),
            "decision_category": (52, 40),
            "focus": (104, 104),
            "unit_icon_large": (152, 42),
            "unit_icon_small": (60, 12),
            "autonomy_icon": (36, 36),
            "diplomacy_alert": (47, 42),

            "technology_gui_distance": 210,            
        },
        "replace_paths": [
        ],
    }, kwargs])
    
    SaveJson(settings, pjoin(root, 'hoi4dev_settings', 'config.json'), indent=4)
    SaveJson(LoadJson(find_resource('configs/copy.json')), pjoin(root, 'hoi4dev_settings', 'copy.json'), indent=4)
    SaveJson(LoadJson(find_resource('configs/manpower.json')), pjoin(root, 'hoi4dev_settings', 'manpower.json'), indent=4)
    SaveJson(LoadJson(find_resource('configs/buildings.json')), pjoin(root, 'hoi4dev_settings', 'buildings.json'), indent=4)
    
    with open(pjoin(mods_path, f'{name}.mod'), 'w') as f:
        f.write("\n".join(
            [f"version=\"{settings['version']}\""] +
            [ "tags = {"] +
            [ ("\t"+tag) for tag in settings['tags'] ] +
            [ "}" ] +
            [ f"name=\"{settings['title']}\"" ] +
            [ "picture=\"thumbnail.png\""] +
            [ f"supported_version=\"{settings['hoi4_version']}\""] +
            [ f"replace_path={p}" for p in settings['replace_paths'] ] +
            [ f"path=\"{root}\""]
        ))
    
    return root

def InitMod():
    '''
    Initialize a new mod.
    Args:
        None
    Return:
        None
    '''
    copy_config = LoadJson(F('hoi4dev_settings/copy.json'))
    game_path = get_config('HOI4_GAME_PATH')
    for key, value in copy_config.items():
        for v in value:
            if key in ['CopyFolder', 'CopyFile']:
                eval(f"{key}(\"{pjoin(game_path, v)}\", \"{F(v)}\")")
            elif key in ['CCLConvert']:
                eval(f"{key}(\"{pjoin(game_path, v)}\", \"{F(pjoin('data',AsFormat(v,'json')))}\")")
            elif key in ['CreateFolder']:
                eval(f"{key}(\"{F(v)}\")")

def CompileMod():
    '''
    Compile the mod to get a final version.
    Args:
        None
    Return:
        None
    '''
    files = [(path, f) for path in MAIN_DIRECTORIES for f in EnumFiles(F(pjoin('data', path)), relpath=F(pjoin('data', path))) if f.endswith('.json')]
    for path, file in TQDM(files, desc=f"Compiling the mod..."):
        CCLConvert(
            F(pjoin('data', path, file)),
            F(pjoin(path, AsFormat(file,'txt')))
        )
    CopyFolder(F(pjoin("data", "localisation")), F("localisation"))