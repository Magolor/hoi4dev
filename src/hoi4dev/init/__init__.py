from ..utils import *

MAIN_DIRECTORIES = ['common', 'events', 'gfx', 'history', 'interface', 'music', 'sound', 'tutorial', "portraits", "country_metadata"]
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
    git_folder = pjoin(GIT_PATH, name)
    if ExistFolder(pjoin(root, ".git")):
        CopyFolder(pjoin(root, ".git"), git_folder, rm=True)
    ClearFolder(root, rm=True)
    if ExistFolder(git_folder):
        CopyFolder(git_folder, pjoin(root, ".git"), rm=True)
    
    game_path = get_config('HOI4_GAME_PATH')
    for path in MAIN_DIRECTORIES:
        for folder in ListFolders(pjoin(game_path, path)):
            CreateFolder(pjoin(root, path, folder))
    
    CreateFolder(pjoin(root, 'hoi4dev_settings'))
    CopyFolder(find_resource(""), pjoin(root, "hoi4dev_settings"), rm=True)
    
    if "copies" in kwargs:
        CopyFolder(kwargs["copies"], root, rm=True)
    
    settings = merge_dicts([LoadJson(find_resource('configs/config.json')), kwargs])
    SaveJson(settings, pjoin(root, 'hoi4dev_settings', 'configs', 'config.json'), indent=4)
    
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
    with open(pjoin(root, 'descriptor.mod'), 'w') as f:
        f.write("\n".join(
            [f"version=\"{settings['version']}\""] +
            [ "tags = {"] +
            [ ("\t"+f"\"{tag}\"") for tag in settings['tags'] ] +
            [ "}" ] +
            [ f"name=\"{settings['title']}\"" ] +
            [ "picture=\"thumbnail.png\""] +
            [ f"supported_version=\"{settings['hoi4_version']}\""] +
            [ f"replace_path=\"{p}\"" for p in settings['replace_paths'] ]
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
    copy_config = LoadJson(F(pjoin("hoi4dev_settings","configs","copy.json")))
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
    if ('_gfx' in directory) or ('spriteTypes' in content): return 'gfx'
    if 'guiTypes' in content: return 'gui'
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
        try:
            CCLConvert(
                F(pjoin('data', path, file)),
                F(pjoin(path, AsFormat(file.replace('_gfx', ''), format)))
            )
        except Exception as e:
            print(f"Error: {e}")
            print(f"File: {file}")
    CopyFolder(F(pjoin("data", "localisation")), F("localisation"))