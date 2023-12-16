from .lm import LMTranslate
from .llm import LLMTranslate

from copy import deepcopy

def PopulateLocs(locs, languages=["zh", "en", "ru"], translation=LLMTranslate):
    '''
    Filling the missing localisations with auto-translation.
    Args:
        locs: dict. The localisation dictionary.
        languages: List[str]. The list of languages to be populated. The first language in the list will be used as the source language.
        translation: function. The translation function. `LMTranslate` or `LLMTranslate`. Default is `LLMTranslate`.
    Return:
        locs: dict. The populated localisation dictionary.
    '''
    locs = deepcopy(locs)
    for key, values in locs.items():
        for language in languages:
            if (languages[0] in values) and (language not in values):
                locs[key][language] = translation(values[languages[0]], src_lang=languages[0], tgt_lang=language)
    return locs