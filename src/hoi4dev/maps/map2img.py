from ..utils import *

def extract_by_color(img, color, fill_color=(0,0,0)):
    mask = img.clone()
    mask.transparent_color(Color('rgb({},{},{})'.format(*color)), alpha=0.0, fuzz=0.0, invert=True)
    mask.opaque_paint(target=Color('rgb({},{},{})'.format(*color)), fill=Color('rgb({},{},{})'.format(*fill_color)), fuzz=0.0, invert=False)
    return mask

def PaintBorderColor(img, border_color=(0, 0, 0), K=1):
    '''
    Given an image, paint the border with the given color.
    Args:
        img: image.Image. The image.
        border_color: tuple. The color of the border.
        K: int. The thickness of the border.
    Return:
        image.Image. The image with the border.
    '''
    with img.clone() as mask:
        mask.alpha_channel = 'extract'
        with mask.clone() as eroded:
            eroded.morphology(method='erode', kernel=f'disk:{K}x{K}')
            mask.composite_channel('alpha', eroded, operator='difference')
            border_img = extract_by_color(mask, color=(255,255,255), fill_color=border_color)
            eroded_img = img.clone()
            eroded_img.composite_channel('alpha', eroded, operator='copy_alpha')
            border_img.composite(eroded_img)
            return border_img
    return border_img

def ExtractProvinceImage(prov_id, color=(0,0,0), border_color=(255,255,255), thickness=1):
    '''
    Get the image of a province with the given province id.
    Args:
        prov_id: int. The province id.
        color: tuple. The color of the province.
        border_color: tuple. The color of the border.
        thickness: int. The thickness of the border.
    Return:
        image.Image. The image of the province.
    '''
    assert ExistFile(F("data/map/color2prov.json")), "The color2prov file does not exist."
    assert ExistFile(F("map/provinces.bmp")), "The provinces.bmp file does not exist."
    color2prov = {eval(k):v for k, v in LoadJson(F("data/map/color2prov.json")).items()}
    img = ImageLoad(F("map/provinces.bmp"))

    prov_color = None
    for c, i in color2prov.items():
        if i == int(prov_id):
            prov_color = c
            break
    assert (prov_color is not None), f"The province {prov_id} is not in the color2prov file."
    
    prov_img = extract_by_color(img, prov_color, fill_color=color)
    return prov_img if border_color == color else PaintBorderColor(prov_img, border_color, K=thickness)

