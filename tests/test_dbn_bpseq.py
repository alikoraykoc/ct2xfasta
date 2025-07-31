import textwrap
from ct2xfasta import parsers

def write_tmp(path, content):
    path.write_text(textwrap.dedent(content), encoding="utf-8")

def test_parse_dbn_headerless(tmp_path):
    dbn = tmp_path / "v.dbn"
    write_tmp(dbn, """\
    AUGC
    (.())
    """)
    recs = parsers.parse_dbn(str(dbn))
    assert len(recs) == 1
    assert recs[0][1] == "AUGC"
    assert recs[0][2].count("(") == 2

def test_parse_bpseq(tmp_path):
    bp = tmp_path / "s.bpseq"
    write_tmp(bp, """\
    1 A 0
    2 U 4
    3 G 0
    4 C 2
    """)
    recs = parsers.parse_bpseq(str(bp))
    assert len(recs) == 1
    assert recs[0][1] == "AUGC"
    