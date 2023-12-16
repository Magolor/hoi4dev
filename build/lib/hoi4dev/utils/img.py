from .utils import *

from wand import image
from math import cos, sin, radians

def ImageLoad(path):
    '''
    Load image from a given path.
    Args:
        path: str. Path to the image file.
    Return:
        image.Image. A `wand` image object. None if not found.
    '''
    try:
        return image.Image(filename=path)
    except:
        return None

def ImageSave(img, path, format='dds', flip=False):
    '''
    Save image to the given path with specified format.
    Args:
        path: str. If it contains suffix, the suffix will be replaced with `format`, otherwise the suffix will be appended.
        format: str. Like 'dds', 'tga', 'png', etc.
        flip: bool. Flip image if it is a `tga` file.
    Return:
        None
    
    Optimizations for HOI4:
    - support `dds` compression with `dxt5`.
    - support `tga` flipping.
    '''
    cloned = img.clone()
    if format == 'dds':
        cloned.compression = 'dxt5'
    elif format == 'tga':
        if flip:
            cloned.flip()
    elif format == 'png':
        pass
    else:
        pass
    if not path.endswith(f".{format}"):
        path = '.'.join(path.split('.')[:-1])+f".{format}"
    cloned.save(filename=path)

def ImageFind(path, priority=['png','dds','tga'], find_default=True):
    '''
    Find image in the given path with specified priority.
    Args:
        path: str. Path to the image file.
        priority: list. Priority of suffixes.
        find_default: bool. If True, will find file named `default` and search in it.
    Return:
        image.Image. A `wand` image object. None if not found.
    '''
    for p in priority:
        if ExistFile(pjoin(path, p)):
            return ImageLoad(pjoin(path, p))
    if find_default:
        default_path = '/'.join(path.split('/')[:-1])+'/'+'default'
        for p in priority:
            if ExistFile(pjoin(default_path, p)):
                return ImageLoad(pjoin(default_path, p))
    return None

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
    bg = image.Image(width=w, height=h, background=image.Color('transparent'))
    bg.composite(img, int((w-img.width)/2), int((h-img.height)/2))
    return bg

def ImageZoom(img, r=1, w=-1, h=-1, behavior='max'):
    '''
    Zoom image to the given size and crop/extend it accordingly to fit the desired size `(w,h)`. The extend image will be centered and filled with transparent color.
    Args:
        img: image.Image. A `wand` image object.
        r: float. Ratio.
        w: int. Width.
        h: int. Height.
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
    cloned = img.clone()
    if r:
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
    bg = image.Image(width=rot_w, height=rot_h, background=image.Color('transparent'))
    bg.composite(img, int((rot_w-img.width)/2), int((rot_h-img.height)/2))
    bg.rotate(angle, background=image.Color('transparent'))
    return bg