def ExtractStateImage(state_id, color=(0,0,0), prov_border_color=(0,0,0), state_border_color=(255,255,255), prov_border_thickness=2, state_border_thickness=4):
    '''
    Get the image of a state with the given state id.
    Args:
        state_id: int. The state id.
        color: tuple. The color of the state.
        prov_border_color: tuple. The color of the province border. Notice that only even numbers are effective.
        state_border_color: tuple. The color of the state border.
        state_border_thickness: int. The thickness of the state border.
    Return:
        image.Image. The image of the state.
    '''
    assert ExistFile(F("data/map/prov2state.json")), "The prov2state file does not exist."
    assert ExistFile(F("data/map/color2prov.json")), "The color2prov file does not exist."
    assert ExistFile(F("map/provinces.bmp")), "The provinces.bmp file does not exist."
    prov2state = LoadJson(F("data/map/prov2state.json"))
    img = ImageLoad(F("map/provinces.bmp"))
    
    state_img = CreateBlankImage(w=img.size[0], h=img.size[1])
    prov_ids = [int(prov_id) for prov_id, state in prov2state.items() if state == int(state_id)]
    prov_imgs = [ExtractProvinceImage(prov_id, color, border_color=prov_border_color, thickness=prov_border_thickness//2) for prov_id in prov_ids]
    for prov_img in prov_imgs: state_img.composite(prov_img)
    return PaintBorderColor(state_img, state_border_color, K=state_border_thickness)

def ExtractStatesImage(state_ids, color=(0,0,0), prov_border_color=(0,0,0), state_border_color=(0,0,0), group_border_color=(255,255,255), prov_border_thickness=2, state_border_thickness=4, group_border_thickness=6):
    '''
    Get the image of a group of states with the given state ids.
    Args:
        state_ids: list. The list of state ids.
        color: tuple. The color of the states.
        prov_border_color: tuple. The color of the province border. Notice that only even numbers are effective.
        state_border_color: tuple. The color of the state border.
        group_border_color: tuple. The color of the group border.
        state_border_thickness: int. The thickness of the state border. Notice that only even numbers are effective.
        group_border_thickness: int. The thickness of the group border.
    Return:
        image.Image. The image of the states.
    '''
    assert ExistFile(F("data/map/prov2state.json")), "The prov2state file does not exist."
    assert ExistFile(F("data/map/color2prov.json")), "The color2prov file does not exist."
    assert ExistFile(F("map/provinces.bmp")), "The provinces.bmp file does not exist."
    img = ImageLoad(F("map/provinces.bmp"))
    
    group_img = CreateBlankImage(w=img.size[0], h=img.size[1])
    state_imgs = [ExtractStateImage(state_id, color, prov_border_color, state_border_color, prov_border_thickness, state_border_thickness//2) for state_id in state_ids]
    for state_img in state_imgs: group_img.composite(state_img)
    return PaintBorderColor(group_img, group_border_color, K=group_border_thickness)

def CreateHighlightImage(img, internal_color, border_color, internal_highlight, border_highlight):
    '''
    Given an image, create a new image with the internal and border highlighted.
    Args:
        img: image.Image. The image.
        internal_color: tuple. The color of the internal.
        border_color: tuple. The color of the border.
        internal_highlight: tuple. The color of the internal highlight.
        border_highlight: tuple. The color of the border highlight.
    Return:
        image.Image. The image with the internal and border highlighted.
    '''
    doubled_img = CreateBlankImage(w=img.width*2, h=img.height)
    doubled_img.composite(img, left=0, top=0)
    highlighted = img.clone()
    highlighted.opaque_paint(target=Color('rgb({},{},{})'.format(*internal_color)), fill=Color('rgb({},{},{})'.format(*internal_highlight)), fuzz=0.0, invert=False)
    highlighted.opaque_paint(target=Color('rgb({},{},{})'.format(*border_color)), fill=Color('rgb({},{},{})'.format(*border_highlight)), fuzz=0.0, invert=False)
    doubled_img.composite(highlighted, left=img.width, top=0)
    return doubled_img

def BatchCreateStateGroupImages(named_state_groups, output_path,
    internal_color = (88, 93, 99), border_color = (158, 158, 158),
    internal_highlight = (152, 157, 163), border_highlight = (222, 222, 222),
    margin = 24,
    processing = False,
    zoom_args = {'r': 1.0},
    alpha = 0.8
):
    '''
    Given a dictionary of state groups, create the hightlight images of all state groups.
    The images will be stored locally in the following folder structure:
    /
    ├── cropped_imgs/
    |   └── *.png
    ├── highlighted_imgs/
    |   └── *.png
    ├── processed_imgs/
    |   └── *.png
    ├── state_group_imgs/
    |   └── *.png
    ├── all_groups_mask.png
    ├── all_groups.png
    ├── bounding_box.json
    ├── cropped_all_groups.png
    ├── highlighted_all_groups.png
    └── processed_all_groups.png
    

    Args:
        named_state_groups: dict. The dictionary of state groups.
        output_path: str. The workspace directory for outputting the images.
        internal_color: tuple. The color of the internal.
        border_color: tuple. The color of the border.
        internal_highlight: tuple. The color of the internal highlight.
        border_highlight: tuple. The color of the border highlight.
        margin: int. The margin of the bounding box.
        processing: bool. Whether to process the images.
        zoom_args: dict. The arguments for zooming. Only effective when processing is True. Using `ImageZoom` method.
    Return:
        None.
        
    For example, a `named_state_groups` for kirins can be:
    KIRIN_STATE_GROUPS = {
        "KIRIN_CENTRAL": [772, 883, 211],
        "KIRIN_WESTERN": [773, 779, 208, 173, 213],
        "KIRIN_NORTHERN": [770, 739, 131, 734, 756, 784, 628],
        "KIRIN_EASTERN": [203, 217, 788, 179, 787, 793, 205, 820, 184, 60, 202],
        "KIRIN_SOUTHERN": [828, 847, 819, 224, 201, 810, 226, 801],
        "KIRIN_FOREST": [731, 736, 742, 759]
    }
    '''
    # STEP 1: Preprocess all state group images
    CreateFolder(pjoin(output_path, "state_group_imgs"))
    state_group_imgs = {}
    for group_name, state_group in named_state_groups.items():
        if ExistFile(pjoin(output_path, f"state_group_imgs/{group_name}.png")):
            state_group_imgs[group_name] = ImageLoad(pjoin(output_path, f"state_group_imgs/{group_name}.png"))
            continue
        group_img = ExtractStatesImage(state_group,
            color = internal_color, prov_border_color = internal_color,
            state_border_color = border_color, group_border_color = border_color,
            prov_border_thickness=0, state_border_thickness=2, group_border_thickness=4
        )
        state_group_imgs[group_name] = group_img
        ImageSave(group_img, pjoin(output_path, f"state_group_imgs/{group_name}.png"))
    
    # STEP 2: Get the a minimal bounding box for all state_groups
    if not ExistFile(pjoin(output_path, "all_groups.png")):
        all_groups_img = state_group_imgs["KIRIN_CENTRAL"].clone()
        for group_name, group_img in state_group_imgs.items():
            all_groups_img.composite(group_img)
        ImageSave(all_groups_img, pjoin(output_path, f"all_groups.png"))
    else:
        all_groups_img = ImageLoad(pjoin(output_path, "all_groups.png"))
    
    if not ExistFile(pjoin(output_path, "bounding_box.json")):
        min_x, min_y, max_x, max_y = all_groups_img.width, all_groups_img.height, 0, 0
        all_groups_img_mask = all_groups_img.clone()
        all_groups_img_mask.alpha_channel = 'extract'
        all_groups_img_mask.depth = 8
        ImageSave(all_groups_img_mask, pjoin(output_path, "all_groups_mask.png"))
        blob = all_groups_img_mask.make_blob(format='RGB')
        for y in range(all_groups_img.height):
            for x in range(all_groups_img.width):
                cursor = (y*all_groups_img.width+x)*3
                if tuple([int(blob[cursor]),int(blob[cursor+1]),int(blob[cursor+2])]) != (0, 0, 0):
                    min_x, min_y, max_x, max_y = min(min_x, x), min(min_y, y), max(max_x, x), max(max_y, y)
        SaveJson({"min_x": min_x, "min_y": min_y, "max_x": max_x, "max_y": max_y}, pjoin(output_path, "bounding_box.json"), indent=4)
    else:
        bounding_box = LoadJson(pjoin(output_path, "bounding_box.json"))
        min_x, min_y, max_x, max_y = bounding_box["min_x"], bounding_box["min_y"], bounding_box["max_x"], bounding_box["max_y"]
    min_x, min_y, max_x, max_y = max(0, min_x-margin), max(0, min_y-margin), min(all_groups_img.width, max_x+margin), min(all_groups_img.height, max_y+margin)

    # STEP 3: Crop all state group images
    CreateFolder(pjoin(output_path, "cropped_imgs"))
    cropped_imgs = dict()
    for group_name, img in state_group_imgs.items():
        cropped_img = img.clone()
        cropped_img.crop(min_x, min_y, max_x, max_y)
        ImageSave(cropped_img, pjoin(output_path, f"cropped_imgs/{group_name}.png"))
        cropped_imgs[group_name] = cropped_img
    cropped_all_groups_img = all_groups_img.clone()
    cropped_all_groups_img.crop(min_x, min_y, max_x, max_y)
    ImageSave(cropped_all_groups_img, pjoin(output_path, "cropped_all_groups.png"))
    
    # STEP 4: Process the images
    def process_imgs(img):
        if not processing: return img

        # 1. Zoom
        zoomed_img = ImageZoom(img, **zoom_args)
        
        # 2. Alpha
        alphaed_img = zoomed_img.clone()
        alphaed_img.transparentize(1-alpha)

        return alphaed_img
    
    CreateFolder(pjoin(output_path, "processed_imgs"))
    processed_imgs = dict()
    for group_name in named_state_groups:
        processed_imgs[group_name] = process_imgs(cropped_imgs[group_name])
        ImageSave(processed_imgs[group_name], pjoin(output_path, f"processed_imgs/{group_name}.png"))
    processed_all_groups_img = process_imgs(cropped_all_groups_img)
    ImageSave(processed_all_groups_img, pjoin(output_path, "processed_all_groups.png"))
    
    # STEP 4: Create the doubled images with highlights for all imgs
    CreateFolder(pjoin(output_path, "highlighted_imgs"))
    for group_name in named_state_groups:
        doubled_img = CreateHighlightImage(processed_imgs[group_name], internal_color, border_color, internal_highlight, border_highlight)
        ImageSave(doubled_img, pjoin(output_path, f"highlighted_imgs/{group_name}.png"))
    doubled_all_groups_img = CreateHighlightImage(cropped_all_groups_img, internal_color, border_color, internal_highlight, border_highlight)
    ImageSave(doubled_all_groups_img, pjoin(output_path, "highlighted_all_groups.png"))
    