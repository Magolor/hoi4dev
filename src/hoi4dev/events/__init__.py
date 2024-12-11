from ..utils import *
from ..translation import AddLocalisation

def AddEvent(path, space, translate=True):
    '''
    Add a event to the mod.
    Args:
        path: str. The path of the resource files of the event. The resources should include the event image (optional), the event definition and the localisation.
        space: str. The space of the event.
        translate: bool. Whether to translate the localisation of the country.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].split('-',1)[0]
    assert (tag.isdigit()), f"Event tag should be numeric, but got {tag}."
    tag = int(tag)
    info = merge_dicts([{
        'id': f"{space}.{tag}",
        'picture': f"GFX_EVENT_{space}_{tag}",
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    category = info.pop('category', 'country')
    if 'title' not in info:
        info['title'] = f"EVENT_{space}_{tag}"
    if 'desc' not in info:
        info['desc'] = f"EVENT_{space}_{tag}_desc"
    if 'options' in info:
        options = info.pop('options')
        for o in options:
            info[find_dup('option', info)] = o
    for o in info:
        if find_ori(o)=='option':
            c = find_idx(o)
            if 'name' not in info[o]:
                info[o]['name'] = f"EVENT_{space}_{tag}_o{c}"
    if 'date' in info:
        date = info.pop('date')
        assert ("date_scope" in info), f"Event {space}.{tag} has 'date' but no 'date_scope'."
        date_scope = info.pop('date_scope')
        bookmark_date = get_mod_config('bookmark_date')
        if '~' in date:
            start_date, end_date = [d.strip() for d in date.split('~')]
            delta = get_num_days(start_date, end_date)
        else:
            start_date, delta = date.strip(), 0
        on_action = {
            "on_startup": {
                "effect": {
                    date_scope: {
                        f"{category}_event": {
                            "id": f"{space}.{tag}",
                            "days": get_num_days(bookmark_date,start_date),
                        } | ({"random_days": delta} if delta else {})
                    }
                }
            }
        }
        SaveJson({"on_actions": on_action}, F(pjoin("data","common","on_actions",f"EVENT_{space}_{tag}_on_actions.json")), indent=4)

    # Add event localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"EVENT_{space}_{tag}", translate=translate)
    
    # Initialize event definition (An empty event space folder is added if not exists)
    space_path = F(pjoin("data","event_spaces",space)); CreateFolder(space_path)
    Edit(F(pjoin("data","event_spaces",f"{space}",f"EVENT_{space}_{tag}.json")), {f"{category}_event": info})
    
    # Add event picture
    scales = get_mod_config('img_scales'); w, h = scales[f"{category}_event"]
    picture = ImageFind(pjoin(path,"default"))
    if picture is None:
        picture = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_event")), find_default=None)
        assert (picture is not None), "The default event picture is not found!"
    if space == "SUPER":
        w, h = scales["super_event"]
        picture = ImageZoom(picture, w=w, h=h)
    elif category == 'country':
        picture = CreateCountryEventImage(picture)
    else:
        picture = ImageZoom(picture, w=w, h=h)
    ImageSave(picture, F(pjoin("gfx","event_pictures",f"EVENT_{space}_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","events",f"EVENT_{space}_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_EVENT_{space}_{tag}", "texturefile": pjoin("gfx","event_pictures",f"EVENT_{space}_{tag}.dds")}}})

def AddEventSpace_(space):
    event_space_path = F(pjoin("data","event_spaces",space)); CreateFolder(event_space_path)
    event_files = [file for file in ListFiles(event_space_path) if file.endswith('.json')]
    events = [LoadJson(pjoin(event_space_path,file)) for file in sorted(event_files, key=lambda x: int(Prefix(x).split('_')[-1]))]
    event_space = merge_dicts([{"add_namespace": space}] + events, d=True)
    SaveJson(event_space, F(pjoin("data","events",f"{space}.json")), indent=4)

def AddEventSpace(path, translate=True):
    '''
    Add a event space and all events inside it.
    Args:
        path: str. The path of the resource files of the event space. The resources should include a list of folders, each representing a event.
        translate: bool. Whether to translate the localisation of the event.
    Return:
        None
    '''
    space = path.strip('/').split('/')[-1].upper()
    for event in ListFolders(path):
        if not event.startswith('__'):
            AddEvent(pjoin(path, event), space=space, translate=translate)
    AddEventSpace_(space)


def InitSuperEvent():
    '''
    Add the super event feature to the mod.
    '''
    CreateFolder(F(pjoin("data", "event_spaces", "SUPER")))
    CreateFolder(F(pjoin("data", "interface", "super_events")))
    CreateFolder(F(pjoin("data", "common", "scripted_guis")))
    CreateFolder(F(pjoin("data", "common", "scripted_localisation")))
    SaveJson(LoadJson(F(pjoin("hoi4dev_settings", "configs", "super_event.json"))), F(pjoin("data","interface","super_events","super_event.json")), indent=4)
    SaveJson(LoadJson(F(pjoin("hoi4dev_settings", "configs", "super_event_gfx.json"))), F(pjoin("data","interface","super_events","super_event_gfx.json")), indent=4)
    SaveJson(LoadJson(F(pjoin("hoi4dev_settings", "configs", "super_event_gui.json"))), F(pjoin("data","common","scripted_guis","super_events_gui.json")), indent=4)
    SaveJson(LoadJson(F(pjoin("hoi4dev_settings", "configs", "super_event_localisation_name.json"))), F(pjoin("data","common","scripted_localisation","super_events_name.json")), indent=4)
    SaveJson(LoadJson(F(pjoin("hoi4dev_settings", "configs", "super_event_localisation_desc.json"))), F(pjoin("data","common","scripted_localisation","super_events_desc.json")), indent=4)
    SaveJson(LoadJson(F(pjoin("hoi4dev_settings", "configs", "super_event_localisation_mark.json"))), F(pjoin("data","common","scripted_localisation","super_events_mark.json")), indent=4)
    CreateFolder(F(pjoin("gfx","interface", "super_events")))
    CopyFile(F(pjoin("hoi4dev_settings", "imgs", "Super_Event_Close_Button.dds")), F(pjoin("gfx","interface", "super_events", "Super_Event_Close_Button.dds")))
    CopyFile(F(pjoin("hoi4dev_settings", "imgs", "Super_Event_Underlay.dds")), F(pjoin("gfx","interface", "super_events", "Super_Event_Underlay.dds")))
    CopyFile(F(pjoin("hoi4dev_settings", "imgs", "Super_Event_Window.dds")), F(pjoin("gfx","interface", "super_events", "Super_Event_Window.dds")))

def AddSuperEvent(path, translate=True):
    '''
    Add a super event to the mod. (You have to manually execute `AddEventSpace_("SUPER"); AddEventSpace_("SUPER_NEWS")` after adding super events)
    Args:
        path: str. The path of the resource files of the super event. The resources should include the super event image (optional), the super event definition and the localisation.
        translate: bool. Whether to translate the localisation of the country.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].split('-',1)[0]
    assert (tag.isdigit()), f"Event tag should be numeric, but got {tag}."
    tag = int(tag)
    info = LoadJson(pjoin(path,"info.json"))
    name = info.pop('name', None)
    effects = info.pop('effects', dict())
    news_effects = info.pop('news_effects', dict())
    o_effects = info.pop('o_effects', dict())

    # Add event localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"EVENT_SUPER_{tag}", translate=translate)
    
    # Initialize event definition (An empty event space folder is added if not exists)
    space_path = F(pjoin("data","event_spaces","SUPER")); CreateFolder(space_path)
    Edit(F(pjoin("data","event_spaces",f"SUPER",f"EVENT_SUPER_{tag}.json")), {
        "country_event": {
            "id": f"SUPER.{tag}",
            "title": f"EVENT_SUPER_{tag}_NAME",
            "desc": f"EVENT_SUPER_{tag}_DESC",
            "picture": f"GFX_EVENT_SUPER_{tag}",
            "is_triggered_only": True,
            "fire_only_once": True,
            "hidden": True,
            "immediate": {"hidden_effect": merge_dicts([effects, {
                "set_global_flag": f"PIHC_GLOBAL_FLAG_SUPEREVENT_{tag}_ON",
                "set_global_flag__D1": f"PIHC_GLOBAL_FLAG_SUPEREVENTS_VISIBLE"
            }], d=True)},
            "option": {
                "ai_chance": {
                    "factor": 100,
                },
                "mark_focus_tree_layout_dirty": True
            }
        }
    })
    news_path = F(pjoin("data","event_spaces","SUPER_NEWS")); CreateFolder(news_path)
    Edit(F(pjoin("data","event_spaces",f"SUPER_NEWS",f"EVENT_SUPER_NEWS_{tag}.json")), {
        'news_event': {
            "id": f"SUPER_NEWS.{tag}",
            "title": f"EVENT_SUPER_{tag}_NEWS_NAME",
            "desc": f"EVENT_SUPER_{tag}_NEWS_DESC",
            "picture": f"GFX_EVENT_SUPER_NEWS_{tag}",
            "is_triggered_only": True,
            "major": True,
            "immediate": {"hidden_effect": news_effects},
            "option": {
                "ai_chance": {
                    "factor": 100,
                },
                "trigger": {
                    "is_ai": True
                }
            },
            "option__D1": {
                "ai_chance": {
                    "factor": 100,
                },
                "trigger": {
                    "is_ai": False
                },
                "name": f"EVENT_SUPER_{tag}_NEWS_o",
                "hidden_effect": {
                    "set_global_flag": f"PIHC_GLOBAL_FLAG_SUPEREVENT_{tag}_HAPPENED",
                    "country_event": {
                        "id": f"SUPER.{tag}",
                    }
                }
            } | o_effects
        }
    })
    
    # Add event picture
    scales = get_mod_config('img_scales'); w, h = scales[f"super_event"]
    picture = ImageFind(pjoin(path,"default"))
    if picture is None:
        picture = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_event")))
        assert (picture is not None), "The default event picture is not found!"
    picture = ImageZoom(picture, w=w, h=h)
    ImageSave(picture, F(pjoin("gfx","event_pictures",f"EVENT_SUPER_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","events",f"EVENT_SUPER_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_EVENT_SUPER_{tag}", "texturefile": pjoin("gfx","event_pictures",f"EVENT_SUPER_{tag}.dds")}}})
    w_n, h_n = scales[f"news_event"]
    news_picture = ImageFind(pjoin(path,"news"))
    if news_picture is None:
        news_picture = picture.clone()
    news_picture = ImageZoom(news_picture, w=w_n, h=h_n)
    ImageSave(news_picture, F(pjoin("gfx","event_pictures",f"EVENT_SUPER_NEWS_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","events",f"EVENT_SUPER_NEWS_{tag}.json")), {'spriteTypes': {'spriteType': {"name": f"GFX_EVENT_SUPER_NEWS_{tag}", "texturefile": pjoin("gfx","event_pictures",f"EVENT_SUPER_NEWS_{tag}.dds")}}})

    # Add event gui
    # Notice that the order matters, so the file should be sorted after editing
    Edit(F(pjoin("data","interface","super_events","super_event.json")), {
        "$guiTypes": {
            "$containerWindowType": {
                "iconType": {
                    "name": f"sp_event_picture_{tag}",
                    "spriteType": f"GFX_EVENT_SUPER_{tag}",
                    "position": {"x":-w//2,"y":-h//2+10},
                    "orientation": "center"
                }
            }
        }
    }, d=True)
    data = LoadJson(F(pjoin("data","interface","super_events","super_event.json")))
    window = data['guiTypes']['containerWindowType']
    order_list_mapping = {
        'sp_event_text_underlay': 1,
        'sp_event_desc': 2,
        'sp_event_overlay': 3,
        'sp_event_name': 4,
        'sp_event_close_button': 5
    }
    data['guiTypes']['containerWindowType'] = {
        k:v for k, v in sorted(window.items(), key =
            lambda item:
                ( order_list_mapping[item[1]['name']]
                if (item[1]['name'] in order_list_mapping) else 0 )
                if isinstance(item[1], dict) and ('name' in item[1]) else -1
        )
    }
    SaveJson(data, F(pjoin("data","interface","super_events","super_event.json")), indent=4)
    
    # Add event scripted guis
    Edit(F(pjoin("data","common","scripted_guis","super_events_gui.json")), {
        "$scripted_gui": {
            "$sp_event_window": {
                "triggers": {
                    f"sp_event_picture_{tag}_visible": {
                        "has_global_flag": f"PIHC_GLOBAL_FLAG_SUPEREVENT_{tag}_ON"
                    }
                },
                "$effects": {
                    "$sp_event_close_button_click": {
                        "if": {
                            "limit": {
                                "has_global_flag": f"PIHC_GLOBAL_FLAG_SUPEREVENT_{tag}_ON"
                            },
                            "clr_global_flag": f"PIHC_GLOBAL_FLAG_SUPEREVENT_{tag}_ON"
                        }
                    }
                }
            }
        }
    }, d=True)
    
    # Add event scripted localisations (name, desc, mark)
    # Notice that the order matters, so the file should be sorted after editing
    for key in ['name', 'desc', 'mark']:
        Edit(F(pjoin("data","common","scripted_localisation",f"super_events_{key}.json")), {
            "$defined_text": {
                "text": {
                    "trigger": {
                        "has_global_flag": f"PIHC_GLOBAL_FLAG_SUPEREVENT_{tag}_ON"
                    },
                    "localization_key": f"EVENT_SUPER_{tag}_{key.upper()}"
                }
            }
        }, d=True)
        data = LoadJson(F(pjoin("data","common","scripted_localisation",f"super_events_{key}.json")))
        window = data['defined_text']
        data['defined_text'] = {
            k:v for k, v in sorted(window.items(), key = lambda item: -1 if (item[0]=='name') else (item[1]['localization_key']=="Error"))
        }
        SaveJson(data, F(pjoin("data","common","scripted_localisation",f"super_events_{key}.json")), indent=4)
