from .config import *
import numpy as np

# TODO: For some reason, Wand/Imagemagick is glitchy when saving dds files, resulting in strange artifacts.

try:
    from wand import image
    from wand.color import Color
    from wand.image import Image
    from wand.drawing import Drawing
    from wand.display import display
    from wand.api import library
    from ctypes import c_void_p, c_size_t
    library.MagickSetCompressionQuality.argtypes = [c_void_p, c_size_t]
except Exception as e:
    print(e)
from math import cos, sin, radians

def rgb2hex(rgb):
    r, g, b = rgb
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def hex2rgb(hex):
    if hex.startswith('#'):
        hex = hex[1:]
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def hoi4dev_auto_image(
    path,
    searches = ["icon", "default"],
    resource_type = "idea",
    resource_default = True,
    scale = (-1, -1),
    cache_key = None,
    compression = 'dxt3',
    force = False
):
    cache_path = pjoin(path, ".cache", f"{resource_type}_{cache_key}.dds" if cache_key else f"{resource_type}.dds")
    if (not force) and ExistFile(cache_path):
        return ImageLoad(cache_path)
    if isinstance(scale, str):
        scale = get_mod_config('img_scales')[scale]
    w, h = scale
    icon = None
    for search in searches:
        if icon is None:
            icon = ImageFind(pjoin(path, search))
        else:
            break
    if (icon is None) and resource_default:
        if resource_default==True: resource_default = f"default_{resource_type}"
        else: resource_default = f"default_{resource_default}"
        icon = ImageFind(pjoin("hoi4dev_settings", "imgs", "defaults", resource_default), find_default=False)
        assert (icon is not None), f"The default {resource_type} icon is not found in {path}!"
    if icon is not None:
        icon = ImageZoom(icon, w=w, h=h)
        if force or (not ExistFile(cache_path)):
            CreateFolder(pjoin(path, ".cache"))
            ImageSave(icon, cache_path, format='dds', compression=compression)
    return icon

def IsImagePath(path):
    '''
    Determine whether the file has format 'dds', 'tga', 'png'.
    Args:
        path: str. Path to the file with suffix.
    Return:
        bool. True if the file is an image file.
    '''
    return path.endswith('.dds') or path.endswith('.tga') or path.endswith('.png')
    

def ImageLoad(path):
    '''
    Load image from a given path.
    Args:
        path: str. Path to the image file.
    Return:
        image.Image. A `wand` image object. None if not found.
    '''
    try:
        img = image.Image(filename=path, depth=32)
        return img
    except TypeError as e:
        print(e)
        return None

def ImageShow(img):
    '''
    Show the image.
    Args:
        img: image.Image. A `wand` image object.
    Return:
        None
    '''
    display(img)

STABLE_EXPORT = os.environ.get('HOI4DEV_STABLE_EXPORT',False)
def ImageSave(img, path, format=None, flip_tga=True, compression='dxt3'):
    '''
    Save image to the given path with specified format.
    Args:
        path: str. If it contains suffix, the suffix will be replaced with `format`, otherwise the suffix will be appended.
        format: str. Like 'dds', 'tga', 'png', etc. If not set, will use the suffix of `path`.
        flip_tga: bool. Flip image if it is a `tga` file (specialized for HoI4 country flags).
        compression: str. Compression method. Default is 'dxt3'. Only works for `dds` files.
    Return:
        None
    
    Optimizations for HOI4:
    - support `dds` compression with `dxt3` by default.
    - support `tga` flipping.
    '''
    cloned = img.clone()
    cloned.alpha_channel = "set"
    library.MagickSetCompressionQuality(cloned.wand, 100)
    if STABLE_EXPORT:
        time.sleep((cloned.size[0]*cloned.size[1]/2073600)*2.0+0.2) # 4.0s for each 4K image
    if format == 'dds' or ((format is None) and path.endswith('.dds')):
        if compression is not None:
            cloned.compression = compression
            cloned.options['dds:mipmaps'] = '0'
    elif format == 'tga' or ((format is None) and path.endswith('.tga')):
        if flip_tga:
            cloned.flip()
    elif format == 'png' or ((format is None) and path.endswith('.png')):
        pass
    else:
        pass
    if format and (not path.endswith(f".{format}")):
        path = AsFormat(path, format)
    CreateFile(path)
    cloned.save(filename=path)

