from ..utils import *

def get_ideologies():
    data = LoadJson(F(pjoin("data","common","ideologies","00_ideologies.json")))
    return {k: list(data['ideologies'][k]['types'].keys()) for k in data['ideologies']}