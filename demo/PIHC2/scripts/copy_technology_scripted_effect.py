from hoi4dev import *

def create_copy_technology_scripted_effect():
    banned = set([
        "TECHNOLOGY_TANK_TITAN_WINDIGO",
        "TECHNOLOGY_NSB_TANK_TITAN_WINDIGO",
        "TECHNOLOGY_TANK_TITAN_TIREK",
        "TECHNOLOGY_NSB_TANK_TITAN_TIREK"
    ])
    techs = ["TECHNOLOGY_"+x for x in ListFolders("resources/technologies", ordered=True) if x not in banned]
    info = {
        "STEAL_ALL_TECHNOLOGY": {
            "if": {
                "limit": {
                    "has_variable": "PREV.VAR_STEAL_TECHNOLOGY_SOURCE_COUNTRY_SCOPE"
                },
                # tech_steal
            }
        },
        "STEAL_RANDOM_TECHNOLOGY": {
            "if": {
                "limit": {
                    "has_variable": "PREV.VAR_STEAL_TECHNOLOGY_SOURCE_COUNTRY_SCOPE"
                },
                "random_list": {
                    "seed": "random",
                    # tech_steal
                }
            }
        }
    }
    for bonus in [30, 50, 100, 200]:
        info = info | {
            f"STEAL_RANDOM_TECHNOLOGY_BONUS_{bonus}": {
                "if": {
                    "limit": {
                        "has_variable": "PREV.VAR_STEAL_TECHNOLOGY_SOURCE_COUNTRY_SCOPE"
                    },
                    "random_list": {
                        "seed": "random",
                        # tech_steal
                        "1": {
                            # do nothing
                        }
                    }
                }
            }
        }
    for tech in techs:
        tech_steal = {
            "if": {
                "limit": {
                    "var:PREV.VAR_STEAL_TECHNOLOGY_SOURCE_COUNTRY_SCOPE": {
                        "has_tech": tech
                    },
                    "NOT": {
                        "PREV": {
                            "has_tech": tech
                        }
                    }
                },
                "PREV": {
                    "set_technology": {
                        tech: 1
                    }
                }
            }
        }
        info["STEAL_ALL_TECHNOLOGY"]["if"][find_dup("if",info["STEAL_ALL_TECHNOLOGY"]["if"])] = tech_steal["if"]
        tech_steal_modifier = {
            "modifier": {
                "factor": 0,
                "OR": {
                    "NOT": {
                        "var:PREV.VAR_STEAL_TECHNOLOGY_SOURCE_COUNTRY_SCOPE": {
                            "has_tech": tech
                        }
                    },
                    "PREV": {
                        "has_tech": tech
                    }
                }
            },
            "PREV": {
                "set_technology": {
                    tech: 1
                }
            }
        }
        info["STEAL_RANDOM_TECHNOLOGY"]["if"]["random_list"][find_dup("1",info["STEAL_RANDOM_TECHNOLOGY"]["if"]["random_list"])] = tech_steal_modifier
        for bonus in [30, 50, 100, 200]:
            tech_steal_bonus_modifier = {
                "modifier": {
                    "factor": 0,
                    "OR": {
                        "NOT": {
                            "var:PREV.VAR_STEAL_TECHNOLOGY_SOURCE_COUNTRY_SCOPE": {
                                "has_tech": tech
                            }
                        },
                        "PREV": {
                            "has_tech": tech
                        }
                    }
                },
                "PREV": {
                    "add_tech_bonus": {
                        "technology": tech,
                        "bonus": bonus/100.0,
                        "name": "PIHC_STEALED_TECHNOLOGY"
                    }
                }
            }
            info[f"STEAL_RANDOM_TECHNOLOGY_BONUS_{bonus}"]["if"]["random_list"][find_dup("1",info[f"STEAL_RANDOM_TECHNOLOGY_BONUS_{bonus}"]["if"]["random_list"])] = tech_steal_bonus_modifier
    SaveJson(info, "resources/copies/data/common/scripted_effects/PIHC_STEAL_TECHNOLOGY.json", indent=4)

if __name__=="__main__":
    create_copy_technology_scripted_effect()