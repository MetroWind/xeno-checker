#!/usr/bin/env python

import sys, os

def sanitizeName(name: str) -> str:
    Camal = ''.join(seg.capitalize() for seg in name.strip().split())
    return Camal.replace("'", "").replace('"', '')

def escape(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"')

def main():
    import argparse

    Parser = argparse.ArgumentParser(description='Process some integers.')
    Parser.add_argument('TypeName', metavar='TYPE',
                        help='Name of the type')

    Args = Parser.parse_args()

    Symbols = []
    for Line in sys.stdin:
        Str = Line.strip()
        Symbol = sanitizeName(Line)
        Symbols.append((Str, Symbol))

    print("class {}(enum.Enum):".format(Args.TypeName))
    for Str, Symbol in Symbols:
        print("    {} = enum.auto()".format(Symbol))

    print("\n    def __str__(self):")
    FirstLine = True
    for Str, Symbol in Symbols:
        print("        if self == {}.{}:".format(Args.TypeName, Symbol))
        print("            return \"{}\"".format(escape(Str)))

    print("\n    @classmethod")
    print("    def fromStr(cls, s):")
    for Str, Symbol in Symbols:
        print('        if s == "{}":'.format(escape(Str)))
        print('            return {}.{}'.format(Args.TypeName, Symbol))

if __name__ == "__main__":
    main()
