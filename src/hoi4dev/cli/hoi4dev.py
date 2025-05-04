from ..utils import *
from ..utils.version import __version__
import click

@click.group()
@click.version_option(__version__, '--version', '-v', message='%(version)s')
@click.help_option('--help', '-h')
@click.pass_context
def cli(ctx):
    pass

@cli.command(name="setup")
@click.help_option('--help', '-h')
@click.option('--reset', '-r', is_flag=True, help='Reset the configuration file to default.', default=False)
def init(reset=False):
    """Initialize the HOI4DEV tool. It will change the config file at '~/.hoi4dev/config.json'."""
    from ..utils.config_utils import ConfigManager
    ConfigManager().setup(reset=reset)
    click.echo(SUCCESS('HOI4DEV successfully initialized.'))

@cli.group(name="config")
@click.help_option('--help', '-h')
@click.pass_context
def cli_config(ctx):
    pass

@cli_config.command(name="show")
@click.help_option('--help', '-h')
@click.argument('key', required=False, default=None)
@click.option('--global', '-g', 'level', flag_value='global', help='Show global config.', default='local')
def hoi4dev_cli_config_show(key, level='local'):
    """Show the configuration."""
    from ..utils.config_utils import ConfigManager, dumps_json
    config = ConfigManager().get(key_path=key, level=level)
    click.echo(dumps_json(config))

@cli_config.command(name="open")
@click.help_option('--help', '-h')
@click.option('--global', '-g', 'level', flag_value='global', help='Show global config.', default='local')
def hoi4dev_cli_config_open(level='local'):
    """Show the configuration."""
    from ..utils.config_utils import ConfigManager
    import subprocess
    config_path = ConfigManager().global_config_path if level == 'global' else ConfigManager().local_config_path
    subprocess.Popen(["open", config_path])

@cli_config.command(name="set")
@click.help_option('--help', '-h')
@click.option('--global', '-g', 'level', flag_value='global', help='Edit global config.', default='local')
@click.argument('key')
@click.argument('value')
@click.option('--json/--no-json', help='Treate the value as a json str.', default=False)
def hoi4dev_cli_config_set(key, value, json=False, level='local'):
    """Edit the configuration."""
    from ..utils.config_utils import ConfigManager, loads_json
    ConfigManager().set(key_path=key, value=loads_json(value) if json else smart_type(value), level=level)

@cli_config.command(name="unset")
@click.help_option('--help', '-h')
@click.option('--global', '-g', 'level', flag_value='global', help='Edit global config.', default='local')
@click.argument('key')
def hoi4dev_cli_config_unset(key, level='local'):
    """Unset the configuration."""
    from ..utils.config_utils import ConfigManager
    ConfigManager().unset(key_path=key, level=level)