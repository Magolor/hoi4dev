# ===================================== #
# ==== CHAPTER 0: Create a New Mod ==== #
# ===================================== #

# %%
# Import hoi4dev
from hoi4dev import *
# Fix the random seed
import numpy as np
np.random.seed(42)

# %%
# Create our new mod from scratch. 
mod_name = "PIHC_dev"
version = "v0.2.2"
version_title = "Lokadhatu"
root = CreateMod(
    name = mod_name,
    version =  version,
    hoi4_version = "1.16.4",
    tags = ["Alternative History", "Gameplay", "Map", "Technologies", "Sound", "National Focuses", "Events", "Ideologies",],
    title = f"The Pony In The High Castle",
    copies = "resources/copies/",
    languages = ["zh", "en"],
    replace_paths = [
        "common/abilities",
        "common/ai_equipment",
        "common/ai_focuses",
        "common/ai_strategy",
        "common/ai_strategy_plans",
        "common/ai_templates",
        "common/autonomous_states",
        "common/bookmarks",
        "common/bop",
        "common/buildings",
        "common/characters",
        "common/countries",
        "common/country_leader",
        "common/continuous_focus",
        "common/country_tag_aliases",
        "common/country_tags",
        "common/decisions",
        "common/decisions/categories",
        "common/difficulty_settings",
        "common/focus_inlay_windows",
        "common/game_rules",
        "common/ideas",
        "common/ideologies",
        "common/modifiers",
        "common/dynamic_modifiers",
        "common/military_industrial_organization/organizations",
        "common/national_focus",
        "common/on_actions",
        "common/operations",
        "common/raids",
        "common/raids/categories",
        "common/resources",
        "common/scripted_diplomatic_actions",
        "common/scripted_effects",
        "common/scripted_guis",
        "common/scripted_localisation",
        "common/scripted_triggers",
        "common/special_projects",
        "common/special_projects/project_tags",
        "common/special_projects/projects",
        "common/special_projects/prototype_rewards",
        "common/special_projects/specialization",
        "common/technologies",
        "common/technology_tags",
        "common/technology_sharing",
        "common/unit_tags",
        "common/units",
        "common/unit_leader",
        "common/unit_medals",
        "common/units/codenames_operatives",
        "common/units/equipment",
        "common/units/equipment/upgrades",
        "common/units/names",
        "common/units/names_divisions",
        "common/units/names_railway_guns",
        "common/units/names_ships",
        "common/wargoals",
        "common/operations",
        "common/operation_tokens",
        "common/operation_phases",
        "common/peace_conference",
        "common/peace_conference/ai_peace",
        "common/peace_conference/categories",
        "common/peace_conference/cost_modifiers",
        "country_metadata",
        "events",
        "gfx/flags",
        "gfx/leaders",
        "gfx/loadingscreens",
        "gfx/event_pictures",
        "gfx/interface/equipmentdesigner/graphic_db",
        "history/countries",
        "history/general",
        "history/states",
        "history/units",
        "map",
        "map/strategicregions",
        "map/supplyareas",
        "map/terrain",
        "portraits",
        "tutorial",
    ]
)

# %%
# Remember to config the mod path.
set_config("CURRENT_MOD_PATH", root)

# %%
# Edit config
for file in EnumFiles("hoi4dev_settings", relpath="hoi4dev_settings"):
    if not ExistFile(pjoin(root, "hoi4dev_settings", file)):
        CopyFile(pjoin("hoi4dev_settings", file), pjoin(root, "hoi4dev_settings", file))
    else:
        if file.endswith(".json"):
            data = merge_dicts([LoadJson(pjoin(root, "hoi4dev_settings", file)), LoadJson(pjoin("hoi4dev_settings", file))])
            SaveJson(data, pjoin(root, "hoi4dev_settings", file), indent=4)
        else:
            CopyFile(pjoin("hoi4dev_settings", file), pjoin(root, "hoi4dev_settings", file), rm=True)


# %%
# First modify the configs manually if needed, then initialize the mod.
InitMod()

# %%
# Copy thumbnail and default images to the newly created mod.
thumbnail = ImageLoad(pjoin("hoi4dev_settings", "imgs", "thumbnail.png"))
thumbnail = ImageZoom(thumbnail, w=128, h=128)
ImageSave(thumbnail, F("thumbnail.png"))

# %%
# Add the term table
# SaveJson(LoadJson("resources/term_table.json"), F("hoi4dev_settings/term_table.json"))

# %%
# Edit mod config
set_mod_config("bookmark_date","1002.12.1")

# %%
# Add miscs localisation
for loc in ListFiles("resources/locs"):
    if loc.endswith(".txt"):
        loc_path = pjoin("resources", "locs", loc); loc_scope = loc.split(".")[0].upper()
        AddLocalisation(loc_path, scope=loc_scope, replace=True, translate=False)