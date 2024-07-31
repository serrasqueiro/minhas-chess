# mychess  (c)20243  Henrique Moreira

""" Interaction with chess.com
"""

## 	Creates chessfun.json if file does not yet exist
##

# pylint: disable=missing-function-docstring

from sys import argv
import os.path
import json

DEBUG = 1
IO_ENCODING = "ISO-8859-1"

BASE_DNAME = os.path.realpath(os.path.dirname(__file__))

JSON_IO = "chessfun.json"
COMT_IN = "comentarios.tsv"
LANCES_IN = "lances.tsv"

MEMBERS_LIST = (
    {
        "UserName": "hclmoreira",
    },
)

RAW_COMMENTS_SKEL = {
    "AnId": 0,
    "Id": None,
    "IdSys": None,
    "ShortComment": "",
    "SysObs": "",
}

J_LIST = {
    "MembersList": MEMBERS_LIST,
    "RawComments": [RAW_COMMENTS_SKEL],
}


def main():
    if runner(argv[1:]) is None:
        print(f"""Usage:
{__file__}

Reads {COMT_IN} (comments), and outputs: {JSON_IO}

Note {JSON_IO} is not in 'git'; it is only created if file does not exist yet.
""")

def runner(param, debug=0):
    if param:
        return None
    res = script(os.path.join(BASE_DNAME), debug)
    return res

def script(bdir:str, debug=0):
    param = [
        os.path.join(bdir, JSON_IO),
        os.path.join(bdir, COMT_IN),
    ]
    opts = {}
    what = "D"
    obj = J_LIST
    msg, seq, dct = do_this(what, param, obj, opts, debug=DEBUG)
    if msg:
        print("Error:", msg)
        return 1
    dump_lances(LANCES_IN, dct)
    return 0

def do_this(what, param, obj, opts=None, debug=0):
    msg = ""
    opts = {} if opts is None else opts
    assert isinstance(opts, dict), "Bad options"
    assert param, "Nada?"
    jio_name, comm_name = param
    seq = []
    dct = {}
    if debug > 0:
        print("# Reading:", comm_name, "; io:", jio_name)
    with open(comm_name, "r", encoding=IO_ENCODING) as fdcom:
        comms = [ala.rstrip() for ala in fdcom.readlines() if valid_tsv_line(ala, 4)]
    for idx, item in enumerate(comms, 1001):
        spl = item.split("\t")
        g_id = str(int(spl[0]))
        if debug > 0:
            print(desample(g_id), spl[1:])
        seq.append((idx, spl))
        dct[spl[0]] = spl
    if not os.path.isfile(jio_name):
        print("# Creating:", jio_name)
        create_json(jio_name, obj)
    myobj = json.load(open(jio_name, encoding="ascii"))
    #print(">>>\n" + json_string(myobj) + "<<<\n\n")
    save_json(jio_name, myobj, (seq,))
    return msg, seq, dct

def desample(astr):
    # https://www.chess.com/analysis/game/live/110970067119?tab=review
    res = f"https://www.chess.com/analysis/game/live/{astr}?tab=review"
    return res

def dump_lances(fname, dct):
    with open(fname, "r", encoding=IO_ENCODING) as fdcom:
        lines = [ala.rstrip() for ala in fdcom.readlines() if valid_tsv_line(ala, 3)]
    for line in lines:
        spl = line.split("\t")
        lance_ref, url, comment = spl
        assert lance_ref[0] == "L", lance_ref
        g_id = url.split("/")[-1].split("?", maxsplit=1)[0]
        print(f"# {lance_ref} game-id={g_id}: {comment}")
        assert g_id in dct, "g_id not in dictionary"
    return True

def valid_tsv_line(astr, num_cols=-1):
    last = astr[-1]
    #print(":::", astr)
    assert last == "\n", f"Bad line (last = {ord(last)}d): {[astr]}"
    astr = astr[:-1]
    check = astr.rstrip(" ") == astr
    assert check, f"Tailing blanks? {astr}"
    if astr.startswith("#"):
        return False
    spl = astr.split("\t")
    if num_cols == -1:
        return True
    assert len(spl) == num_cols, f"Wrong tabs: {[astr]}, expected: {num_cols}"
    return True

def create_json(fname, obj):
    """ Create json output for file 'fname' """
    astr = json_string(obj)
    with open(fname, "wb") as fdout:
        fdout.write(astr.encode("ascii"))
    return fname

def save_json(fname, obj, tups):
    seq = tups[0]
    #print("###", seq)
    there = obj["RawComments"]
    last = there[-1]
    new = []
    for idx, spl in seq:
        alist = spl[:1] + [idx] + spl[1:]
        #print("###", idx, alist)
        keys = sorted(last)
        dct = dict(zip(keys, alist))
        new.append(dct)
    new.append(last)
    #print("JSON:", json_string(new))
    obj["RawContents"] = new
    create_json(fname, obj)
    return True

def json_string(obj, ensure_ascii=True):
    """ Dump in JSON format """
    ind, asort, ensure = 2, True, ensure_ascii
    astr = json.dumps(obj, indent=ind, sort_keys=asort, ensure_ascii=ensure)
    assert not astr.endswith('\n'), "No new line?"
    return astr + '\n'

# Main script
if __name__ == "__main__":
    main()
