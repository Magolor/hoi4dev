from ..utils import *

MAIN_DIRECTORIES = ['common', 'events', 'gfx', 'history', 'interface', 'music', 'sound', 'tutorial']
def CreateMod(name, **kwargs):
    '''
    Initialize a new mod.
    Args:
        name: str. The name of the mod.
        **kwrags: Dict. Other arguments.
    Return:
        str. The path of the mod.
    
    For example, the arguments could include:
    - version: str. Version of the mod.
    - languages: List[str]. Supported languages of the mod. The first language will be used as the main language (default language, source of translation, etc.).
    - img_scales: Dict. Image scales of the mod. Like {'loadingscreen': (1920,1080), ...}.
    - copies: str. The path to a mod resource, the entire mod will be copied before creating the current mod.
    - replace_paths: list. List of files to be replaced.
    '''
    mods_path = get_config('HOI4_MODS_PATH')
    root = pjoin(mods_path, name)
    ClearFolder(root, rm=True)
    
    if "copies" in kwargs:
        CopyFolder(kwargs["copies"], root, rm=True)
    
    game_path = get_config('HOI4_GAME_PATH')
    for path in MAIN_DIRECTORIES:
        for folder in ListFolders(pjoin(game_path, path)):
            CreateFolder(pjoin(root, path, folder))
    
    CreateFolder(pjoin(root, 'hoi4dev_settings'))
    settings = merge_dicts([LoadJson(find_resource('configs/default.json')), kwargs])
    SaveJson(settings, pjoin(root, 'hoi4dev_settings', 'config.json'), indent=4)
    SaveJson(LoadJson(find_resource('configs/copy.json')), pjoin(root, 'hoi4dev_settings', 'copy.json'), indent=4)
    SaveJson(LoadJson(find_resource('configs/manpower.json')), pjoin(root, 'hoi4dev_settings', 'manpower.json'), indent=4)
    SaveJson(LoadJson(find_resource('configs/buildings.json')), pjoin(root, 'hoi4dev_settings', 'buildings.json'), indent=4)
    SaveJson({}, pjoin(root, 'hoi4dev_settings', 'term_table.json'), indent=4)
    CreateFolder(pjoin(root, 'hoi4dev_settings', 'imgs'))
    for file in ListFiles(find_resource('imgs/defaults')):
        src = pjoin(find_resource('imgs/defaults'), file); tgt = pjoin(root, 'hoi4dev_settings', 'imgs', file)
        if not ExistFile(tgt): ImageCopy(src, tgt, format='png')
    
    with open(pjoin(mods_path, f'{name}.mod'), 'w') as f:
        f.write("\n".join(
            [f"version=\"{settings['version']}\""] +
            [ "tags = {"] +
            [ ("\t"+f"\"{tag}\"") for tag in settings['tags'] ] +
            [ "}" ] +
            [ f"name=\"{settings['title']}\"" ] +
            [ "picture=\"thumbnail.png\""] +
            [ f"supported_version=\"{settings['hoi4_version']}\""] +
            [ f"replace_path=\"{p}\"" for p in settings['replace_paths'] ] +
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
            if key in ['CopyFile']:
                if not ExistFile(F(v)):
                    eval(f"{key}(\"{pjoin(game_path, v)}\", \"{F(v)}\")")
            elif key in ['CCLConvert']:
                if not ExistFile(F(pjoin('data',AsFormat(v,'json')))):
                    eval(f"{key}(\"{pjoin(game_path, v)}\", \"{F(pjoin('data',AsFormat(v,'json')))}\")")
            elif key in ['CreateFolder']:
                eval(f"{key}(\"{F(v)}\")")

def get_format(directory, content):
    if directory != 'interface': return 'txt'
    if 'guiTypes' in content: return 'gui'
    if 'spriteTypes' in content: return 'gfx'
    return 'txt'

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
        format = get_format(path, ReadTxt(F(pjoin('data', path, file))))
        CCLConvert(
            F(pjoin('data', path, file)),
            F(pjoin(path, AsFormat(file, format)))
        )
    CopyFolder(F(pjoin("data", "localisation")), F("localisation"))