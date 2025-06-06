# HOI4DEV HOI4 MOD Development Tool

Version: 0.1.1.3

Compatible with HOI4 Version: ~ 1.16.4

## Installation and Configuration

Complete installation and configuration tutorial: [Installation Tutorial - Prerequisites](https://github.com/Magolor/hoi4dev/blob/main/docs/zh/0.%E5%AE%89%E8%A3%85%E6%95%99%E7%A8%8B-%E5%89%8D%E7%BD%AE.md) and [Installation Tutorial](https://github.com/Magolor/hoi4dev/blob/main/docs/zh/1.%E5%AE%89%E8%A3%85%E6%95%99%E7%A8%8B.md)

Pre-installation requirements: [ImageMagick](https://imagemagick.org/script/download.php), Steam, Steam version of HOI4

<br/>

### PIP Installation
```bash
pip install -U hoi4dev
```

<br/>

### Installation from Repo
```bash
git clone git@github.com:Magolor/hoi4dev.git
cd ./hoi4dev/
bash install_win.bash # or bash install_mac.bash
```

<br/>

### Configuration

```bash
hoi4dev init
```

<br/>

### Path Settings

You can find the configuration file `config.json` in the hidden folder `~/.hoi4dev/` in your user directory.

On Windows, it is located at `C:\Users\<Your Username>\.hoi4dev\config.json`:
```json
{
    "HOI4_GAME_PATH": "/Users/<Your Username>/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV/",
    "HOI4_WORKSHOP_PATH": "/Users/<Your Username>/Library/Application Support/Steam/steamapps/workshop/content/394360/",
    "HOI4_MODS_PATH": "/Users/<Your Username>/Documents/Paradox Interactive/Hearts of Iron IV/mod/",
    "HOI4_MODS_COMPILE_PATH": "/Users/<Your Username>/Documents/Paradox Interactive/Hearts of Iron IV/mod/",
    "CURRENT_MOD_PATH": null
}
```

On MacOS, it is located at `/Users/<Your Username>/.hoi4dev/config.json`:
```json
{
    "HOI4_GAME_PATH": "C:\\/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV/",
    "HOI4_WORKSHOP_PATH": "C:\\/Program Files (x86)/Steam/steamapps/workshop/content/394360/",
    "HOI4_MODS_PATH": "C:\\/Users/<Your Username>/Documents/Paradox Interactive/Hearts of Iron IV/mod/",
    "HOI4_MODS_COMPILE_PATH": "C:\\/Users/<Your Username>/Documents/Paradox Interactive/Hearts of Iron IV/mod/",
    "CURRENT_MOD_PATH": null
}
```

If you have modified these paths during the installation of Steam, HOI4, or mods, you may need to adjust them manually.

Where:
- `HOI4_GAME_PATH` should be the installation location of your Steam HOI4, which should contain the executable and many other files;
- `HOI4_WORKSHOP_PATH` should be the location of your Steam HOI4 workshop download files (this path is usually not used);
- `HOI4_MODS_PATH` should be the installation location of all your HOI4 mod files; note that `.mod` files must be present for the HOI4 launcher to recognize and load the mods;
- `HOI4_MODS_COMPILE_PATH` should be the expected location for your compiled mods (the HOI4 launcher only needs to recognize `.mod` files, and mod resource files do not need to be placed together with `.mod` files. If your computer is low on space, you can choose to set `HOI4_MODS_COMPILE_PATH` to another drive or any other location. Typically, if the user does not make changes, this path will be the same as `HOI4_MODS_PATH`);
- `CURRENT_MOD_PATH` is the mod currently being modified, recorded by the tool, and you do not need to worry about it. When you have a mod project folder you are developing, you can use the command `hoi4dev checkout <your folder address>` to switch `CURRENT_MOD_PATH` to the mod you are currently modifying.

<br/>

## Basic Functions

### Conversion between HOI4 Script CCL and JSON Format

Use `hoi4dev convert -i <input file> -o <output file>` to automatically and intelligently convert from one format to another.

Format recognition depends on the file extension; `.txt`, `.gui`, and `.gfx` files will be treated as CCL, while `.json` files will be treated as JSON format.

For example, converting from CCL to JSON format in Python code is equivalent to:
```python
input_file = "<input file>"
output_file = "<output file>"

ccl_data = ReadTxt(input_file)
json_data = CCL2Dict(ccl_data)

CreateFile(output_file)
SaveJson(json_data, output_file, indent=4)
```

Conversely, converting from JSON format to CCL is equivalent to:
```python
input_file = "<input file>"
output_file = "<output file>"

json_data = LoadJson(input_file)
ccl_data = Dict2CCL(json_data)

CreateFile(output_file)
SaveTxt(ccl_data, output_file)
```

<br/>

### TXT Format Localization

Use `hoi4dev loc2json -i <input file> -o <output file> -s <domain>` to convert TXT or YML to JSON. Format recognition depends on the file extension; `.txt` files will be treated as localization text files defined by HOI4DEV, while `.yml` files will be treated as HOI4's localization format. `<domain>` only applies to `.txt` files.

In Python code, this is equivalent to:
```python
input_file = "<input file>"
output_file = "<output file>"

json_data = ReadTxtLocs(input_file, scope="<domain>") if input.endswith('.txt') else ReadYmlLocs(path=input)

CreateFile(output_file)
SaveJson(json_data, output_file, indent=4)
```

Meanwhile, using `hoi4dev json2loc -i <input file> -o <output file>` can convert JSON files back to TXT text files. Since converting to YML will result in multiple files placed in different locations within the mod's `localisation/` directory, it needs to be used during mod compilation.

In Python code, this is equivalent to:
```python
input_file = "<input file>"
output_file = "<output file>"

json_data = LoadJson(input_file)

CreateFile(output_file)
SaveTxtLocs(json_data, output_file)
```

<br/>

### Image Editing

The image editing function allows users to resize and convert image formats, supporting various image formats including `.png`, `.jpg`, `.tga`, and the particularly beloved `.dds` by Paradox Interactive.

Use the following command for basic image resizing, cropping, and format conversion:
```bash
hoi4dev imgedit -i <input file> -o <output file> -r <scale ratio> -w <width> -h <height> -b <behavior> -f <flip TGA> -c <compression>
```

- `-i` or `--input`: Input file path.
- `-o` or `--output`: Output file path.
- `-r` or `--ratio`: Scale ratio, default is 1.
- `-w` or `--width`: Target width, default is -1 (maintain original width).
- `-h` or `--height`: Target height, default is -1 (maintain original height).
- `-b` or `--behavior`: Scaling behavior, default is `max`, optional values are `max` or `min`.
- `-f` or `--flip_tga`: Whether to flip the image when saving as a `.tga` file, default is `False` (indicating no flip; HOI4 flags are all upside-down `.tga` files).
- `-c` or `--compression`: Compression format when saving the edited image, default is `dxt3`. Only applicable to `.dds`.

Please note the behavior of this command:
1. The aspect ratio of the image will always be maintained, avoiding stretching or distortion.
2. If a ratio `r` is given, the image will always be scaled proportionally, then cropped/extended (filling with a transparent background). `w` and `h` should either both be unset or both set; otherwise, it will cause an error.
3. If no ratio is given, and neither `w` nor `h` is provided, the image will not be modified.
4. Otherwise, if no ratio is given, and only one of `w` or `h` is provided, the image will be scaled to the given size.
5. If both `w` and `h` are provided, if the behavior is 'max', the image will scale until both sides are greater than the given size, then crop to the given size; if the behavior is 'min', the image will scale until only one side equals the given size, then extend to the given size.
For example:
- An image of size (5, 3) scaled by `r=2` will result in (10, 6).
- An image of size (5, 3) scaled by `r=2, w=30, h=30` will result in (10, 6) then extended to (30, 30).
- An image of size (5, 3) scaled by `w=30` will result in (30, 18).
- An image of size (5, 3) scaled by `h=30` will result in (50, 30).
- An image of size (5, 3) scaled by `w=30, h=30, behavior='max'` will result in (50, 30) then cropped to (30, 30).
- An image of size (5, 3) scaled by `w=30, h=30, behavior='min'` will result in (30, 18) then extended to (30, 30).

In practical use, for example:
```bash
hoi4dev imgedit -i <input file> -o <output file> -r 2 -w 800 -h 600 -b max -c dxt3
```

This will double the size of the input image, crop it to 800x600 (if smaller, it will fill with a transparent background), and if saved as a `.dds` file, it will be compressed.

In Python code, this is equivalent to:
```python
input_file = "<input file>"
output_file = "<output file>"
r = 2  # Scale ratio
w = 800  # Target width
h = 600  # Target height
behavior = 'max'  # Scaling behavior
flip_tga = False  # Do not flip TGA
compression = 'dxt3'  # Compression format

img = ImageLoad(input_file)
edited_img = ImageZoom(img, r=r, w=w, h=h, flip_tga=flip_tga, behavior=behavior)
ImageSave(edited_img, output_file, compression=compression)
```

However, it is worth noting that in Python code, `flip_tga` defaults to true, meaning all `.tga` image files are flipped by default.

<br/>

## Advanced Functions and Project Examples

For more details, see: [Usage Tutorial](https://github.com/Magolor/hoi4dev/blob/main/docs/zh/2.%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B.md) and [Example - PIHC2 Mod](https://github.com/Magolor/hoi4dev/blob/main/docs/zh/3.%E7%A4%BA%E4%BE%8B-PIHC2%E6%A8%A1%E7%BB%84.md)

Complete mod development example project: PIHC (The Pony In The High Castle MOD).

[GitHub Link](https://github.com/Magolor/HOI4-PIHC) (currently private, contact the author for access; we will open it soon).

<br/>

## Changelog

### v0.1.1.3

- Bugfix

### v0.1.0.14

- Bugfix

### v0.1.0.13

- Bugfix

- tga image format optimization

### v0.1.0.12

- Performance improvement

### v0.1.0.11

- Added support for entity modding and more image utils

### v0.1.0.10

- Added support for special projects and scientists

- `hoi4dev` terminal command auto-infers output path

- `hoi4dev blueprint`

<br/>

## Contact Information

Talirian:

- QQ: 125657190
- Email: magolorcz@gmail.com

<br/>
