from ..utils import *
import openai
from seed import LLM

llm = None
def LLMTranslate(src, src_lang='zh', tgt_lang='en', term_table={}):
    '''
    Translate a given text from source language to target language (using a large language model).
    Args:
        src: str. The source text to be translated.
        src_lang: str. The source language.
        tgt_lang: str. The target language.
        term_table: dict. The term table used for translation.
    Return:
        str. The translated text.
    '''
    global llm
    if llm is None:
        llm = LLM()
    prompt = f"Please translate the following text from {LANGUAGE_MAPPING[src_lang]['nl']} to {LANGUAGE_MAPPING[tgt_lang]['nl']}:\n"
    response = llm.q([{'role': 'user', 'content': prompt+src}])
    if response['text'] is not None:
        return response['text'].strip()
    else:
        return ''