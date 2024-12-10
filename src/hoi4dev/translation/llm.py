from ..utils import *
try:
    from seed import LLM
except ImportError as e:
    pass

import re
def clean_text_for_contain(text):
    return re.sub(r'[^\w\s]', '', re.sub(r'\s', '', text), flags=re.UNICODE).lower().strip()

def contain(text, pattern):
    return clean_text_for_contain(pattern) in clean_text_for_contain(text)

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
    term_table = LoadJson(F(pjoin("hoi4dev_settings", "configs", "term_table.json")))
    terms = list(term_table[f"{src_lang}-{tgt_lang}"].items()) if f"{src_lang}-{tgt_lang}" in term_table else list()
    useful_terms = [f"{s}: {t}" for s, t in terms if contain(src, s)]
    term_table_prompt = "Here are some terms that may be useful for reference:\n" + ("\n".join(useful_terms))
    final_prompt = prompt+src+('\n'+term_table_prompt if len(useful_terms) else '')
    print(final_prompt)
    response = llm.q([{'role': 'user', 'content': final_prompt}])
    if response['text'] is not None:
        return response['text'].strip()
    else:
        return ''
# %%
