from hoi4dev import *
from copy import deepcopy

JOKES_PATH = "./resources/events/JOKES/"
JOKES_ACHIEVEMENT_PATH = "./resources/achievements/PIHC_2UN_ALL_JOKER/"

SINGLE_JOKE = {
    "immediate": {
        "hidden_effect": {
            
        }
    },
    "options": [
        {
            "ai_chance": {
                "factor": 100
            }
        },
        {
            "ai_chance": {
                "factor": 0
            },
            "hidden_effect": {
                "country_event": {
                    "id": "JOKES.9999"
                }
            }
        },
        {
            "ai_chance": {
                "factor": 0
            }
        },
        {
            "ai_chance": {
                "factor": 0
            }
        }
    ],
    "is_triggered_only": True
}
JOKES_COLLECTION = {
    "immediate": {
        "hidden_effect": {
            "random_list": {
                
            }
        }
    },
    "options": [
        {
            "ai_chance": {
                "factor": 100
            }
        }
    ],
    "hidden": True,
    "is_triggered_only": True
}


def compile_all_jokes():
    all_joke_events = [f for f in ListFiles(pjoin(JOKES_PATH, "__txts__"), ordered=True) if f.endswith(".txt")]
    for i, joke in enumerate(all_joke_events, 1):
        joke_path = pjoin(JOKES_PATH, joke.split('.')[0])
        ClearFolder(joke_path, rm=True)
    
        joke_data = deepcopy(SINGLE_JOKE)
        joke_data["immediate"]["hidden_effect"].update({
            "if": {
                "limit": {
                    "NOT": {
                        "has_global_flag": f"PIHC_GLOBAL_FLAG_JOKE_{i:03d}_SEEN"
                    }
                },
                "add_to_variable": {
                    "var": "global.VAR_PIHC_JOKE_COUNTER",
                    "value": 1
                },
                "set_global_flag": f"PIHC_GLOBAL_FLAG_JOKE_{i:03d}_SEEN"
            }
        })
        joke_data["options"][2].update({"country_event": {"id": f"JOKES.{i+1}"}})
        joke_data["options"][3].update({"country_event": {"id": f"JOKES.{i-1}"}})
        locs = ReadTxt(pjoin(JOKES_PATH, "__txts__", joke))
        button_locs = [
            {
                "zh": "不看了",
                "en": "I’m Done"
            },
            {
                "zh": "随机笑话",
                "en": "Random Joke"
            },
            {
                "zh": "下一个笑话",
                "en": "Next Joke"
            },
            {
                "zh": "上一个笑话",
                "en": "Previous Joke"
            }
        ]
        if i == 1:
            joke_data['options'].pop(3)
            button_locs.pop(3)
        if i == len(all_joke_events):
            joke_data['options'].pop(2)
            button_locs.pop(2)
        with open(pjoin(joke_path, "locs.txt"), "w", encoding='utf-8') as f:
            f.write(locs + "\n")
            for j, button in enumerate(button_locs):
                f.write(f"[zh.@o{j}]\n{button['zh']}\n[en.@o{j}]\n{button['en']}\n")
        SaveJson(joke_data, pjoin(joke_path, f"info.json"), indent=4)

    compile_joke_path = pjoin(JOKES_PATH, "9999-隐藏事件：随机笑话")
    ClearFolder(compile_joke_path, rm=True)
    collection_data = deepcopy(JOKES_COLLECTION)
    random_jokes = collection_data["immediate"]["hidden_effect"]["random_list"]
    for i, joke in enumerate(all_joke_events, 1):
        random_jokes[find_dup("1", random_jokes)] = {
            "modifier": {
                "factor": 8,
                "NOT": {
                    "has_global_flag": f"PIHC_GLOBAL_FLAG_JOKE_{i:03d}_SEEN"
                }
            },
            "country_event": f"JOKES.{i}"
        }
    SaveJson(collection_data, pjoin(compile_joke_path, "info.json"), indent=4)
    with open(pjoin(compile_joke_path, "locs.txt"), "w", encoding='utf-8') as f:
        f.write("[zh.@]\n隐藏事件：随机笑话\n[en.@]\nHidden Event: Random joke\n[zh.@desc]\n隐藏事件：随机笑话\n[en.@desc]\nHidden Event: Random joke\n[zh.@o0]\n好吧\n[en.@o0]\nOkay\n")

    JOKE_COUNT = len(all_joke_events)
    achievement_data = LoadJson(pjoin(JOKES_ACHIEVEMENT_PATH, "info.json"))
    achievement_data["happened"]["hidden_trigger"]["check_variable"]["value"] = JOKE_COUNT
    SaveJson(achievement_data, pjoin(JOKES_ACHIEVEMENT_PATH, "info.json"), indent=4)