def ImageFind(path, priority=['png','dds','tga'], find_default=True):
    '''
    Find image in the given path with specified priority.
    Args:
        path: str. Path to the image file without suffix.
        priority: list. Priority of suffixes.
        find_default: bool. If True, will find file named `default` and search in it.
    Return:
        image.Image. A `wand` image object. None if not found.
    
    Notice that the function first search by the given path (assuming suffix contained).
    Otherwise, it will search by the given path with each suffix in `priority` appended.
    Finally, if `find_default` is True, it will search by the given path with `default` appended.
    '''
    if ExistFile(path):
        return ImageLoad(path)
    for p in priority:
        if ExistFile('.'.join([path, p])):
            return ImageLoad('.'.join([path, p]))
    if find_default:
        default_path = '/'.join(path.split('/')[:-1])+'/'+'default'
        for p in priority:
            if ExistFile('.'.join([default_path, p])):
                return ImageLoad('.'.join([default_path, p]))
    return None

def ImageCopy(src_path, tgt_path, priority=['png','dds','tga'], find_default=True, format=None, flip_tga=False):
    '''
    Copy image from `src_path` to `tgt_path` with specified priority and save format.
    Args:
        src_path: str. Path to the source image file.
        tgt_path: str. Path to the target image file.
        priority: list. Priority of suffixes.
        find_default: bool. If True, will find file named `default` and search in it.
        format: str. Like 'dds', 'tga', 'png', etc.
        flip_tga: bool. Flip image if it is a `tga` file (specialized for HoI4 country flags).
    Return:
        None
    '''
    img = ImageFind(src_path, priority=priority, find_default=find_default)
    if img is not None:
        ImageSave(img, tgt_path, format=format, flip_tga=flip_tga)
    else:
        raise FileNotFoundError(f"Image not found: \"{src_path}\"!")

def CreateBlankImage(w, h, color='transparent'):
    '''
    Create a blank image with the given size and color (transparent by default).
    Args:
        w: int. Width.
        h: int. Height.
        color: str. Color (transparent by default).
    Return:
        image.Image. A `wand` image object.
    '''
    return image.Image(width=w, height=h, background=Color(color) if isinstance(color,str) else color)

def ImageExtend(img, w, h):
    '''
    Extend image to the given size. The extended image will be centered and filled with transparent color.
    Args:
        img: image.Image. A `wand` image object.
        w: int. Width.
        h: int. Height.
    Return:
        image.Image. The extended image.
    
    Notice that if `(w,h)` is smaller than `(img.width,img.height)`, the image will be cropped.
    '''
    bg = CreateBlankImage(w,h)
    bg.composite(img, int((w-img.width)/2), int((h-img.height)/2))
    return bg

