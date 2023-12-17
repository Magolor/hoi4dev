from ..utils import *

def get_ideologies():
    data = LoadJson(F(pjoin("data","common","ideologies","00_ideologies.json")))
    return {k: data['ideologies'][k]['types'] for k in data['ideologies']}