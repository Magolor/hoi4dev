from .config import *

try:
    from wand import image
    from wand.color import Color
    from wand.image import Image
    from wand.drawing import Drawing
except Exception as e:
    print(e)
from math import cos, sin, radians

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
    if format == 'dds' or ((format is None) and path.endswith('.dds')):
        if compression is not None:
            cloned.compression = compression
    elif format == 'tga' or ((format is None) and path.endswith('.tga')):
        if flip_tga:
            cloned.flip()
    elif format == 'png' or ((format is None) and path.endswith('.png')):
        pass
    else:
        pass
    if format and (not path.endswith(f".{format}")):
        path = AsFormat(path, format)
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
    return image.Image(width=w, height=h, background=image.Color(color))

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
        cloned.resize(int(cloned.width*r), int(cloned.height*r))
        assert ((w!=-1 and h!=-1) or (w==-1 and h==-1)), "When the ratio `r` is given, `w` and `h` should be either not set, or both set!"
        return cloned if (w==-1 and h==-1) else ImageExtend(cloned, w, h)
    if w == -1 and h == -1:
        return cloned
    w_zoom_ratio = w / img.width; w_w = w; w_h = int(img.height*w_zoom_ratio)
    h_zoom_ratio = h / img.height; h_w = int(img.width*h_zoom_ratio); h_h = h
    min_w = min(w_w, h_w); min_h = min(w_h, h_h)
    max_w = max(w_w, h_w); max_h = max(w_h, h_h)
    if w==-1:
        cloned.resize(h_w, h_h)
    elif h==-1:
        cloned.resize(w_w, w_h)
    else:
        if behavior == 'max':
            cloned.resize(max_w, max_h)
            cloned.crop(width=w, height=h, gravity='center')
        elif behavior == 'min':
            cloned.resize(min_w, min_h)
            cloned = ImageExtend(cloned, w, h)
    return cloned

def ImageRotate(img, angle):
    '''
    Rotate image to the given angle. The rotated image will be centered and filled with transparent color.
    Args:
        img: image.Image. A `wand` image object.
        angle: float. Angle in degree.
    Return:
        image.Image. The rotated image.
    
    Notice that the image will always be zoomed larger or smaller to fit the rotated image.
    '''
    rot_w = int(img.width*abs(cos(radians(angle))) + img.height*abs(sin(radians(angle))))
    rot_h = int(img.width*abs(sin(radians(angle))) + img.height*abs(cos(radians(angle))))
    bg = CreateBlankImage(rot_w, rot_h)
    bg.composite(img, int((rot_w-img.width)/2), int((rot_h-img.height)/2))
    bg.rotate(angle, background=image.Color('transparent'))
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