def ImageZoom(img, r=1, w=-1, h=-1, behavior='max'):
    '''
    Zoom image to the given size and crop/extend it accordingly to fit the desired size `(w,h)`. The extend image will be centered and filled with transparent color.
    Args:
        img: image.Image. A `wand` image object.
        r: float. Ratio.
        w: int. Width. If a float is given, it will be converted to int first.
        h: int. Height. If a float is given, it will be converted to int first.
        behavior: str. 'max' or 'min'.
    Return:
        image.Image. The zoomed image.
    
    Please pay attention to the behavior of this function:
    0. The ratio of the image will always be kept.
    1. If the ratio `r` is given, the image will alwyas be zoomed by the ratio and then cropped/extended. `w` and `h` should be either not set, or both set, otherwise leads to an error.
    2. If neither `w` nor `h` is given, the image will not be modified.
    3. Otherwise, if only one of `w` and `h` is given, the image will be zoomed to the given size.
    4. If both `w` and `h` are given, if behavior is 'max', the image will be zoomed until both sides are larger than the given size, and then cropped to the given size; if behavior is 'min', the image will be zoomed unti only one side is larger than the given size, and then extended to the given size.
    Examples:
        (5, 3) zoom with `r=2` will result in (10, 6).
        (5, 3) zoom with `r=2, w=30, h=30` will result in (10, 6) and then extended to (30, 30).
        (5, 3) zoom with `w=30` will result in (30, 18).
        (5, 3) zoom with `h=30` will result in (50, 30).
        (5, 3) zoom with `w=30, h=30, behavior='max'` will result in (50, 30) and then cropped to (30, 30).
        (5, 3) zoom with `w=30, h=30, behavior='min'` will result in (30, 18) and then extended to (30, 30).
    '''
    cloned = img.clone(); w = int(w); h = int(h)
    if r != 1:
        cloned.resize(int(cloned.width*r), int(cloned.height*r), filter='lanczos', blur=0)
        assert ((w!=-1 and h!=-1) or (w==-1 and h==-1)), "When the ratio `r` is given, `w` and `h` should be either not set, or both set!"
        return cloned if (w==-1 and h==-1) else ImageExtend(cloned, w, h)
    if w == -1 and h == -1:
        return cloned
    w_zoom_ratio = w / img.width; w_w = w; w_h = int(img.height*w_zoom_ratio)
    h_zoom_ratio = h / img.height; h_w = int(img.width*h_zoom_ratio); h_h = h
    min_w = min(w_w, h_w); min_h = min(w_h, h_h)
    max_w = max(w_w, h_w); max_h = max(w_h, h_h)
    if w==-1:
        cloned.resize(h_w, h_h, filter='lanczos', blur=0)
    elif h==-1:
        cloned.resize(w_w, w_h, filter='lanczos', blur=0)
    else:
        if behavior == 'max':
            cloned.resize(max_w, max_h, filter='lanczos', blur=0)
            cloned.crop(width=w, height=h, gravity='center')
        elif behavior == 'min':
            cloned.resize(min_w, min_h, filter='lanczos', blur=0)
            cloned = ImageExtend(cloned, w, h)
    return cloned

def ImageRotate(img, angle):
    '''
    Rotate image to the given angle. The rotated image will be centered and filled with transparent color.
    Args:
        img: image.Image. A `wand` image object.
        angle: float. Angle in degree (clockwise).
    Return:
        image.Image. The rotated image.
    
    Notice that the image will always be zoomed larger or smaller to fit the rotated image.
    '''
    rot_w = int(img.width*abs(cos(radians(angle))) + img.height*abs(sin(radians(angle))))
    rot_h = int(img.width*abs(sin(radians(angle))) + img.height*abs(cos(radians(angle))))
    bg = CreateBlankImage(rot_w, rot_h)
    bg.composite(img, int((rot_w-img.width)/2), int((rot_h-img.height)/2))
    bg.rotate(angle, background=Color('transparent'))
    return bg

def ImageShift(img, dw=0, dh=0):
    '''
    Shift image by the given offset. The image will be extended to (w+dw,h+dh) and the shifted image will be filled with transparent color.
    Args:
        img: image.Image. A `wand` image object.
        dw: int. Offset along width. Positive value means shift right.
        dh: int. Offset along height. Positive value means shift down.
    Return:
        image.Image. The shifted image.
    '''
    ext = ImageExtend(img, w=img.width+abs(dw)*2, h=img.height+abs(dh)*2)
    ext.crop(left=max(-dw,0), top=max(-dh,0), width=img.width+abs(dw), height=img.height+abs(dh))
    return ext

def ImageComposite(imgs):
    '''
    Composite images together. The images will be centered and filled with transparent color.
    Args:
        imgs: list[image.Image]. A list of `wand` image objects.
    Return:
        image.Image. The composited image.
    '''
    assert len(imgs) > 0, "No image to composite!"
    w, h = max([img.width for img in imgs]), max([img.height for img in imgs])
    bg = CreateBlankImage(w, h)
    for img in imgs:
        bg.composite(img, gravity='center')
    return bg

def ImageColorTransfer(img, src_color, tgt_color, intensity=0.3):
    '''
    Transfer the color of the image from `src_color` to `tgt_color`.
    Args:
        img: image.Image. A `wand` image object.
        src_color: str. Source color in hex format.
        tgt_color: str. Target color in hex format.
        intensity: float. Intensity of the color transfer (0.0-1.0). 1.0 means painting, while 0.0 means no change.
    Return:
        image.Image. The color transferred image.
    '''
    cloned = img.clone()
    src_color = Color(src_color)
    inv_src_color = Color(rgb2hex((255-src_color.red_int8, 255-src_color.green_int8, 255-src_color.blue_int8)))
    alpha = Color(rgb2hex((int(255*intensity), int(255*intensity), int(255*intensity))))
    cloned.colorize(Color(tgt_color), alpha)
    cloned.colorize(inv_src_color, alpha)
    return cloned

