from .utils import *
import click
from pyheaven import set_default_encoding, load_default_encoding
from .__init__ import __version__

@click.group()
@click.version_option(__version__, '--version', '-v', message='%(version)s')
@click.help_option('--help', '-h')
@click.pass_context
def cli(ctx):
    pass

@cli.command()
@click.option('--encoding', '-e', is_flag=False, default='utf-8', help='Set the default encoding used by the tool. Default is utf-8. Recommended \'gbk\' for Chinese.')
@click.option('--compile_path', '-p', is_flag=False, default=None, help='Set the compile path for the tool. Which will be a workspace to store mods compiled from your source code. Default is None, which automatically sets it equal to the \'HOI4_MODS_PATH\' in the config.')
def init(encoding='utf-8',compile_path=None):
    """Initialize the HOI4DEV tool. It will change the config file at '~/.hoi4dev/config.json' and set the encoding (defaults to 'utf-8')."""
    init_config(force=True)
    set_default_encoding(encoding)
    if compile_path is not None:
        set_config('HOI4_MODS_COMPILE_PATH', compile_path)
    else:
        set_config('HOI4_MODS_COMPILE_PATH', get_config('HOI4_MODS_PATH'))
    click.echo(SUCCESS('HOI4DEV successfully initialized.'))

@cli.command()
@click.option('--encoding', '-e', is_flag=False, default=None, help='Set the default encoding used by the tool. Default is None, which will not change the current encoding.')
def enc(encoding=None):
    """Set the default encoding used by the tool. If not specified, it will print the current encoding."""
    if encoding is None:
        click.echo(f"Default encoding unchanged. Current encoding: '{load_default_encoding()}'")
    else:
        click.echo(SUCCESS(f"Default encoding set to '{encoding}'. (Previous encoding: '{load_default_encoding()}')"))
        set_default_encoding(encoding)

@cli.command()
@click.option('--path', '-p', is_flag=False, default=None, help='Path to the mod directory.')
def checkout(path):
    """Switch the current working mod to the specified mod directory. It should be a path will your mod SOURCE CODE is located."""
    set_current_mod(path)
    click.echo('Switched to mod directory: ' + path)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path.')
def ccl2json(input=None, output=None):
    """Convert a CCL (Clausewitz scripting language) file to a JSON file."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        output = click.prompt('Enter the output file path')
    ccl = ReadTxt(input)
    CreateFile(output); SaveJson(CCL2Dict(ccl), output, indent=4)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path.')
def json2ccl(input=None, output=None):
    """Convert a JSON file to a CCL (Clausewitz scripting language) file. Make sure the input file is a valid JSON file."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        output = click.prompt('Enter the output file path')
    ccl = Dict2CCL(LoadJson(input))
    CreateFile(output); SaveTxt(ccl, output)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path.')
def convert(input=None, output=None):
    """Automatic conversion between CCL (Clausewitz scripting language) and JSON files. The conversion type will be determined by the file extension. Specifically, '.txt", '.gfx' and '.gui' files are considered CCL files, while '.json' files are considered JSON files. Using other file extensions may result in an error."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        output = click.prompt('Enter the output file path')
    CCLConvert(input, output)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path.')
@click.option('--scope', '-s', is_flag=False, default="", help='The scope of the localisation file. Default to an empty string. This will replace the key \'@\' in HOI4DEV localisation files. Only works with \'.txt\' files.')
def loc2json(input=None, output=None, scope=""):
    """Convert a localisation file to a JSON file. If the input file is a '.txt' file, it should follow the HOI4DEV provided localisation format. Otherwise, it should be a standard HOI4 localisation '.yml' file. Using other file extensions may result in an error."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        output = click.prompt('Enter the output file path')
    locs = ReadTxtLocs(path=input, scope=scope) if input.endswith('.txt') else ReadYmlLocs(path=input)
    CreateFile(output); SaveJson(locs, output, indent=4)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path.')
def json2loc(input=None, output=None):
    """Convert a JSON file to a localisation file. The output file will be a '.txt' file following the HOI4DEV provided localisation format."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        output = click.prompt('Enter the output file path')
    locs = LoadJson(input)
    CreateFile(output); SaveTxtLocs(locs, output)