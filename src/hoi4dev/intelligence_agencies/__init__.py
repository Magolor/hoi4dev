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

def AddIntelAgency(path, translate=True):
    '''
    Add an intelligence agency to the mod.
    Args:
        path: str. The path of the resource files of the intelligence agency. The resources should include the intelligence agency icon, the intelligence agency definition and the localisation.
        translate: bool. Whether to translate the localisation of the intelligence agency.
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
    scales = get_mod_config('img_scales'); w, h = scales['intel_agency']
    icon = ImageFind(pjoin(path,"default"))
    if icon is None:
        icon = ImageFind(F(pjoin("hoi4dev_settings", "imgs", "defaults", "default_intel_agency")), find_default=False)
        assert (icon is not None), "The default intelligence agency icon is not found!"
    icon = CreateIntelAgencyImage(ImageZoom(icon, w=w, h=h))
    ImageSave(icon, F(pjoin("gfx","interface","intelligence_agencies",f"INTEL_AGENCY_{tag}")), format='dds')
    Edit(F(pjoin("data","interface","intelligence_agencies",f"INTEL_AGENCY_{tag}.json")), {'spriteTypes': {'spriteType': {
        "name": f"GFX_INTEL_AGENCY_{tag}",
        "texturefile": pjoin("gfx","interface","intelligence_agencies",f"INTEL_AGENCY_{tag}.dds"),
        "noOfFrames": 2,
    }}})
