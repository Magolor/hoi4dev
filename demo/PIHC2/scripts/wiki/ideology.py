
from hoi4dev import *


ideologies = {
    "democratic": "liberalism",
    "despotic": "despotism",
    "harmonicism": "harmonism",
    "equatism": "equatism",
    "fascism": "nationalism",
    "peacism": "pacifism",
    "corporation": "commercialism",
    "transcendence": "transcendence",
    "anarchy": "chaos"
}

language = "zh"

wiki_text = ""
for key, ideology in ideologies.items():
    file = pjoin(f"./resources/locs/ideologies_{ideology}.txt")
    data = ReadTxtLocs(file)
    
    wiki_text += f"== '''{data[key][language]} ({data[key]['en']})''' ==\n\n"
    tooltip = data[key+'_wiki_tooltip'][language].replace('\n','\n\n')
    wiki_text += f"{tooltip}\n"
    
    sub_ideologies_list = [k for k in data.keys() if k.startswith(key + "_") and k+'_desc' in data]
    for sub_ideology in sub_ideologies_list:
        wiki_text += f"* {data[sub_ideology][language]} ({data[sub_ideology]['en']})\n"
    wiki_text += "\n\n\n"
    
    for sub_ideology in sub_ideologies_list:
        wiki_text += f"=== '''{data[sub_ideology][language]} ({data[sub_ideology]['en']})''' ===\n"
        tooltip = data[sub_ideology+'_desc'][language].replace('\n','\n\n')
        if language == "zh":
            tooltip = tooltip.split('：\n',1)[-1]
        wiki_text += f"{tooltip}\n\n\n"

with open(f"./scripts/wiki/wiki_ideologies_{language}.txt", "w", encoding="utf-8") as f:
    f.write(wiki_text)

wiki_text = ""
for key, ideology in ideologies.items():
    file = pjoin(f"./resources/locs/ideologies_{ideology}.txt")
    data = ReadTxtLocs(file)
    
    wiki_text += f"== '''{data[key]['en']}''' ==\n\n"
    tooltip = data[key+'_wiki_tooltip']['en'].replace('\n','\n\n')
    wiki_text += f"{tooltip}\n"
    
    sub_ideologies_list = [k for k in data.keys() if k.startswith(key + "_") and k+'_desc' in data]
    for sub_ideology in sub_ideologies_list:
        wiki_text += f"* {data[sub_ideology]['en']}\n"
    wiki_text += "\n\n\n"
    
    for sub_ideology in sub_ideologies_list:
        wiki_text += f"=== '''{data[sub_ideology]['en']}''' ===\n"
        tooltip = data[sub_ideology+'_desc']['en'].replace('\n','\n\n')
        tooltip = tooltip.split(':\n',1)[-1]
        wiki_text += f"{tooltip}\n\n\n"

with open(f"./scripts/wiki/wiki_ideologies_en.txt", "w", encoding="utf-8") as f:
    f.write(wiki_text)
