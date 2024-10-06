from hoi4dev import *

def gen_central_equestria_core_decisions():
    category_path = "./resources/decisions/CENTRAL_EQUESTRIA/"
    for folder in ListFolders(category_path):
        Delete(pjoin(category_path, folder), rm=True)
        
    names = LoadJson("./resources/strat_region_names.json")
    REGIONS = {
        i: (75, 3, 120, dict())
        for i in list(range(9, 57))+[231]
    }

    for s, (pp, civ, days, complement) in REGIONS.items():
        name = names[str(s)]
        info = {
            "name": f"Core {name['english']}",
            "priority": 100,

            "days_remove": days,
            "visible": {
                "ROOT": {
                    "any_owned_state": {
                        "region": s,
                        "has_state_flag": "PIHC_STATE_FLAG_IS_CENTRAL_EQUESTRIA",
                        "is_fully_controlled_by": "ROOT",
                        "NOT": {
                            "is_core_of": "ROOT"
                        }
                    },
                    "all_state": {
                        "OR": {
                            "NOT": {
                                "AND": {
                                    "region": s,
                                    "has_state_flag": "PIHC_STATE_FLAG_IS_CENTRAL_EQUESTRIA"
                                }
                            },
                            "AND": {
                                "is_owned_by": "ROOT",
                                "is_fully_controlled_by": "ROOT"
                            }
                        }
                    }
                }
            },
            "available": {
                f"num_of_civilian_factories_available_for_projects > {civ-1}": None,
                "hidden_trigger": {
                    f"has_political_power > {pp-1}": None
                }
            },
            "highlight_states": {
                "highlight_states_trigger": {
                    "region": s,
                    "has_state_flag": "PIHC_STATE_FLAG_IS_CENTRAL_EQUESTRIA",
                    "is_owned_by": "ROOT",
                    "is_fully_controlled_by": "ROOT",
                    "NOT": {
                        "is_core_of": "ROOT"
                    }
                }
            },
            "custom_cost_trigger": {
                f"num_of_civilian_factories_available_for_projects > {civ-1}": None,
                f"has_political_power > {pp-1}": None
            },
            "custom_cost_text": f"CUSTOM_COST_CIV_FACTORY_{civ}_PP_{pp}",
            "modifier": {
                "civilian_factory_use": civ
            },
            "ai_hint_pp_cost": pp,
            "complete_effect": {
                "hidden_effect": {
                    "add_political_power": -pp
                }
            },
            "remove_effect": {
                "ROOT": {
                    "every_owned_state": {
                        "limit": {
                            "region": s,
                            "is_fully_controlled_by": "ROOT",
                            "has_state_flag": "PIHC_STATE_FLAG_IS_CENTRAL_EQUESTRIA",
                            "NOT": {
                                "is_core_of": "ROOT"
                            }
                        },
                        "add_core_of": "ROOT"
                    }
                }
            },
            "ai_will_do": {
                "base": 100
            }
        }
        info = merge_dicts([info, complement], d=True)
        path = pjoin(category_path, f"CENTRAL_EQUESTRIA_CORE_{s}_{name['english'].upper().replace(' ','_')}")
        CreateFolder(path)
        SaveJson(info, pjoin(path, "info.json"), indent=4)
        with open(pjoin(path, "locs.txt"), "w", encoding='utf-8', errors='ignore') as f:
            f.write(f"[en.@]\nIntegrate §Y{name['english']}§! Area\n[zh.@]\n整合§Y{name['chinese']}§!地区\n\n[en.@desc]\nIntegrate §Y{name['english']}§! Area\n[zh.@desc]\n整合§Y{name['chinese']}§!地区\n")
        CopyFile(pjoin(category_path, "default.png"), pjoin(path, "default.png"))

if __name__=="__main__":
    gen_central_equestria_core_decisions()