# HOI4DEV

**Warning: This package is currently underdeveloped and does not guarantee any consistency.**

## Install

1. Install `magick` (for image processing):

On MacOS:
```bash
brew install freetype imagemagick
export MAGICK_HOME=/opt/homebrew/opt/imagemagick
export PATH=$MAGICK_HOME/bin:$PATH
```

On Windows, please checkout [this link](https://docs.wand-py.org/en/0.6.12/guide/install.html#install-imagemagick-on-windows), then:
```bash
export MAGICK_HOME=C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI
export PATH=%MAGICK_HOME%\\bin;%PATH%
```

2. Install `hoi4dev` and its dependencies:
```bash
export PDOC_ALLOW_EXEC=1
pip install -q -r requirements.txt
pip install -e .

pdoc -d google --output-dir doc hoi4dev

python -c "from hoi4dev import init_config; init_config()"
python -c "import hoi4dev; from pyheaven import GREEN; print(GREEN(f'hoi4dev version {hoi4dev.__version__} successfully installed!'))"
```

Or you can use the integrated script in `install.bash`. This installation setup is configured and tested for MacOS. If you encounter dependency issues, try manually configure `magick` and then run `python setup.py develop` or `python setup.py install` instead of the integrated script.

3. After installation, you need to setup the config to start working for a specific mod project. By default, `init_config()` creates a config at `~/.hoi4dev/config.json`, you can setup the paths manually.

On MacOS:
```bash
{
    "HOI4_GAME_PATH": "/Users/<YOUR_USER_NAME_HERE>/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV",
    "HOI4_MODS_PATH": "/Users/<YOUR_USER_NAME_HERE>/Documents/Paradox Interactive/Hearts of Iron IV/mod",
    "HOI4_MODS_COPY_PATH": "/Users/<YOUR_USER_NAME_HERE>/Documents/Paradox Interactive/Hearts of Iron IV/mod",
    "CURRENT_MOD_PATH": "/Users/<YOUR_USER_NAME_HERE>/Documents/Paradox Interactive/Hearts of Iron IV/mod/<YOUR_MOD_NAME>"
}
```

On Windows:
```bash
{
    "HOI4_GAME_PATH": "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Hearts of Iron IV",
    "HOI4_MODS_PATH": "C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\394360",
    "HOI4_MODS_COPY_PATH": "C:\\Users\\<YOUR_USER_NAME_HERE>\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod",
    "CURRENT_MOD_PATH": "C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\394360\\<YOUR_MOD_NAME>"
}
```

The `HOI4_MODS_COPY_PATH` is usually useless, but sometimes it may be required if your user name contains Chinese or other non-UTF-8 characters. Though, it is still worth warning that **This package is known to malfunction if you are running on Windows with non-UTF-8 characters. May be fixed in the future.**

## Basic Features

### CCL (Clausewitz scripting language) and JSON conversion

```python
from hoi4dev import *
# Load JSON file
A = LoadJson("xxx.json")

# Convert JSON to CCL
with open("xxx.txt", "w") as f:
    f.write(Dict2CCL(A) + "\n")

# Load CCL file
with open("ccl.txt", "r") as f:
    A_ccl = f.read()

# Convert CCL to JSON

```

### Image conversion

```python
from hoi4dev import *

# Load a png
a = ImageLoad("xxx.png")

# Zoom & auto-Crop to target size
A = ImageZoom(a, w=512, h=512)

# Save Image:
ImageSave(A, "xxx.dds") # automatically compress dds with dxt5
ImageSave(A, "xxx.tga") # automatically flip tga for flags
```

### Find your COMPILED mod

```python
# Use `F` to find your COMPILED mod files
path_to_your_mod = F("")
# Add a thumbnail manually
CopyFile("thumbnail.png", F("thumbnail.png"))
```

## Advanced Features

See example scripts in `example_scripts/`. Those scripts may not all able to run as they lack project resource files, but can be useful to help you understand the `hoi4dev` mechanism and classical workflows. For example, consider example scripts in `PIHC_v_0_2_1_2024_10_06/`

On the one hand, there are some useful little tools that can be created using `hoi4dev` in `scripts/*/`:

For example `scripts/states_editor/szj.py` shows how you can batch change the owner of certain states by converting all state history files to JSON, modifying them, and save them back.

`scripts/add_kitin_state_group_gui.py` batch creates a map GUI gfxs (results are in `scripts/region_gui/`). This rely on preprocessed map information by `scripts/C01_build_the_map.py`.

`scripts/adv_gen/script.py` and `scripts/mil_gen/script.py` allow you generate a huge amount of political advisors and military generals with a single `.csv` file. You can create Chinese translation if all your mod developers are from Chinese, for example.

...

On the other hand, scripts starting with `scripts/CXX_....` demonstrates how a regular mod workflow runs. `v0.2.1.py` is the main thread, generating a mod from scratch (not able to run here due to lack of project resource files).
