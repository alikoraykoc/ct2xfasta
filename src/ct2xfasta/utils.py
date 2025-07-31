import os


def normalize_sequence(
    seq: str,
    to_upper: bool = False,
    to_lower: bool = False,
    rna: bool = False,
    strip_gaps: bool = False,
) -> str:
    s = seq
    if strip_gaps:
        s = s.replace("-", "").replace(".", "").replace(" ", "")
    if rna:
        s = s.replace("T", "U").replace("t", "u")
    if to_upper and to_lower:
        to_lower = False
    if to_upper:
        s = s.upper()
    elif to_lower:
        s = s.lower()
    return s


def read_name_map(path: str) -> dict:
    mapping = {}
    if not path:
        return mapping
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            mapping[os.path.basename(parts[0])] = parts[1]
    return mapping


def guess_format(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".ct":
        return "ct"
    if ext in [".dbn", ".dot", ".vienna", ".b"]:
        return "dbn"
    if ext in [".bpseq", ".bp"]:
        return "bpseq"
    return "ct"
