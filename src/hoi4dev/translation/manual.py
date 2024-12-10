
def ManualTranslate(src, src_lang='zh', tgt_lang='en', B=128):
    '''
    Display the content to be translated and ask for manual translation.
    Args:
        src: str. The source text to be translated.
        src_lang: str. The source language.
        tgt_lang: str. The target language.
        B: int. The chunk size. The chunking will be soft, depending on the sentencing of the `src` text, so the actual chunk size may be larger than `B`.
    Return:
        str. The translated text.
    '''
    print("Source Language:", src_lang)
    print("Target Language:", tgt_lang)
    print(src)
    return eval('"'+input()+'"')