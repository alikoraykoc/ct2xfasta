from typing import Iterable, Tuple, TextIO

def write_xfasta(records: Iterable[Tuple[str, str, str]], fh: TextIO):
    for name, seq, dot in records:
        fh.write(f">{name}\n")
        fh.write(f"{seq}\n")
        fh.write(f"{dot}\n")

# NEW
def write_dotbracket(records: Iterable[Tuple[str, str, str]], fh: TextIO):
    for name, _seq, dot in records:
        fh.write(f">{name}\n")
        fh.write(f"{dot}\n")