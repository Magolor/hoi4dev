from hoi4dev import *

KIRIN_STATE_GROUPS = {
    "KIRIN_CENTRAL": [772, 883, 211],
    "KIRIN_WESTERN": [773, 779, 208, 173, 213],
    "KIRIN_NORTHERN": [770, 739, 131, 734, 756, 784, 628],
    "KIRIN_EASTERN": [203, 217, 788, 179, 787, 793, 205, 820, 184, 60, 202],
    "KIRIN_SOUTHERN": [828, 847, 819, 224, 201, 810, 226, 801],
    "KIRIN_FOREST": [731, 736, 742, 759]
}
KIRIN_ID_MAPPING = {
    "KIRIN_CENTRAL": 1,
    "KIRIN_WESTERN": 2,
    "KIRIN_NORTHERN": 3,
    "KIRIN_EASTERN": 4,
    "KIRIN_SOUTHERN": 5,
    "KIRIN_FOREST": 6
}

def add_Kirin_state_group_gui():
    workspace_path = "./scripts/region_gui/Kirin/"
    CreateFolder(workspace_path)
    BatchCreateStateGroupImages(named_state_groups=KIRIN_STATE_GROUPS, output_path=workspace_path,
        internal_color = (199,196,151),
        border_color = (170,168,133),
        internal_highlight = (221,221,192),
        border_highlight = (195,195,168),
        processing = True,
        alpha = 0.8,
    )
    nirik_workspace_path = "./scripts/region_gui/nirik/"
    CreateFolder(nirik_workspace_path)
    BatchCreateStateGroupImages(named_state_groups=KIRIN_STATE_GROUPS, output_path=nirik_workspace_path,
        internal_color = (90,77,85),
        border_color = (53,42,48),
        internal_highlight = (158,141,148),
        border_highlight = (109,97,103),
        processing = True,
        alpha = 0.8,
    )
    gfxs_path = "./resources/copies/gfx/interface/state_group_guis/"
    interface_path = "./resources/copies/data/interface/"
    sprites = dict()
    for group_name in KIRIN_STATE_GROUPS:
        img = ImageLoad(pjoin(workspace_path, f"highlighted_imgs/{group_name}.png"))
        ImageSave(img, pjoin(gfxs_path, f"{group_name}.dds"), compression='no')
        sprites = merge_dicts([sprites, {
            "spriteType": {
                "name": f"GFX_state_group_gui_KIRIN_{KIRIN_ID_MAPPING[group_name]}",
                "textureFile": f"gfx/interface/state_group_guis/{group_name}.dds",
                "noOfFrames": 2,
                "transparencecheck": True
            }
        }], d=True)
        img = ImageLoad(pjoin(nirik_workspace_path, f"highlighted_imgs/{group_name}.png"))
        ImageSave(img, pjoin(gfxs_path, f"{group_name}_nirik.dds"), compression='no')
        sprites = merge_dicts([sprites, {
            "spriteType": {
                "name": f"GFX_state_group_gui_KIRIN_{KIRIN_ID_MAPPING[group_name]}_nirik",
                "textureFile": f"gfx/interface/state_group_guis/{group_name}_nirik.dds",
                "noOfFrames": 2,
                "transparencecheck": True
            }
        }], d=True)
    SaveJson({'spriteTypes': sprites}, pjoin(interface_path, "PIHC_C18_state_group_gui_gfx.json"), indent=4)
    SaveJson({
        'guiTypes': {
            "containerWindowType": {
                "name": "C18_state_group_gui_entry_container",
                "buttonType": {
                    "name": "state_group_btn",
                    "spriteType": "GFX_state_group_gui_KIRIN_1",
                    "pdx_tooltip": "C18_state_group_btn_tooltip",
                    "scale": 0.75
                },
                "buttonType__D1": {
                    "name": "state_group_btn_nirik",
                    "spriteType": "GFX_state_group_gui_KIRIN_1_nirik",
                    "pdx_tooltip": "C18_state_group_btn_nirik_tooltip",
                    "scale": 0.75
                }
            }
        }
    }, pjoin(interface_path, "PIHC_C18_state_group_gui.json"), indent=4)


def add_Kirin_state_group_update_effects():
    info = dict()
    with open("./resources/locs/C18_modifications.txt", "w") as f:
        for r in "0123456":
            for o in ["ADD", "DEL"]:
                for t in ["NIRIK", "GROWTH"]:
                    for p in list(range(1,25)) + list(range(25, 105, 5)) + [200]:
                        key = f"C18_{o}_{t}_{r}_{p}"; v = 1+p/100 if o=="ADD" else 1-p/100
                        info[key] = {
                            "custom_effect_tooltip": f"{key}_TOOLTIP",
                        }
                        rs = [int(r)] if r!='0' else [1,2,3,4,5,6]
                        var = "C18.ARRAY_REGIONAL_DEV_REGIONS_NIRIKS_PERCENTAGE" if t=="NIRIK" else "C18.ARRAY_REGIONAL_DEV_REGIONS_NIRIKS_WEEKLY_FACTOR"
                        for r_ in rs:
                            info[key] = merge_dicts([info[key], { "multiply_variable": { var+f"^{r_-1}" : float(f"{v:.2f}") } }, {
                                "clamp_variable": {
                                    "var": var+f"^{r_-1}",
                                    "min": 0.005,
                                    "max": 100.0
                                },
                            }], d=True)
                        
                        if t == "NIRIK":
                            info[key] = merge_dicts([info[key], { "C18_REGIONAL_DEV_COMPUTE": True }], d=True)
                        
                        locs = (
f"""[zh.{key}_TOOLTIP]
§C{'全国' if r=='0' else '$C18_REGIONAL_DEV_STATE_GROUP_'+r+'$'}§!的§0逆麟率§!§{'G-' if o=='DEL' else 'R+'}{p:.1f}%§!（相对值）。
[en.{key}_TOOLTIP]
The §C{'nation' if r=='0' else '$C18_REGIONAL_DEV_STATE_GROUP_'+r+'$'}§!’s §0Nirik Rate§! §{'G-' if o=='DEL' else 'R+'}{p:.1f}%§! (relative value).
""") if t=="NIRIK" else (
f"""[zh.{key}_TOOLTIP]
§C{'全国' if r=='0' else '$C18_REGIONAL_DEV_STATE_GROUP_'+r+'$'}§!的§0逆麟率增长速度§! §{'G-' if o=='DEL' else 'R+'}{p:.1f}%§!。
[en.{key}_TOOLTIP]
The §C{'nation' if r=='0' else '$C18_REGIONAL_DEV_STATE_GROUP_'+r+'$'}§!’s §0Nirik Rate Growth§! §{'G-' if o=='DEL' else 'R+'}{p:.1f}%§!.
""")
                        f.write(locs + "\n")
    SaveJson(info, "./resources/copies/data/common/scripted_effects/PIHC_C18_MODIFICATIONS.json", indent=4)

if __name__=="__main__":
    add_Kirin_state_group_gui()
    add_Kirin_state_group_update_effects()
    