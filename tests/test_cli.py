import textwrap
from ct2xfasta.cli import main


def write_tmp(path, content):
    path.write_text(textwrap.dedent(content), encoding="utf-8")


def test_cli_basic_ct(tmp_path):
    ct = tmp_path / "a.ct"
    write_tmp(
        ct,
        """\
    3  X
    1 A 0 2 0 1
    2 U 1 3 3 2
    3 G 2 0 2 3
    """,
    )
    out = tmp_path / "o.xfasta"
    rc = main(["-i", str(ct), "-o", str(out)])
    assert rc == 0
    lines = out.read_text().strip().splitlines()
    assert len(lines) == 3 and lines[0].startswith(">")


def test_cli_dbn_b_extension(tmp_path):
    dbn = tmp_path / "m.b"
    write_tmp(
        dbn,
        """\
    AUGCU
    (..())
    """,
    )
    out = tmp_path / "o2.xfasta"
    rc = main(["-i", str(dbn), "-o", str(out)])
    assert rc == 0
    lines = out.read_text().strip().splitlines()
    assert len(lines) == 3 and lines[2] == "(..())"
