from pyheaven import *

if __name__=="__main__":
    args = HeavenArguments.from_parser([
        StrArgumentDescriptor("mod",        short="m",                          help="The name of your mod.",),
    ])