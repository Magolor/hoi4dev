from ..utils import *

try:
    import nltk
    from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
except ImportError as e:
    pass

M2M100 = [None, None]
CKPT_PATH = pjoin(ROOT_PATH, "ckpt")
DEFAULT_CKPT = "facebook/m2m100_418M"
def initialize_translation_model(force=False):
    global M2M100
    if (not force) and ExistFolder(pjoin(CKPT_PATH, DEFAULT_CKPT)):
        tokenizer = M2M100Tokenizer.from_pretrained(pjoin(CKPT_PATH, DEFAULT_CKPT), local_files_only=True)
        model = M2M100ForConditionalGeneration.from_pretrained(pjoin(CKPT_PATH, DEFAULT_CKPT), local_files_only=True)
    else:
        CreateFolder(pjoin(CKPT_PATH, DEFAULT_CKPT))
        tokenizer = M2M100Tokenizer.from_pretrained(DEFAULT_CKPT); tokenizer.save_pretrained(pjoin(CKPT_PATH, DEFAULT_CKPT))
        model = M2M100ForConditionalGeneration.from_pretrained(DEFAULT_CKPT); model.save_pretrained(pjoin(CKPT_PATH, DEFAULT_CKPT))
    try:
        nltk.sent_tokenize("Hearts of Iron IV Modding is fun! Let's enjoy it!", language='english')
    except LookupError as e:
        nltk.download('punkt')
    M2M100 = [model, tokenizer]

def sentencing(src, src_lang='zh'):
    try:
        return nltk.sent_tokenize(src, language=LANGUAGE_MAPPING[src_lang]['nltk'])
    except LookupError as e:
        if src_lang == 'zh':
            return re.split('[。？！\n]', src)

def LMTranslate(src, src_lang='zh', tgt_lang='en', B=128):
    '''
    Translate a given text from source language to target language (using a machine learning translation model).
    Args:
        src: str. The source text to be translated.
        src_lang: str. The source language.
        tgt_lang: str. The target language.
        B: int. The chunk size. The chunking will be soft, depending on the sentencing of the `src` text, so the actual chunk size may be larger than `B`.
    Return:
        str. The translated text.
    '''
    if (M2M100[0] is None) or (M2M100[1] is None):
        initialize_translation_model()
    model, tokenizer = M2M100
    tokenizer.src_lang = src_lang
    
    sentences = sentencing(src, src_lang=src_lang)
    translated_segments = []
    current_segment = ""
    for sentence in sentences:
        if len(current_segment) + len(sentence) >= B:
            encoded = tokenizer(current_segment+sentence, return_tensors='pt')
            generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang))
            translated_segments.append(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0])
            current_segment = ""
        else:
            current_segment += sentence
    return ' '.join(translated_segments)