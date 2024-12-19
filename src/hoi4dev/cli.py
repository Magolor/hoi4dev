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
@click.option('--yes', '-y', is_flag=True, default=False, help='Accept the default output file path if not specified, without asking. Default is False.')
@click.option('--delete-input', '-d', is_flag=True, default=False, help='Whether to delete the input file after the conversion. Default is False. For safety reasons, the input file will not be deleted but moved to trash.')
def ccl2json(input=None, output=None, yes=False, delete_input=False):
    """Convert a CCL (Clausewitz scripting language) file to a JSON file."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        default_output = AsFormat(input, 'json')
        if not yes:
            output = click.prompt('Enter the output file path (default: ' + default_output + ')', default=default_output)
        else:
            output = default_output
    ccl = ReadTxt(input)
    CreateFile(output); SaveJson(CCL2Dict(ccl), output, indent=4)
    if delete_input and input != output: Delete(input, rm=False)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path.')
@click.option('--yes', '-y', is_flag=True, default=False, help='Accept the default output file path if not specified, without asking. Default is False.')
@click.option('--delete-input', '-d', is_flag=True, default=False, help='Whether to delete the input file after the conversion. Default is False. For safety reasons, the input file will not be deleted but moved to trash.')
def json2ccl(input=None, output=None, yes=False, delete_input=False):
    """Convert a JSON file to a CCL (Clausewitz scripting language) file. Make sure the input file is a valid JSON file."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        default_output = AsFormat(input, get_format_by_content(LoadJson(input)))
        if not yes:
            output = click.prompt('Enter the output file path (default: ' + default_output + ')', default=default_output)
        else:
            output = default_output
    ccl = Dict2CCL(LoadJson(input))
    CreateFile(output); SaveTxt(ccl, output)
    if delete_input and input != output: Delete(input, rm=False)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path.')
@click.option('--yes', '-y', is_flag=True, default=False, help='Accept the default output file path if not specified, without asking. Default is False.')
@click.option('--delete-input', '-d', is_flag=True, default=False, help='Whether to delete the input file after the conversion. Default is False. For safety reasons, the input file will not be deleted but moved to trash.')
def convert(input=None, output=None, yes=False, delete_input=False):
    """Automatic conversion between CCL (Clausewitz scripting language) and JSON files. The conversion type will be determined by the file extension. Specifically, '.txt", '.gfx' and '.gui' files are considered CCL files, while '.json' files are considered JSON files. Using other file extensions may result in an error."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        if input.endswith('.json'):
            default_output = AsFormat(input, get_format_by_content(LoadJson(input)))
        else:
            default_output = AsFormat(input, 'json')
        if not yes:
            output = click.prompt('Enter the output file path (default: ' + default_output + ')', default=default_output)
        else:
            output = default_output
    CCLConvert(input, output)
    if delete_input and input != output: Delete(input, rm=False)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path.')
@click.option('--scope', '-s', is_flag=False, default="", help='The scope of the localisation file. Default to an empty string. This will replace the key \'@\' in HOI4DEV localisation files. Only works with \'.txt\' files.')
@click.option('--yes', '-y', is_flag=True, default=False, help='Accept the default output file path if not specified, without asking. Default is False.')
@click.option('--delete-input', '-d', is_flag=True, default=False, help='Whether to delete the input file after the conversion. Default is False. For safety reasons, the input file will not be deleted but moved to trash.')
def loc2json(input=None, output=None, scope="", yes=False, delete_input=False):
    """Convert a localisation file to a JSON file. If the input file is a '.txt' file, it should follow the HOI4DEV provided localisation format. Otherwise, it should be a standard HOI4 localisation '.yml' file. Using other file extensions may result in an error."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        default_output = AsFormat(input, 'json')
        if not yes:
            output = click.prompt('Enter the output file path (default: ' + default_output + ')', default=default_output)
        else:
            output = default_output
    locs = ReadTxtLocs(path=input, scope=scope) if input.endswith('.txt') else ReadYmlLocs(path=input)
    CreateFile(output); SaveJson(locs, output, indent=4)
    if delete_input and input != output: Delete(input, rm=False)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path.')
