from hoi4dev import *

def AddInventoryItem(path, translate=True):
    '''
    Add an inventory item to the mod.
    Args:
        path: str. The path of the resource files of the inventory item. The resources should include the inventory item icon, the item definition and the localisation.
        translate: bool. Whether to translate the localisation of the inventory item.
    Return:
        None
    '''
    raw_tag = path.strip('/').split('/')[-1].upper()
    idx, tag = int(raw_tag.split('-')[0]), raw_tag.split('-')[1]
    info = merge_dicts([{
        'operations': list()
    }, LoadJson(pjoin(path,"info.json")) if ExistFile(pjoin(path,"info.json")) else dict()])['operations']
    
    # Add item localisation
    locs = AddLocalisation(pjoin(path,"locs.txt"), scope=f"INVENTORY_ITEM_{tag}", translate=translate)
    languages = get_mod_config('languages'); locs[f"INVENTORY_ITEM_{tag}_COUNT"] = dict()
    count_enum = list(range(1, 101)) + list(range(100, 3050, 50)) + [9999]
    for c in count_enum:
        locs[f"CUSTOM_GAIN_INVENTORY_ITEM_{tag}_{c}"] = dict()
        locs[f"CUSTOM_SPEND_INVENTORY_ITEM_{tag}_{c}"] = dict()
        locs[f"CUSTOM_OWN_INVENTORY_ITEM_{tag}_{c}"] = dict()
    locs[f"HAVE_INVENTORY_ITEM_{tag}"] = dict()
    locs[f"HAVE_INVENTORY_ITEM_{tag}_NOT_MET"] = dict()
    for language in languages:
        locs[f"INVENTORY_ITEM_{tag}_COUNT"][language] = f"[?VAR_INVENTORY_ITEM_{tag}|Y0]"
        item_name = locs[f"INVENTORY_ITEM_{tag}"][language]
        if language == 'zh':
            for c in count_enum:
                locs[f"CUSTOM_GAIN_INVENTORY_ITEM_{tag}_{c}"]['zh'] = f"获得物品 §Y{item_name}§! ×§Y{c}§!"
                locs[f"CUSTOM_SPEND_INVENTORY_ITEM_{tag}_{c}"]['zh'] = f"消耗物品 §Y{item_name}§! ×§Y{c}§!"
                locs[f"CUSTOM_OWN_INVENTORY_ITEM_{tag}_{c}"]['zh'] = f"拥有不少于 §Y{c}§! 个物品 §Y{item_name}§!"
            locs[f"HAVE_INVENTORY_ITEM_{tag}"]['zh'] = f"拥有物品 §Y{item_name}§!"
            locs[f"HAVE_INVENTORY_ITEM_{tag}_NOT_MET"]['zh'] = f"需要拥有物品 §Y{item_name}§!，但我们还尚未取得"
        if language == 'en':
            for c in count_enum:
                locs[f"CUSTOM_GAIN_INVENTORY_ITEM_{tag}_{c}"]['en'] = f"Gain Item §Y{item_name}§! ×§Y{c}§!"
                locs[f"CUSTOM_SPEND_INVENTORY_ITEM_{tag}_{c}"]['en'] = f"Spend Item §Y{item_name}§! ×§Y{c}§!"
                locs[f"CUSTOM_OWN_INVENTORY_ITEM_{tag}_{c}"]['en'] = f"Own at least §Y{c}§! Item §Y{item_name}§!"
            locs[f"HAVE_INVENTORY_ITEM_{tag}"]['en'] = f"Own Item §Y{item_name}§!"
            locs[f"HAVE_INVENTORY_ITEM_{tag}_NOT_MET"]['en'] = f"Require Item §Y{item_name}§! but we don’t have it yet"
    for o_idx, operation in enumerate(info):
        if f"INVENTORY_ITEM_{tag}_o{o_idx}_TOOLTIP" not in locs:
            locs[f"INVENTORY_ITEM_{tag}_o{o_idx}_TOOLTIP"] = dict()
        for language in languages:
            locs[f"INVENTORY_ITEM_{tag}_o{o_idx}_TOOLTIP"][language] = f"[!pihc_inventory_item_{tag}_o{o_idx}_button_click_enabled]"+"\n\n[GetCustomEffectTooltip]\n"+f"[!pihc_inventory_item_{tag}_o{o_idx}_button_click]"
    SaveLocs(locs, name=f"INVENTORY_ITEM_{tag}", path=F(pjoin("data","localisation")))
    
    # Add buttons
    scripted_gui = LoadJson(F(pjoin("data","common","scripted_guis","PIHC_inventory.json")))
    interface = LoadJson(F(pjoin("data","interface","PIHC_inventory.json")))
    container = {
        "context_type": "player_context",
        "window_name": f"pihc_inventory_item_{tag}_buttons_container",
        "parent_window_name": "pihc_inventory_container",
        "visible": {
            "is_ai": False,
            "has_variable": "pihc_inventory_open",
            "has_variable__D1": "PIHC_INVENTORY_DISPLAY",
            "check_variable": {
                "var": "PIHC_INVENTORY_DISPLAY",
                "value": idx,
                "compare": "equals"
            }
        },
        "triggers": {
        },
        "effects": {
        },
    }
    guitype = {
        "containerWindowType": {
            "name": f"pihc_inventory_item_{tag}_buttons_container",
            "Orientation": "upper_left",
			"size": {
				"width": 560,
				"height": 100
			},
            "position": {
                "x": 0,
                "y": 610
            },
            "moveable": True,
            "clipping": False,
        }
    }
    STEP_SIZE = 560 // max(len(info), 1)
    for o_idx, operation in enumerate(info):
        if 'type' not in operation:
            operation['type'] = 'click'
        container["triggers"] = container["triggers"] | {
            f"pihc_inventory_item_{tag}_o{o_idx}_button_visible": operation["visible"] if 'visible' in operation else {'always': True}
        }
        if operation['type'] == 'click':
            container["triggers"] = container["triggers"] | {
                f"pihc_inventory_item_{tag}_o{o_idx}_button_click_enabled": operation["trigger"] if 'trigger' in operation else {'always': True}
            }
            container["effects"] = container["effects"] | {
                f"pihc_inventory_item_{tag}_o{o_idx}_button_click": operation["effects"] if 'effects' in operation else dict()
            }
        elif operation['type'] == 'switch':
            container["triggers"] = container["triggers"] | {
                f"pihc_inventory_item_{tag}_o{o_idx}_button_click_enabled": {
                    "if": merge_dicts([{
                        "limit": {
                            "NOT": {
                                "has_country_flag": f"PIHC_INVENTORY_ITEM_{tag}_o{o_idx}_SWITCH_ON"
                            }
                        },
                    },(operation["on_trigger"] if 'on_trigger' in operation else dict())], d=True),
                    "else": (operation["off_trigger"] if 'off_trigger' in operation else dict())
                }
            }
            container["effects"] = container["effects"] | {
                f"pihc_inventory_item_{tag}_o{o_idx}_button_click": {
                    "if": merge_dicts([{
                        "limit": {
                            "NOT": {
                                "has_country_flag": f"PIHC_INVENTORY_ITEM_{tag}_o{o_idx}_SWITCH_ON"
                            }
                        },
                    },(operation["on_effects"] if 'on_effects' in operation else dict()), {
                        "set_country_flag": f"PIHC_INVENTORY_ITEM_{tag}_o{o_idx}_SWITCH_ON"
                    }], d=True),
                    "else": merge_dicts([(operation["off_effects"] if 'off_effects' in operation else dict()), {
                        "clr_country_flag": f"PIHC_INVENTORY_ITEM_{tag}_o{o_idx}_SWITCH_ON"
                    }], d=True)
                }
            }
            SaveJson({
                "defined_text": {
                    "name": f"GetItemSwitchName_{tag}",
                    "text": {
                        "trigger": {
                            "has_country_flag": f"PIHC_INVENTORY_ITEM_{tag}_o{o_idx}_SWITCH_ON"
                        },
                        "localization_key": f"INVENTORY_ITEM_{tag}_o{o_idx}_off"
                    },
                    "text__D1": {
                        "localization_key": f"INVENTORY_ITEM_{tag}_o{o_idx}_on"
                    }
                }
            }, F(pjoin("data","common", "scripted_localisation",f"inventory_items_{tag}_o{o_idx}_switch.json")), indent=4)
        button = {
            "buttonType": {
                "name": f"pihc_inventory_item_{tag}_o{o_idx}_button",
                "quadTextureSprite": "GFX_button_148x34",
                "position": {
                    "x": STEP_SIZE * o_idx + STEP_SIZE//2 + 485,
                    "y": 0
                },
                "buttonText": f"INVENTORY_ITEM_{tag}_o{o_idx}" if operation['type'] == 'click' else f"[GetItemSwitchName_{tag}]",
                "buttonFont": "hoi_20b",
                "Orientation": "upper_left",
                "clicksound": "click_close",
                "oversound": "ui_menu_over",
                "pdx_tooltip": f"INVENTORY_ITEM_{tag}_o{o_idx}_TOOLTIP"
            }
        }
        guitype['containerWindowType'] = merge_dicts([guitype['containerWindowType'], button], d=True)
    interface['guiTypes'] = merge_dicts([interface['guiTypes'], guitype], d=True)
    scripted_gui['scripted_gui'] = merge_dicts([scripted_gui['scripted_gui'],{f"pihc_inventory_item_{tag}_buttons": container}], d=True)
    SaveJson(scripted_gui, F(pjoin("data","common","scripted_guis","PIHC_inventory.json")), indent=4)
    SaveJson(interface, F(pjoin("data","interface","PIHC_inventory.json")), indent=4)
    
    # Add scripted effects
    scripted_effects = dict()
    for c in count_enum:
        scripted_effects = scripted_effects | {
            f"ADD_INVENTORY_ITEM_{tag}_{c}": {
                "custom_effect_tooltip": f"CUSTOM_GAIN_INVENTORY_ITEM_{tag}_{c}",
                "add_to_variable": {f"VAR_INVENTORY_ITEM_{tag}": c},
                "mark_focus_tree_layout_dirty": True
            },
            f"DEL_INVENTORY_ITEM_{tag}_{c}": {
                "custom_effect_tooltip": f"CUSTOM_SPEND_INVENTORY_ITEM_{tag}_{c}",
                "add_to_variable": {f"VAR_INVENTORY_ITEM_{tag}": -c},
                "mark_focus_tree_layout_dirty": True
            }
        }
    SaveJson(scripted_effects, F(pjoin("data","common","scripted_effects",f"PIHC_INVENTORY_ITEM_{tag}.json")), indent=4)
    
    # Add scripted triggers
    scripted_triggers = {
        f"TRIGGER_HAVE_INVENTORY_ITEM_{tag}": {
            "custom_trigger_tooltip": {
                "tooltip": f"HAVE_INVENTORY_ITEM_{tag}",
                "check_variable": {
                    "var": f"VAR_INVENTORY_ITEM_{tag}",
                    "value": 1,
                    "compare": "greater_than_or_equals",
                }
            }
        },
        f"TRIGGER_HAVE_INVENTORY_ITEM_{tag}_IF": {
            "if": {
                "limit": {
                    "NOT": {
                        "check_variable": {
                            "var": f"VAR_INVENTORY_ITEM_{tag}",
                            "value": 1,
                            "compare": "greater_than_or_equals",
                        }
                    }
                },
                "custom_trigger_tooltip": {
                    "tooltip": f"HAVE_INVENTORY_ITEM_{tag}_NOT_MET",
                    "always": False
                }
            }
        }
    }
    for c in count_enum:
        scripted_triggers = scripted_triggers | {
            f"TRIGGER_INVENTORY_ITEM_{tag}_{c}": {
                "custom_trigger_tooltip": {
                    "tooltip": f"CUSTOM_OWN_INVENTORY_ITEM_{tag}_{c}",
                    "check_variable": {
                        "var": f"VAR_INVENTORY_ITEM_{tag}",
                        "value": c,
                        "compare": "greater_than_or_equals",
                    }
                }
            }
        }
    SaveJson(scripted_triggers, F(pjoin("data","common","scripted_triggers",f"PIHC_INVENTORY_ITEM_{tag}.json")), indent=4)
    
    # Add item icons
    w, h = (512, 512); w_s, h_s = (64, 64)
    icon = ImageFind(pjoin(path,"large"), find_default=True)
    if icon is None:
        icon = ImageFind(pjoin(path,"small"), find_default=True)
        if icon is None:
            icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_item")), find_default=False)
            assert (icon is not None), "The default item icon is not found!"
    icon = ImageZoom(icon, w=w, h=h)
    icon_small = ImageFind(pjoin(path,"small"), find_default=True)
    if icon_small is None:
        icon_small = icon.clone()
    icon_small = ImageZoom(icon_small, w=w_s, h=h_s)
    ImageSave(icon, F(pjoin("gfx","interface","inventory_items",f"INVENTORY_ITEM_{tag}")), format='dds')
    ImageSave(icon_small, F(pjoin("gfx","interface","inventory_items",f"INVENTORY_ITEM_{tag}_SMALL")), format='dds')
    Edit(F(pjoin("data","interface","inventory_items",f"INVENTORY_ITEM_{tag}.json")), {'spriteTypes': {
        'spriteType': {"name": f"GFX_INVENTORY_ITEM_{tag}", "texturefile": pjoin("gfx","interface","inventory_items",f"INVENTORY_ITEM_{tag}.dds")},
        'spriteType__D1': {"name": f"GFX_INVENTORY_ITEM_{tag}_SMALL", "texturefile": pjoin("gfx","interface","inventory_items",f"INVENTORY_ITEM_{tag}_SMALL.dds")}
    }})
    
    # Add scripted localisation to support GUI
    DEFINED_TEXT = {
        "GetInventoryItemIcon": "GFX_INVENTORY_ITEM_{tag}_SMALL",
        "GetInventoryItemPicture": "GFX_INVENTORY_ITEM_{tag}",
        "GetInventoryItemName": "INVENTORY_ITEM_{tag}",
        "GetInventoryItemDescription": "INVENTORY_ITEM_{tag}_DESC",
        "GetInventoryItemIconCount": "INVENTORY_ITEM_{tag}_COUNT",
        
        "GetInventoryDisplayItemIcon": "GFX_INVENTORY_ITEM_{tag}_SMALL",
        "GetInventoryDisplayItemPicture": "GFX_INVENTORY_ITEM_{tag}",
        "GetInventoryDisplayItemName": "INVENTORY_ITEM_{tag}",
        "GetInventoryDisplayItemDescription": "INVENTORY_ITEM_{tag}_DESC",
        "GetInventoryDisplayItemIconCount": "INVENTORY_ITEM_{tag}_COUNT"
    }
    for define in DEFINED_TEXT:
        file = F(pjoin("data","common", "scripted_localisation",f"inventory_items_{define}.json"))
        if not ExistFile(file):
            SaveJson({
                "defined_text": {
                    "name": define,
                    "text": {
                        "trigger": {
                            "check_variable": {
                                ("v" if "Display" not in define else "PIHC_INVENTORY_DISPLAY"): 0,
                            },
                        },
                        "localization_key": DEFINED_TEXT[define].format(tag="DEFAULT"),
                    }
                }
            }, file, indent=4)
        Edit(file, {
            "$defined_text": {
                "text": {
                    "trigger": {
                        "check_variable": {
                            ("v" if "Display" not in define else "PIHC_INVENTORY_DISPLAY"): idx,
                        },
                    },
                    "localization_key": DEFINED_TEXT[define].format(tag=tag),
                }
            }
        }, d=True)