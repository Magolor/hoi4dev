# HOI4DEV

**Warning: This package is currently underdeveloped and does not guarantee any consistency.**

**Tutorial Coming Soon...**

## Setup

### Installation

On MacOS:
```bash
bash install.bash
```

On Windows, please checkout [this link](https://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-windows) to manually download and install `magick`, then:
```bash
install.cmd
```

### Configuration

After installation, you need to setup the config to start working for a specific mod project. By default, `init_config()` creates a config at `~/.hoi4dev/config.json`, you can setup the paths manually.

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

### Conversion between YML localisation and TXT files

```python
AddLocalisation("xxx.txt", scope="ABC", translate=False)
```

In the txt file, use `[<LANGUAGE_ABBREVIATION>.<KEY>]`, use `@` to copy the `scope`
For example, consider the following `txt` file, under "ABC" scope:
```
[en.key01]
test1
test2
[zh.@key01]

中文测例1
中文测例2
[zh.key01]
中文测例3
中文测例4
```
It will be converted to:
```yml
l_english:
  "key01":0 "test1\ntest2"
```

```yml
l_simp_chinese:
  "ABC_key01":0 "中文测例1\n中文测例2"
  "key01":0 "中文测例3\n中文测例4"
```

Currently `translate` supports either a local translation model or a Large Language Model, but it requires additonal setups (e.g., huggingface `transformer` or `openai`).

Instead of conversion to YML, you can also convert to JSON using:
```python
ReadTxtLocs("xxx.txt", scope="ABC")
```

For example, the above text file will be parsed as `{'key01: {'en': 'test1\ntest2', 'zh': '中文测例3\n中文测例4'}, 'ABC_key01': {'zh': '中文测例1\n中文测例2'}}`.

### Conversion of dates

Want to know how many days you need to set in `on_actions` for the event to happen at a specific date? Or you need to number of weeks for a focus?
```python
get_num_days("1001.06.01", "1001.12.01") // 7   # 26 weeks

get_end_date("1002.12.01", 1298)                # 1006.06.21
```

Actually, when adding events, `hoi4dev` allows you to automatically set the dates in `on_actions`. We will specify how to use that in the `events` tutorial (Coming Soon).

## Advanced Features

See example scripts in `example_scripts/`. Those scripts may not all able to run as they lack project resource files, but can be useful to help you understand the `hoi4dev` mechanism and classical workflows. For example, consider example scripts in `PIHC_v_0_2_1_2024_10_06/`

On the one hand, there are some useful little tools that can be created using `hoi4dev` in `scripts/*/`:

For example `scripts/states_editor/szj.py` shows how you can batch change the owner of certain states by converting all state history files to JSON, modifying them, and save them back.

`scripts/add_kitin_state_group_gui.py` batch creates a map GUI gfxs (results are in `scripts/region_gui/`). This rely on preprocessed map information by `scripts/C01_build_the_map.py`.

`scripts/adv_gen/script.py` and `scripts/mil_gen/script.py` allow you generate a huge amount of political advisors and military generals with a single `.csv` file. You can create Chinese translation if all your mod developers are from Chinese, for example.

...

On the other hand, scripts starting with `scripts/CXX_....` demonstrates how a regular mod workflow runs. `v0.2.1.py` is the main thread, generating a mod from scratch (not able to run here due to lack of project resource files).

## Demos

We plan to share an end-to-end mod project built with the package in the near future. Stay tuned.

## Frequent Issues

### Windows Computer with non-UTF-8 characters / pyheaven running error with JSON files

**This package is known to malfunction if you are running on Windows with non-UTF-8 characters. May be fixed in the future.**

This error is usually occurred when operating JSON files containing Chinese. The error occurred due to version difference of `jsonlines`.

Therefore, you may try to modify the dependency `pyheaven`:
```python
# In pyheaven/serialize_utils/py 3
def SaveJson(obj, path, backend:Literal['json','jsonl','demjson','simplejson','jsonpickle']='json', indent:Optional[int]=None, append:bool=False, *args, **kwargs):
    """Save an object as json (or jsonl) file.

    Args:
        obj: The object to be saved.
        path: The save path.
        backend (str): Specify backend for saving an object in json format. Please refer to function `BUILTIN_JSON_BACKENDS()` for built-in backends.
        indent (int/None): The `indent` argument for saving in json format, only works if backend is not "jsonl".
        append (bool): If True, use "a" mode instead of "w" mode, only works if backend is "jsonl".
    Returns:
        None
    """
    assert (backend in BUILTIN_JSON_BACKENDS()), (f"backend not found! Supported backends: {BUILTIN_JSON_BACKENDS()}")
    CreateFile(path); path = p2s(path)
    if backend=='jsonl':
        assert (indent is None), ("'jsonl' format does not support parameter 'indent'!")
        with jsonlines.open(path, "a" if append else "w", encoding='utf-8', errors='ignore') as f:
            for data in obj:
                f.write(data)
    else:
        assert (append is False), ("'json' format does not support parameter 'append'!")
        module = globals()[backend]
        with open(path, "w", encoding='utf-8', errors='ignore') as f:
            if backend in ['json','simplejson']:
                module.dump(obj, f, indent=indent, *args, **kwargs)
            else:
                f.write(module.dumps(obj, indent=indent, *args, **kwargs))
```

Remove or add `encoding='utf-8', errors='ignore'` depending on your error may solve this issue. You may also want to change `LoadJson` function in the same file. (If you find any convenient fix to this error, feel free to contact me or create a new issue to update `pyheaven`).
