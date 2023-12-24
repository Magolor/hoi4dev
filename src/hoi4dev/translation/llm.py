from ..utils import *
import openai
from seed import LLM

llm = None
def LLMTranslate(src, src_lang='zh', tgt_lang='en'):
    '''
    Translate a given text from source language to target language (using a large language model).
    Args:
        src: str. The source text to be translated.
        src_lang: str. The source language.
        tgt_lang: str. The target language.
    Return:
        str. The translated text.
    You can use the `term_table.json` to control the terms.
    '''
    global llm
    if llm is None:
        llm = LLM()
    prompt = f"Please translate the following text from {LANGUAGE_MAPPING[src_lang]['nl']} to {LANGUAGE_MAPPING[tgt_lang]['nl']}:\n"
    terms = list(LoadJson(F("hoi4dev_settings/term_table.json"))[f"{src_lang}-{tgt_lang}"].items())
    term_table_prompt = "Here are some terms that may be useful for reference:\n" + ("\n".join([f"{src}: {tgt}" for src, tgt in terms]))
    response = llm.q([{'role': 'user', 'content': prompt+src+'\n'+term_table_prompt}])
    if response['text'] is not None:
        return response['text'].strip()
    else:
        return ''