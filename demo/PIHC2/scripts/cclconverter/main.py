from hoi4dev import *

if __name__=="__main__":
    args = HeavenArguments.from_parser([
        StrArgumentDescriptor('src'),
        StrArgumentDescriptor('tgt')
    ])
    CCLConvert(args.src, args.tgt)