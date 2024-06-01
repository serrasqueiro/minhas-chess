# mychess  (c)20243  Henrique Moreira

""" Interaction with chess.com
"""

# pylint: disable=missing-function-docstring

import os.path
#import json

IO_ENCODING = "ISO-8859-1"

BASE_DNAME = os.path.realpath(os.path.dirname(__file__))

JSON_IO = "chessfun.json"
COMT_IN = "comentarios.tsv"


def main():
    if runner() is None:
        print("""Usage:
{__file__}
""")

def runner(debug=0):
    return script(os.path.join(BASE_DNAME), debug)

def script(bdir:str, debug=0):
    param = [
        os.path.join(bdir, JSON_IO),
        os.path.join(bdir, COMT_IN),
    ]
    opts = {}
    what = "D"
    msg = do_this(what, param, opts, debug)
    if msg:
        print("Error:", msg)
    return 0

def do_this(what, param, opts=None, debug=0):
    res = []
    opts = {} if opts is None else opts
    assert isinstance(opts, dict), "Bad options"
    assert param, "Nada?"
    jio_name, comm_name = param
    print("# Reading:", comm_name, "; io:", jio_name)
    with open(comm_name, "r", encoding=IO_ENCODING) as fdcom:
        comms = [ala.rstrip() for ala in fdcom.readlines() if valid_tsv_line(ala)]
    for item in comms:
        spl = item.split("\t")
        g_id = str(int(spl[0]))
        print(desample(g_id), spl[1:])
    return res

def desample(astr):
    # https://www.chess.com/analysis/game/live/110970067119?tab=review
    res = f"https://www.chess.com/analysis/game/live/{astr}?tab=review"
    return res

def valid_tsv_line(astr):
    last = astr[-1]
    #print(":::", astr)
    assert last == "\n", f"Bad line (last = {ord(last)}d): {[astr]}"
    astr = astr[:-1]
    check = astr.rstrip(" ") == astr
    assert check, f"Tailing blanks? {astr}"
    if astr.startswith("#"):
        return False
    spl = astr.split("\t")
    assert len(spl) == 4, f"Wrong tabs: {[astr]}"
    return True

# Main script
if __name__ == "__main__":
    main()
