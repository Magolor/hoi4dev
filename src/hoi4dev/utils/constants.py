from .heaven import *

SUPPORTED_CCL_RESOURCES_SUFFIXES = [
    "gfx",
    "gui",
    "asset",
    "dlc",
    "txt",
]
SUPPORTED_TEXTUAL_RESOURCES_SUFFIXES = [
    "txt",
    "gfx",
    "gui",
    "asset",
    "dlc",
    "yml",
    "lua",
    "fxh",
    "shader",
    "anim",
    "fnt"
    "json",
]

SUPPORTED_IMAGE_RESOURCES_SUFFIXES = [
    "dds",
    "tga",
    "png",
    "jpg",
]
def is_image(filename):
    return filename.rsplit('.', 1)[-1].lower() in SUPPORTED_IMAGE_RESOURCES_SUFFIXES

SUPPORTED_AUDIO_RESOURCES_SUFFIXES = [
    "ogg",
    "wav",
    "mp3",
]
def is_audio(filename):
    return filename.rsplit('.', 1)[-1].lower() in SUPPORTED_AUDIO_RESOURCES_SUFFIXES

SUPPORTED_HOI4DEV_RESOURCES_SUFFIXES = [
    "py",
    "bash",
    "json"
]
def is_hoi4dev(filename):
    return filename.rsplit('.', 1)[-1].lower() in SUPPORTED_HOI4DEV_RESOURCES_SUFFIXES

SUPPORTED_LANGUAGES = {
    'en': {'huggingface': 'en', 'nltk':    'english', 'hoi4':      'english', 'nl':            'English'},
    'zh': {'huggingface': 'zh', 'nltk':    'chinese', 'hoi4': 'simp_chinese', 'nl': 'Simplified Chinese'},
    'ru': {'huggingface': 'ru', 'nltk':    'russian', 'hoi4':      'russian', 'nl':            'Russian'},
    'de': {'huggingface': 'de', 'nltk':     'german', 'hoi4':       'german', 'nl':             'German'},
    'fr': {'huggingface': 'fr', 'nltk':     'french', 'hoi4':       'french', 'nl':             'French'},
    'es': {'huggingface': 'es', 'nltk':    'spanish', 'hoi4':      'spanish', 'nl':            'Spanish'},
    'pt': {'huggingface': 'pt', 'nltk': 'portuguese', 'hoi4':     'braz_por', 'nl':         'Portuguese'},
    'ja': {'huggingface': 'ja', 'nltk':   'japanese', 'hoi4':     'japanese', 'nl':           'Japanese'},
    'pl': {'huggingface': 'pl', 'nltk':     'polish', 'hoi4':       'polish', 'nl':             'Polish'},
}
DEFAULT_LANGUAGE = 'en'

from agent_heaven import is_macos, pj
DEFAULT_HOI4_GAME_PATH = pj("~", "Library", "Application Support", "Steam", "steamapps", "common", "Hearts of Iron IV") if is_macos() else pj("C:\\", "Program Files (x86)", "Steam", "steamapps", "common", "Hearts of Iron IV")
DEFAULT_HOI4_WORKSHOP_PATH = pj("~", "Library", "Application Support", "Steam", "steamapps", "workshop", "content", "394360") if is_macos() else pj("C:\\", "Program Files (x86)", "Steam", "steamapps", "workshop", "content", "394360")
DEFAULT_HOI4_MODS_PATH = pj("~", "Documents", "Paradox Interactive", "Hearts of Iron IV", "mod")
DEFAULT_HOI4_MODS_COMPILE_PATH = pj("~", "Documents", "Paradox Interactive", "Hearts of Iron IV", "mod")

def get_hoi4dev_resource(path):
    import importlib
    with importlib.resources.files("hoi4dev").joinpath("resources", path).as_file() as path:
        return str(path.resolve())
