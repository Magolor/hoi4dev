from hoi4dev import *


PENALTIES = {
    100: (-0.75, -0.40, 70, 40, 20),
     90: (-0.65, -0.35, 60, 30, 10),
     80: (-0.50, -0.30, 50, 20,  0),
     70: (-0.40, -0.25, 40, 10, -1),
     60: (-0.35, -0.22, 30,  0, -1),
     50: (-0.30, -0.18, 20, -1, -1),
     40: (-0.25, -0.15, 10, -1, -1),
     30: (-0.20, -0.12,  0, -1, -1),
     20: (-0.15, -0.08, -1, -1, -1),
     10: (-0.12, -0.06, -1, -1, -1),
      0: (-0.10, -0.05, -1, -1, -1),
     -1: (-0.00, -0.00, -1, -1, -1),
}
def add_winter_penalties():
    source = "ALL_WINTER_PENALTY"
    ideas_path = "./resources/ideas/"
    scripted_effects_path = "./resources/copies/data/common/scripted_effects/"
    effect = dict(); revoke_effect = dict()
    for threat, (monthly_population, stability_factor, subsidy, normal, burn) in PENALTIES.items():
        if threat != -1:
            tag = f"{source}_{threat:03d}"
            CopyFolder(pjoin(ideas_path, source), pjoin(ideas_path, tag), rm=True)
            data = LoadJson(pjoin(ideas_path, tag, "info.json"))
            data['modifier'] = {
                "monthly_population": monthly_population,
                "stability_factor": stability_factor
            }
            SaveJson(data, pjoin(ideas_path, tag, "info.json"), indent=4)

            if_data = {
                "limit": {
                    f"threat > 0.{threat-1}": None,
                },
                "if": {
                    "limit": {
                        "has_idea": "IDEA_ERA_COLD_4_SELF"
                    },
                    "add_ideas": f"IDEA_{source}_{threat:03d}"
                }
            }
            if threat == 0:
                del if_data["limit"]
            if subsidy != -1:
                if_data[find_dup("else_if", if_data)] = {
                    "limit": {
                        "has_idea": "IDEA_ERA_COLD_3_SUBSIDY"
                    },
                    "add_ideas": f"IDEA_{source}_{subsidy:03d}"
                }
            if normal != -1:
                if_data[find_dup("else_if", if_data)] = {
                    "limit": {
                        "OR": {
                            "has_idea": "IDEA_ERA_COLD_1_COAL",
                            "has_idea__D1": "IDEA_ERA_COLD_2_WOOD",
                        }
                    },
                    "add_ideas": f"IDEA_{source}_{normal:03d}"
                }
            if burn != -1:
                if_data[find_dup("else", if_data)] = {
                    "limit": {
                        "has_idea": "IDEA_ERA_COLD_5_BURN"
                    },
                    "add_ideas": f"IDEA_{source}_{burn:03d}"
                }
            if ("if" not in effect):
                effect["if"] = if_data
            elif ("limit" in if_data):
                effect[find_dup("else_if", effect)] = if_data
            else:
                effect["else"] = if_data

            revoke_effect[find_dup("if", revoke_effect)] = {
                "limit": {
                    "has_idea": f"IDEA_{source}_{threat:03d}"
                },
                "remove_ideas": f"IDEA_{source}_{threat:03d}"
            }
    
    data = {"APPLY_WINTER_PENALTY": effect, "REVOKE_WINTER_PENALTY": revoke_effect}
    SaveJson(data, pjoin(scripted_effects_path, "PIHC_WINTER_PENALTY.json"), indent=4)