# HOI4DEV 钢4MOD开发工具

更新日期：2024.12.10

版本：0.1.0.10

适配钢4版本：~ 1.15.1

## 安装与配置

完整版安装与配置教程：[安装教程-前置](https://github.com/Magolor/hoi4dev/blob/main/docs/zh/0.%E5%AE%89%E8%A3%85%E6%95%99%E7%A8%8B-%E5%89%8D%E7%BD%AE.md) 与 [安装教程](https://github.com/Magolor/hoi4dev/blob/main/docs/zh/1.%E5%AE%89%E8%A3%85%E6%95%99%E7%A8%8B.md)

安装前置需求：[ImageMagick](https://imagemagick.org/script/download.php)、Steam、Steam版本钢4

<br/>

### PIP安装
```bash
pip install -U hoi4dev
```

<br/>

### 从Repo安装
```bash
git clone git@github.com:Magolor/hoi4dev.git
cd ./hoi4dev/
bash install_win.bash # or bash install_mac.bash
```

<br/>

### 配置

```bash
hoi4dev init
```

<br/>

### 路径设置

在用户目录的隐藏文件夹`~/.hoi4dev/`中可以看到设置文件`config.json`。

在Windows上为`C:\Users\<您的用户名>\.hoi4dev\config.json`：
```json
{
    "HOI4_GAME_PATH": "/Users/<您的用户名>/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV/",
    "HOI4_WORKSHOP_PATH": "/Users/<您的用户名>/Library/Application Support/Steam/steamapps/workshop/content/394360/",
    "HOI4_MODS_PATH": "/Users/<您的用户名>/Documents/Paradox Interactive/Hearts of Iron IV/mod/",
    "HOI4_MODS_COMPILE_PATH": "/Users/<您的用户名>/Documents/Paradox Interactive/Hearts of Iron IV/mod/",
    "CURRENT_MOD_PATH": null
}
```

在MacOS上为`/Users/<您的用户名>/.hoi4dev/config.json`）。
```json
{
    "HOI4_GAME_PATH": "C:\\/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV/",
    "HOI4_WORKSHOP_PATH": "C:\\/Program Files (x86)/Steam/steamapps/workshop/content/394360/",
    "HOI4_MODS_PATH": "C:\\/Users/<您的用户名>/Documents/Paradox Interactive/Hearts of Iron IV/mod/",
    "HOI4_MODS_COMPILE_PATH": "C:\\/Users/<您的用户名>/Documents/Paradox Interactive/Hearts of Iron IV/mod/",
    "CURRENT_MOD_PATH": null
}
```

如果您在steam、钢4或者mod安装过程中修改过这些路径，那么您可能需要手动操作。

其中：
- `HOI4_GAME_PATH`应为您的steam钢4本体的安装位置，其中应该包含游戏的可执行文件等大量文件；
- `HOI4_WORKSHOP_PATH`应为您的steam钢4创意工坊下载文件位置（这个路径通常不会用到）；
- `HOI4_MODS_PATH`应为您的钢4所有mod文件的安装位置，注意需要`.mod`文件在其中才能让钢4的启动器识别并加载到mod；
- `HOI4_MODS_COMPILE_PATH`应为您的mod编译后预期的位置（钢4启动器只需要识别`.mod`文件即可，而mod资源文件并不需要和`.mod`文件放在一起。如果您的电脑空间紧张，您可以选择将`HOI4_MODS_COMPILE_PATH`设置为另一个盘或者其他任意位置。通常，如果用户不做设置，这个路径会与`HOI4_MODS_PATH`相同。）；
- `CURRENT_MOD_PATH`是当前正在修改的mod，为工具自行记录，您无需操心。当您有一个正在开发的mod工程文件夹时，可以使用命令`hoi4dev checkout <你的文件夹地址>`来将`CURRENT_MOD_PATH`切换到当前正在修改的mod。

<br/>

## 基础功能

### 钢4脚本CCL语言与JSON格式互相转化

使用`hoi4dev convert -i <输入文件> -o <输出文件>`来自动、智能地从一种格式转为另一种格式。

格式识别取决于文件的后缀名，`.txt`，`.gui`与`.gfx`文件会被视为CCL语言，而`.json`文件会被视为JSON格式。

例如，从一个CCL语言转为JSON格式，在Python代码内，这等价于：
```python
input_file = "<输入文件>"
output_file = "<输出文件>"

ccl_data = ReadTxt(input_file)
json_data = CCL2Dict(ccl_data)

CreateFile(output_file)
SaveJson(json_data, output_file, indent=4)
```

而从JSON格式转为CCL语言则等价于：
```python
input_file = "<输入文件>"
output_file = "<输出文件>"

json_data = LoadJson(input_file)
ccl_data = Dict2CCL(json_data)

CreateFile(output_file)
SaveTxt(ccl_data, output_file)
```

<br/>

### TXT格式的本地化

使用`hoi4dev loc2json -i <输入文件> -o <输出文件> -s <域>`可以将TXT或YML，转换为JSON。格式识别取决于文件的后缀名，`.txt`文件会被视为HOI4DEV定义的本地化文本文件，而`.yml`文件会被视为钢4的本地化格式。`<域>`只对`.txt`文件生效。

在Python代码内，这等价于：
```python
input_file = "<输入文件>"
output_file = "<输出文件>"

json_data = ReadTxtLocs(input_file, scope="<域>") if input.endswith('.txt') else ReadYmlLocs(path=input)

CreateFile(output_file)
SaveJson(json_data, output_file, indent=4)
```

与此同时，用`hoi4dev json2loc -i <输入文件> -o <输出文件>`可以将JSON文件转换为TXT文本文件。由于转为YML后会是多个文件放置在mod的`localisation/`目录中不同地方，需要在mod编译时使用。

在Python代码内，这等价于：
```python
input_file = "<输入文件>"
output_file = "<输出文件>"

json_data = LoadJson(input_file)

CreateFile(output_file)
SaveTxtLocs(json_data, output_file)
```

<br/>

### 图像编辑

图像编辑功能允许用户对图像进行缩放和格式转换，支持多种图像格式，包括`.png`、`.jpg`、`.tga`和P社莫名奇妙就特别喜爱的`.dds`。

使用以下命令进行图像的最基本缩放、裁剪编辑和格式转换：
```bash
hoi4dev imgedit -i <输入文件> -o <输出文件> -r <缩放比例> -w <宽度> -h <高度> -b <行为> -f <翻转TGA> -c <压缩>
```

- `-i`或`--input`: 输入文件路径。
- `-o`或`--output`: 输出文件路径。
- `-r`或`--ratio`: 缩放比例，默认为1。
- `-w`或`--width`: 目标宽度，默认为-1（保持原始宽度）。
- `-h`或`--height`: 目标高度，默认为-1（保持原始高度）。
- `-b`或`--behavior`: 缩放行为，默认为`max`，可选值为`max`或`min`。
- `-f`或`--flip_tga`: 保存`.tga`文件时是否翻转图像，默认为`False`表示不翻转（钢4中的国旗都为上下反转的`.tga`文件）。
- `-c`或`--compression`: 保存编辑后图像时的压缩格式，默认为`dxt3`。仅对`.dds`有效。

请注意此命令的行为：
1. 图像的比例将始终保持，不会出现拉伸、扭曲。
2. 如果给定比例 `r`，图像将始终按比例缩放，然后裁剪 / 扩展（填补透明背景）。`w` 和 `h` 应该要么都不设置，要么都设置，否则会导致错误。
3. 如果没有给定比例，同时既没有给定 `w` 也没有给定 `h`，图像将不会被修改。
4. 否则，如果没有给定比例，同时只给定了 `w` 或 `h` 中的一个，图像将缩放到给定的大小。
5. 如果同时给定了 `w` 和 `h`，如果行为为 'max'，图像将缩放直到两个边都大于给定大小，然后裁剪到给定大小；如果行为为 'min'，图像将缩放直到只有一个边等于给定大小，然后扩展到给定大小。
例如：
- (5, 3) 大小的图像按 `r=2` 缩放将得到 (10, 6)。
- (5, 3) 大小的图像按 `r=2, w=30, h=30` 缩放将得到 (10, 6) 然后扩展到 (30, 30)。
- (5, 3) 大小的图像按 `w=30` 缩放将得到 (30, 18)。
- (5, 3) 大小的图像按 `h=30` 缩放将得到 (50, 30)。
- (5, 3) 大小的图像按 `w=30, h=30, behavior='max'` 缩放将得到 (50, 30) 然后裁剪到 (30, 30)。
- (5, 3) 大小的图像按 `w=30, h=30, behavior='min'` 缩放将得到 (30, 18) 然后扩展到 (30, 30)。

在实际使用中，例如：
```bash
hoi4dev imgedit -i <输入文件> -o <输出文件> -r 2 -w 800 -h 600 -b max -c dxt3
```

会将输入图像放大两倍后，裁剪为800x600（如果小于这个数值会填补透明背景），且如果保存为`.dds`文件会进行压缩。

在Python代码内，这等价于：
```python
input_file = "<输入文件>"
output_file = "<输出文件>"
r = 2  # 缩放比例
w = 800  # 目标宽度
h = 600  # 目标高度
behavior = 'max'  # 缩放行为
flip_tga = False  # 不翻转TGA
compression = 'dxt3'  # 压缩格式

img = ImageLoad(input_file)
edited_img = ImageZoom(img, r=r, w=w, h=h, flip_tga=flip_tga, behavior=behavior)
ImageSave(edited_img, output_file, compression=compression)
```

但值得注意的是，在Python代码内，`flip_tga`默认为真，即默认翻转所有`tga`图片文件。

<br/>

## 进阶功能与工程示例

详见：[使用教程](https://github.com/Magolor/hoi4dev/blob/main/docs/zh/2.%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B.md) 与 [示例-PIHC2模组](https://github.com/Magolor/hoi4dev/blob/main/docs/zh/3.%E7%A4%BA%E4%BE%8B-PIHC2%E6%A8%A1%E7%BB%84.md)

完整的mod开发实例工程：PIHC（The Pony In The High Castle MOD），高堡奇驹模组。

[GitHub链接](https://github.com/Magolor/HOI4-PIHC)（暂时为私密，需要联系作者申请访问；我们将很快开放）。

<br/>

## 更新日志

### v0.1.0.10

- 支持特殊工程、科学家

- `hoi4dev`终端命令自动推断输出路径

- `hoi4dev blueprint`

<br/>

## 联系方式

Talirian:

- QQ: 125657190
- Email: magolorcz@gmail.com

<br/>
