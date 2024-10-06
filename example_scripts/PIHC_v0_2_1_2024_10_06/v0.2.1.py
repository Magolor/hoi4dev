# %%
from pyheaven import *
args = HeavenArguments.from_parser([
    SwitchArgumentDescriptor("publish", short="p", help="Push the compiled mod to the repository."),
    SwitchArgumentDescriptor("zip", short="z", help="Zip the compiled mod."),
    SwitchArgumentDescriptor("keep-data", short="k", help="Keep the data folder after compiling."),
])
if args.publish:
    args.zip = True
    args.keep_data = False

# %%
from scripts.copy_technology_scripted_effect import create_copy_technology_scripted_effect
create_copy_technology_scripted_effect()
from scripts.add_winter_penalties import add_winter_penalties
add_winter_penalties()
from scripts.update_scripted_locs import update_scripted_locs
update_scripted_locs()
from scripts.compile_jokes import compile_all_jokes
compile_all_jokes()

# %%
from scripts.C00_create_a_new_mod import *

# %%
from scripts.C01_build_the_map import *

# %%
from scripts.C02_add_mirror_portal import *

# %%
from scripts.C03_add_gfxs import *

# %%
from scripts.C04_add_countries import *

# %%
from scripts.C05_add_characters import *

# %%
from scripts.C06_add_ideas import *

# %%
from scripts.C07_add_military import *

# %%
from scripts.C08_add_decisions import *

# %%
from scripts.C09_add_national_focuses import *

# %%
from scripts.C10_add_events import *

# %%
from scripts.C11_add_intel_agencies import *

# %%
from scripts.C12_add_achievements import *

# %%
from scripts.C13_add_inventory_items import *

# %%
from scripts.C14_add_state_lores import *

# %%
from hoi4dev import *
CompileMod()
if not args.keep_data:
    Delete(F("data"), rm=True)
    Delete(F("hoi4dev_settings"), rm=True)

# %%
from README_generator import *

# %%
mods_path = get_config("HOI4_MODS_PATH")
mods_copy_path = get_config("HOI4_MODS_COPY_PATH")
if mods_copy_path != mods_path:
    CopyFile(pjoin(mods_path,f"{mod_name}.mod"), pjoin(mods_copy_path,f"{mod_name}.mod"))

CopyFile("README.en.md", "README.md", rm=True)
CopyFile("README.md", F("README.md"))
CopyFile("README.en.md", F("README.en.md"))
CopyFile("README.zh.md", F("README.zh.md"))
CopyFile("README.steam.en.md", F("README.steam.en.md"))
CopyFile("README.steam.zh.md", F("README.steam.zh.md"))

if ExistFile("README.en.pdf"):
    CopyFile("README.en.pdf", F("README.en.pdf"))
if ExistFile("README.zh.pdf"):
    CopyFile("README.zh.pdf", F("README.zh.pdf"))

# %%
CopyFile(".gitignore", F(".gitignore"))
CopyFile(".gitattributes", F(".gitattributes"))
CopyFile("version.bash", F("version.bash"))
CopyFile("push_compiled.bash", F("push_compiled.bash"))
CopyFile("clear_git.bash", F("clear_git.bash"))
if args.publish:
    CMD(f"cd \"{F('')}\" && bash push_all.bash")


CMD(f"cd \"{F('')}\" && bash clear_git.bash")
if args.zip:
    small_version = open("version.bash").read().split('=')[-1].strip().strip('"')
    desktop = expanduser("~/Desktop")
    mod_name = "PIHC_dev"
    print("Zipping:", f"cd \"{F('')}..\" && zip -q -r \"{pjoin(desktop, small_version+'.zip')}\" \"./{mod_name}\" \"./{mod_name}.mod\"")
    CMD(f"cd \"{F('')}..\" && zip -q -r \"{pjoin(desktop, small_version+'.zip')}\" \"./{mod_name}\" \"./{mod_name}.mod\"")

# %%
print(SUCCESS("Done."))

# %%
