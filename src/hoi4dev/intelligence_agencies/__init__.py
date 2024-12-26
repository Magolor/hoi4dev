from ..utils import *
from ..translation import AddLocalisation

def InitIntelAgencies():
    '''
    Initialize intelligence agencies.
    Args:
        None
    Return:
        None
    '''
    SaveJson({}, F(pjoin("data","common","intelligence_agencies","00_intelligence_agencies.json")))

def AddIntelAgency(path, translate=True, force=True):
    '''
    Add an intelligence agency to the mod.
    Args:
        path: str. The path of the resource files of the intelligence agency. The resources should include the intelligence agency icon, the intelligence agency definition and the localisation.
        translate: bool. Whether to translate the localisation of the intelligence agency.
        force: bool. Whether to force the overwriting of the existing cached images.
    Return:
        None
    '''
    tag = path.strip('/').split('/')[-1].upper()
    info = merge_dicts([{
        # 'names': [f"INTEL_AGENCY_{tag}"],
        'picture': f"GFX_INTEL_AGENCY_{tag}"
    },LoadJson(pjoin(path,"info.json"))])
    name = info.pop('name', None)
    
    # Add intelligence agency localisation
    AddLocalisation(pjoin(path,"locs.txt"), scope=f"INTEL_AGENCY_{tag}", translate=translate)
    
    # Initialize intelligence agency definition
    Edit(F(pjoin("data","common","intelligence_agencies",f"00_intelligence_agencies.json")), {'intelligence_agency': info}, d=True)
    
    # Add intelligence agency icons
    if (not force) and ExistFile(pjoin(path, ".cache", "doubled.dds")):
        doubled_icon = ImageLoad(pjoin(path, ".cache", "doubled.dds"))
    else:
        icon = hoi4dev_auto_image(
            path = path,
            resource_type = "intel_agency",
            scale = "intel_agency",
            force = force
        )
        doubled_icon = CreateIntelAgencyImage(icon)
        ImageSave(doubled_icon, F(pjoin(path, ".cache", "doubled.dds")), format='dds')
    ImageSave(doubled_icon, F(pjoin("gfx","interface","intelligence_agencies",f"INTEL_AGENCY_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","intelligence_agencies",f"INTEL_AGENCY_{tag}.json")), {'spriteTypes': {'spriteType': {
        "name": f"GFX_INTEL_AGENCY_{tag}",
        "texturefile": pjoin("gfx","interface","intelligence_agencies",f"INTEL_AGENCY_{tag}.dds"),
        "noOfFrames": 2,
    }}})
