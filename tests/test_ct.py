import textwrap
from ct2xfasta import parsers, validate

def write_tmp(path, content):
    path.write_text(textwrap.dedent(content), encoding="utf-8")

def test_parse_ct_single(tmp_path):
    ct = tmp_path / "single.ct"
    write_tmp(ct, """\
    5  MySeq_1 dG=-2.3
    1 A 0 2 0 1
    2 U 1 3 0 2
    3 G 2 4 5 3
    4 C 3 5 0 4
    5 U 4 0 3 5
    """)
    recs = parsers.parse_ct(str(ct))
    assert len(recs) == 1
    name, seq, dot = recs[0]
    assert seq == "AUGCU"
    assert len(seq) == len(dot)
    assert not validate.basic_consistency(seq, dot)
