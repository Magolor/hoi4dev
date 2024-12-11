from pyheaven import *

def update_scripted_locs():
    CMD("cd ./resources/locs/ && python custom_cost_locs_gen.py && python C02_popularity_gen.py")