def ImageGammaCorrection(img, gammas=[0.8, 0.9, 1.33, 1.66]):
    '''
    Perform gamma correction on the image.
    Args:
        img: image.Image. A `wand` image object.
        gammas: list[float]. A list of gamma values.
    Return:
        image.Image. The gamma corrected image.
    '''
    cloned = img.clone()
    for gamma in gammas:
        cloned.gamma(gamma)
    return cloned

def ImageMask(img, mask, color='transparent'):
    '''
    Mask the image with the given mask.
    Args:
        img: image.Image. A `wand` image object.
        mask: image.Image. A `wand` image object, supposed to be black and white. White part will be kept.
        color: str. Color of the background after masking (transparent by default).
    Return:
        image.Image. The masked image.
    '''
    cloned = img.clone()
    bg = CreateBlankImage(img.width, img.height, color)
    alpha = mask.clone()
    alpha.transform_colorspace('gray')
    alpha.alpha_channel = 'copy'
    cloned.composite_channel('alpha', alpha, 'copy_alpha')
    bg.composite(cloned)
    return bg

def CreateLeaderImage(img):
    '''
    Convert an image to a leader image.
    Args:
        img: image.Image. A `wand` image object.
    Return:
        image.Image. The leader image.
    '''
    w_l, h_l = get_mod_config('img_scales')['leader_portrait']
    return ImageZoom(img, w=w_l, h=h_l)

def CreateAdvisorImage(img):
    '''
    Convert a portrait image to an advisor image. The default HOI4 advisor template and size is used.
    Args:
        img: image.Image. A `wand` image object.
    Return:
        image.Image. The advisor image.
    '''
    w_l, h_l = get_mod_config('img_scales')['leader_portrait']
    w_a, h_a = get_mod_config('img_scales')['advisor_portrait']
    bg = CreateBlankImage(w_a,h_a)
    ft = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "advisor_template")), find_default=False)
    assert (ft is not None), "Advisor template not found!"
    adv = ImageZoom(ImageZoom(img, w=w_l, h=h_l), h=h_a)
    rot = ImageZoom(ImageRotate(adv, 355.5), r=0.72)
    bg.composite(rot, top=4, left=4)
    bg.composite(ft, gravity='center')
    return bg

def CreateCountryEventImage(img):
    '''
    Convert a image to a country event image. The default HOI4 country event template and size is used.
    Args:
        img: image.Image. A `wand` image object.
    Return:
        image.Image. The country event image.
    '''
    w, h = get_mod_config('img_scales')['country_event']
    bg = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "country_event_template")), find_default=False)
    assert (bg is not None), "Country event template not found!"
    evt = ImageZoom(img, w=w, h=h)
    rot = ImageZoom(ImageRotate(evt, 355.5), r=0.90)
    sft = ImageShift(rot, dw=-2)
    bg.composite(sft, gravity='center')
    return bg

def CreateIntelAgencyImage(img):
    '''
    Convert a image to an intelligence agency image.
    Args:
        img: image.Image. A `wand` image object.
    Return:
        image.Image. The country event image.
    '''
    W, H = get_mod_config('img_scales')['intel_agency_full']
    w, h = get_mod_config('img_scales')['intel_agency']
    bg = CreateBlankImage(W, H)
    img = ImageZoom(img, w=w, h=h)
    bg.composite(img, gravity='west')
    shd = img.clone()
    shd.shadow(1.0, 1.0, 0, 0)
    shd = ImageExtend(ImageZoom(shd, r=1.1), w, h)
    # Thickening the shadow
    for _ in range(8):
        bg.composite(shd, gravity='east')
    bg.composite(img, gravity='east')
    return bg

