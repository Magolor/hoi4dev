__all__ = [
    'ConfigManager',
]
from ..base import *
    
class ConfigManager(object):
    HOI4DEV_WORKSPACE_DIR = ".hoi4dew"
    HOI4DEV_CONFIG_FILE_NAME = "config.json"
    HOI4DEV_CACHE_DIR = ".cache/"
    def __init__(self):
        self.config = dict()
        self.setup()

    def setup(self, reset:bool = False):
        touch_dir(self.root_path)
        if reset:
            self.reset_config()
        touch_dir(self.cache_path)
        self.load()

    def _load_default_config(self) -> Dict[str, Any]:
        config = load_json(get_hoi4dev_resource("config.json"))
        config['paths'] = {
            "hoi4_game_path": DEFAULT_HOI4_GAME_PATH,
            "hoi4_workshop_path": DEFAULT_HOI4_WORKSHOP_PATH,
            "hoi4_mods_path": DEFAULT_HOI4_MODS_PATH,
            "hoi4_mods_compile_path": DEFAULT_HOI4_MODS_COMPILE_PATH,
            "cache_path": pj("~", self.HOI4DEV_WORKSPACE_DIR, self.HOI4DEV_CACHE_DIR),
        }
    def _init_config_file(self):
        try:
            save_json(self._load_default_config(), self.config_path)
        except Exception as e:
            import click
            click.echo(f"💥 Failed to initialize config at {self.config_path}: {str(e)}.", err=True)
    def _load_config_file(self) -> Dict[str, Any]:
        if not exists_file(self.config_path):
            self._init_config_file()
        try:
            return load_json(self.config_path)
        except Exception as e:
            import click
            click.echo(f"💥 Error loading global config at {self.config_path}: {str(e)}. Using default config.", err=True)
        return self._load_default_config()
    def _save_config_file(self) -> Dict[str, Any]:
        try:
            save_json(self.config, self.config_path)
            return self.config
        except Exception as e:
            import click
            click.echo(f"💥 Error loading global config at {self.config_path}: {str(e)}. Using default config.", err=True)
        return self._load_default_config()
    def save_config_file(self, level:Literal[None,'local','global'] = None):
        if level is None:
            self._save_config_file(level='local')
            self._save_config_file(level='global')
        elif level=='local':
            self._save_config_file(level='local')
        elif level=='global':
            self._save_config_file(level='global')
    def reset_config(self):
        self._init_config_file(level='global')

    @property
    def root_path(self):
        return pj("~", self.HOI4DEV_WORKSPACE_DIR, abs=True)
    @property
    def config_path(self):
        return pj("~", self.HOI4DEV_WORKSPACE_DIR, self.HOI4DEV_CONFIG_FILE_NAME, abs=True)
    @property
    def cache_path(self):
        return pj(self.get("paths.cache_path", default=pj("~", self.HOI4DEV_WORKSPACE_DIR, self.HOI4DEV_CACHE_DIR)), abs=True)

    def get(self, key_path:str = None, default:Any = None):
        return dget(self.config, key_path=key_path, default=default)
    def set(self, key_path:str, value:Any) -> bool:
        changed = dset(self.config, key_path=key_path, value=value)
        if changed:
            self.save_config_file()
        return changed
    def unset(self, key_path:str) -> bool:
        changed = dunset(self.config, key_path=key_path)
        if changed:
            self.save_config_file()
        return changed
    def load(self):
        self.config = self._load_config_file()
    def save(self):
        self.save_config_file()
