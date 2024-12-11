from hoi4dev import *
import numpy as np

TEMPLATE = {
    "every_possible_country": {
        "limit": {
            "is_pony_country": True,
            "is_dynamic_country": False
        },
        "if": {
            "limit": {
                "NOT": {
                    "OR": {
                        
                    }
                }
            },
            "random_list": {
                "seed": "random",
                "1": {
                    "generate_character": {
                        "token_base": "CHARACTER_GENERIC_RANDOM_<TOKEN>",
                        "advisor": {
                            "allowed": {
                                "always": True
                            }
                        },
                        "gender": "male"
                    }
                },
                "5": {
                    "generate_character": {
                        "token_base": "CHARACTER_GENERIC_RANDOM_<TOKEN>_FEMALE",
                        "advisor": {
                            "allowed": {
                                "always": True
                            }
                        },
                        "gender": "female"
                    }

                }
            }
        }
    }
}

def add_random_characters():
    data = LoadJson("./resources/random_advisors.json")
    pihc_generic_advisors = dict()
    for token, traits, advisor_data in data:
        template = deepcopy(TEMPLATE)
        tag = f"{token}_{'_'.join(sorted(traits))}"
        for trait in traits:
            template["every_possible_country"]["if"]["limit"]["NOT"]["OR"] = merge_dicts([
                template["every_possible_country"]["if"]["limit"]["NOT"]["OR"],
                {
                    "has_allowed_idea_with_traits": {
                        "characters": True,
                        "idea": trait
                    }
                }
            ], d=True)
        template["every_possible_country"]["if"]["random_list"]["1"]["generate_character"]["token_base"] = \
        template["every_possible_country"]["if"]["random_list"]["1"]["generate_character"]["token_base"].replace("<TOKEN>", tag)
        template["every_possible_country"]["if"]["random_list"]["1"]["generate_character"]["advisor"] |= advisor_data | {"traits": traits}
        
        template["every_possible_country"]["if"]["random_list"]["5"]["generate_character"]["token_base"] = \
        template["every_possible_country"]["if"]["random_list"]["5"]["generate_character"]["token_base"].replace("<TOKEN>", tag)
        template["every_possible_country"]["if"]["random_list"]["5"]["generate_character"]["advisor"] |= advisor_data | {"traits": traits}
        pihc_generic_advisors = merge_dicts([pihc_generic_advisors, template], d=True)
    SaveJson(pihc_generic_advisors, "./resources/copies/data/history/general/zz_pihc_advisors.json", indent=4)
    
    np.random.seed(42)
    data = LoadJson("./resources/random_corps_commanders.json")
    for tag, count in data.items():
        if count > 0:
            corp_commanders = dict()
            for i in range(count):
                quality = int(np.random.choice([7]*10 + [8]*8 + [9]*5 + [10]*2 + [12]*2 + [16]*1))
                generate_character = {
                    "generate_character": {
                        "token_base": f"CHARACTER_GENERIC_RANDOM_CORPS_COMMANDER_{tag}_{i:03d}"
                    } | GetRandomCorpsCommander(quality=quality)
                }
                male_character = deepcopy(generate_character)
                male_character['generate_character']['gender'] = "male"
                female_character = deepcopy(generate_character)
                female_character['generate_character']['gender'] = "female"
                corp_commanders = merge_dicts([corp_commanders, {
                    tag: {
                        "random_list": {
                            "seed": "random",
                            "1": male_character,
                            "5": female_character
                        }
                    }
                }], d=True)
            SaveJson(corp_commanders, f"./resources/copies/data/history/general/{tag}_pihc_corp_commanders.json", indent=4)