def CreateBlueprintImage(img, color='white', radius=10.0, bg_color='blue', threshold=0.15, add_grid=6, grid_color='white', grid_opacity=0.2, grid_width=None):
    '''
    Convert a image to a blueprint image.
    Args:
        img: image.Image. A `wand` image object.
        color: str. Color ('white' by default). Use by the blueprint lines.
        radius: int. Width of the blueprint lines.
        bg_color: str. Color (transparent by default).
        threshold: float. Threshold for edge detection. The lower threshold will be `0.7*threshold` and the upper threshold will be `1.3*threshold`.
        add_grid: int. Whether to add a grid to the blueprint. If an integer > 0, the grid will be added with the given size. If 0, no grid will be added.
        grid_color: str. Color ('white' by default). Use by the grid.
        grid_opacity: float. Opacity of the grid.
        grid_width: int. Width of the grid. If None, will auto to 1/10 of the grid size.
    Return:
        image.Image. The blueprint image.
    '''
    lines = img.clone()

    # Step 1: Extract edges
    lines.transform_colorspace('gray')
    lines.gaussian_blur(radius=radius/3)
    lower = max(0, 0.7*threshold)
    upper = min(1, 1.3*threshold)
    lines.canny(radius=radius, lower_percent=lower, upper_percent=upper)
    
    # Now we have a image of white lines on a black background
    # Step 2: Extract the white lines, and make black background transparent
    lines.transparent_color(Color('white'), alpha=1)
    lines.alpha_channel = 'remove'
    lines.transparent_color(Color('black'), alpha=0)
    lines.alpha_channel = 'set'
    
    # Step 3: Thickening the lines by dilation
    lines.morphology('dilate', 'octagon', iterations=1)
    
    # Step 4: Change the color of the lines
    if color != 'white':
        lines.colorize(Color(color), Color('white'))
    
    # Step 4: Composite the lines over a blue background
    bg = CreateBlankImage(img.width, img.height, bg_color)
    if add_grid > 0:
        grid = CreateBlankImage(img.width, img.height, 'transparent')
        with Drawing() as draw:
            draw.fill_color = Color(grid_color)
            draw.fill_opacity = grid_opacity
            draw.stroke_color = Color(grid_color)
            draw.stroke_opacity = grid_opacity
            if grid_width is None:
                grid_width = add_grid // 10
            draw.stroke_width = int(grid_width)
            for x in range(add_grid//2, img.width, add_grid):
                draw.line((x, 0), (x, img.height))
            for y in range(add_grid//2, img.height, add_grid):
                draw.line((0, y), (img.width, y))
            draw(grid)
        bg.composite(grid, 0, 0)
    bg.composite(lines, 0, 0)
    return bg

def SetLoadingScreenImages(imgs, main=None):
    '''
    Set loading screen images.
    Args:
        imgs: list[img.Image]. A list of images, each of which is a `wand` image object.
        main: img.Image. The main image. A `wand` image object. If not specified, will use the 5th image in `imgs` which is the default behavior of HoI4.
    Return:
        None
    '''
    if main is None and len(imgs)<5:
        raise ValueError("No main image!")
    if main is None:
        main = imgs[4]
    else:
        imgs = imgs[:4] + [main] + imgs[4:]
    CreateFolder(F(pjoin("gfx","loadingscreens")))
    w_l, h_l = get_mod_config('img_scales')['loadingscreen']
    w_m, h_m = get_mod_config('img_scales')['mainscreen']
    for i, img in enumerate(imgs):
        ImageSave(ImageZoom(img, w=w_l, h=h_l), F(pjoin("gfx","loadingscreens",f"load_{i+1}")), format='dds')
    main_img = ImageZoom(main, w=w_m, h=h_m)
    # Should the main image be saved with a 'loadingscreens' ratio?
    ImageSave(main_img, F(pjoin("gfx","loadingscreens",f"load_5")), format='dds')
    # Together for Victory
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_tfv")), format='dds')
    # Death or Dishonor
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_dod")), format='dds')
    # Waking the Tiger
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_tiger")), format='dds')
    # Man the Guns
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_mtg")), format='dds')
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_mtg_2")), format='dds')
    # La Resistance
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_lar")), format='dds')
    # Battle for the Bosporus
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_botb")), format='dds')
    # No Step Back
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_nsb")), format='dds')
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_nsb2")), format='dds')
    # By Blood Alone
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_bba")), format='dds')
    # Arms Against Tyranny
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_aat")), format='dds')
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_aat2")), format='dds')
    # Trial of Allegiance
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_toa")), format='dds')
    # Gotterdammerung
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_ww")), format='dds')
    # Graveyard of Empires
    ImageSave(main_img, F(pjoin("gfx","loadingscreens","load_goe")), format='dds')
