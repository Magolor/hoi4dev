from .lm import LMTranslate
from .llm import LLMTranslate
from .manual import ManualTranslate

from copy import deepcopy

def PopulateLocs(locs, languages=["zh", "en", "ru"], translation=LLMTranslate):
    '''
    Filling the missing localisations with auto-translation.
    Args:
        locs: Dict. The localisation dictionary.
        languages: List[str]. The list of languages to be populated. The first language in the list will be used as the source language.
        translation: function. The translation function. `LMTranslate` or `LLMTranslate`. Default is `LLMTranslate`.
    Return:
        locs: Dict. The populated localisation dictionary.
    '''
    locs = deepcopy(locs)
    for key, values in locs.items():
        for language in languages:
            if (languages[0] in values) and (language not in values):
                locs[key][language] = translation(values[languages[0]], src_lang=languages[0], tgt_lang=language)
    return locs

from ..utils import *

def AddLocalisation(locs_file, scope="", translate=True, replace=False):
    '''
    Convert the localisation file to a `yml` file and add it to the mod.
    Args:
        locs_file: str. The path of the localisation file.
        scope: str. The scope of the localisation file.
        translate: bool. Whether to translate the localisation file.
        replace: str. Whether to put the localisation in the `replace` folder.
    Return:
        None
    '''
    locs = ReadTxtLocs(locs_file, scope=scope) if ExistFile(locs_file) else {}
    if translate:
        locs = PopulateLocs(locs, languages=get_mod_config('languages'))
    SaveLocs(locs, name=scope, path=F(pjoin("data","localisation")), replace=replace)
    return locs