@click.option('--yes', '-y', is_flag=True, default=False, help='Accept the default output file path if not specified, without asking. Default is False.')
@click.option('--delete-input', '-d', is_flag=True, default=False, help='Whether to delete the input file after the conversion. Default is False. For safety reasons, the input file will not be deleted but moved to trash.')
def json2loc(input=None, output=None, yes=False, delete_input=False):
    """Convert a JSON file to a localisation file. The output file will be a '.txt' file following the HOI4DEV provided localisation format."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        default_output = AsFormat(input, 'txt')
        if not yes:
            output = click.prompt('Enter the output file path (default: ' + default_output + ')', default=default_output)
        else:
            output = default_output
    locs = LoadJson(input)
    CreateFile(output); SaveTxtLocs(locs, output)
    if delete_input and input != output: Delete(input, rm=False)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path.')
@click.option('--ratio', '-r', is_flag=False, default=1, help='The ratio to zoom the image. Default is 1.')
@click.option('--width', '-w', is_flag=False, default=-1, help='The width to resize the image. Default is -1.')
@click.option('--height', '-h', is_flag=False, default=-1, help='The height to resize the image. Default is -1.')
@click.option('--behavior', '-b', is_flag=False, default='max', help='The behavior when resizing the image. Default is \'max\'. Options: \'max\', \'min\'. Please refer to `ImageZoom` for detailed explanation.')
@click.option('--flip-tga', '-f', is_flag=True, default=False, help='Whether to flip the image when saving \'.tga\' files (specialized for HoI4 country flags). Default is False.')
@click.option('--compression', '-c', is_flag=False, default='dxt3', help='The compression when saving the edited image. Default is \'dxt3\'.')
@click.option('--yes', '-y', is_flag=True, default=False, help='Accept the default output file path if not specified, without asking. Default is False.')
@click.option('--delete-input', '-d', is_flag=True, default=False, help='Whether to delete the input file after the editing. Default is False. For safety reasons, the input file will not be deleted but moved to trash.')
def imgedit(input=None, output=None, ratio=1, width=-1, height=-1, behavior='max', flip_tga=False, compression='dxt3', yes=False, delete_input=False):
    """Load an image, zoom it using `ImageZoom`, and save the edited image. Support \'.dds\' with compression, and \'.tga\', \'.png\', \'.jpg\' files."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        if input.endswith('.dds') or input.endswith('.tga'):
            default_output = AsFormat(input, 'png')
        else:
            default_output = AsFormat(input, 'dds')
        if not yes:
            output = click.prompt('Enter the output file path (default: ' + default_output + ')', default=default_output)
        else:
            output = default_output
    img = ImageLoad(input)
    if img is None:
        raise FileNotFoundError(f"Image not found: \"{input}\"!")
    edited_img = ImageZoom(img, r=ratio, w=width, h=height, behavior=behavior)
    ImageSave(edited_img, output, flip_tga=flip_tga, compression=compression)
    if delete_input and input != output: Delete(input, rm=False)

@cli.command()
@click.option('--input', '-i', is_flag=False, default=None, help='Input image file path.')
@click.option('--output', '-o', is_flag=False, default=None, help='Output file path for the blueprint image.')
@click.option('--color', '-c', is_flag=False, default='white', help='Color of the blueprint lines. Default is white.')
@click.option('--radius', '-r', is_flag=False, default=10.0, help='Width of the blueprint lines. Default is 10.0.')
@click.option('--bg_color', '-bg', is_flag=False, default='blue', help='Background color of the blueprint. Default is blue.')
@click.option('--threshold', '-t', is_flag=False, default=0.15, help='Threshold for edge detection. Default is 0.15.')
@click.option('--add_grid', '-g', is_flag=False, default=6, help='Size of the grid to add. Default is 6.')
@click.option('--grid_color', '-gc', is_flag=False, default='white', help='Color of the grid. Default is white.')
@click.option('--grid_opacity', '-go', is_flag=False, default=0.2, help='Opacity of the grid. Default is 0.2.')
@click.option('--grid_width', '-gw', is_flag=False, default=None, help='Width of the grid. Default is auto.')
def blueprint(input=None, output=None, color='white', radius=10.0, bg_color='blue', threshold=0.15, add_grid=6, grid_color='white', grid_opacity=0.2, grid_width=None):
    """Convert an input image to a blueprint image."""
    if input is None:
        input = click.prompt('Enter the input file path')
    if output is None:
        default_output = AsFormat(input, 'png')  # Assuming PNG is a suitable format for the output
        output = click.prompt('Enter the output file path (default: ' + default_output + ')', default=default_output)

    img = ImageLoad(input)
    if img is None:
        raise FileNotFoundError(f"Image not found: \"{input}\"!")
    blueprint_img = CreateBlueprintImage(img, color=color, radius=radius, bg_color=bg_color, threshold=threshold, add_grid=add_grid, grid_color=grid_color, grid_opacity=grid_opacity, grid_width=grid_width)
    ImageSave(blueprint_img, output)
