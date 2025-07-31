import os
import re
from typing import List, Tuple


def _pairs_to_dotbracket(pairs: list) -> str:
    n = len(pairs)
    dot = ["." for _ in range(n)]
    for i, pair in enumerate(pairs, start=1):
        if pair > 0 and i < pair <= n:
            dot[i - 1] = "("
            if dot[pair - 1] == ".":
                dot[pair - 1] = ")"
    return "".join(dot)


def parse_ct(path: str) -> List[Tuple[str, str, str]]:
    structs = []
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip() != ""]
    i = 0
    block_idx = 0
    while i < len(lines):
        header = lines[i]
        parts = header.split()
        try:
            n = int(parts[0])
        except Exception as e:
            raise ValueError(f"Invalid CT header at line {i+1}: {header}") from e

        name = "structure_" + str(block_idx + 1)
        if len(parts) > 1:
            name = "_".join(parts[1:])

        block = lines[i + 1 : i + 1 + n]
        if len(block) < n:
            raise ValueError(f"Incomplete CT block (expected {n} rows) in {path}")

        seq_chars = []
        pairs = [0] * n
        for row in block:
            cols = row.split()
            if len(cols) < 5:
                raise ValueError(f"Malformed CT row: {row}")
            base = cols[1]
            pair = int(cols[4])
            seq_chars.append(base)
            pairs[len(seq_chars) - 1] = pair

        dot = _pairs_to_dotbracket(pairs)
        structs.append((name, "".join(seq_chars), dot))
        i = i + 1 + n
        block_idx += 1
    return structs


# --- NEW: Vienna / DBN ---
_dbn_struct_re = re.compile(r"^([().\[\]<>]+)")


def parse_dbn(path: str) -> List[Tuple[str, str, str]]:
    """
    Supports both styles:
      >name
      SEQUENCE
      STRUCTURE [optional energy]
    or
      SEQUENCE
      STRUCTURE [optional energy]
    Repeated blocks are supported.
    """
    out = []
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith(">"):
            name = line[1:].strip() or "record"
            if i + 2 >= len(lines):
                break
            seq = lines[i + 1].strip()
            struct_line = lines[i + 2].strip()
            m = _dbn_struct_re.match(struct_line)
            if not m:
                raise ValueError(f"DBN structure line not recognized: {struct_line}")
            dot = m.group(1)
            out.append((name, seq, dot))
            i += 3
        else:
            # headerless: seq + structure
            if i + 1 >= len(lines):
                break
            seq = line
            struct_line = lines[i + 1].strip()
            m = _dbn_struct_re.match(struct_line)
            if not m:
                raise ValueError(f"DBN structure line not recognized: {struct_line}")
            dot = m.group(1)
            # derive a name from filename with incremental index
            base = os.path.splitext(os.path.basename(path))[0]
            name = f"{base}_{len(out)+1}"
            out.append((name, seq, dot))
            i += 2
    return out


def parse_bpseq(path: str) -> List[Tuple[str, str, str]]:
    """
    BPSEQ: index base pair_index (3 columns). '#' lines are comments.
    """
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            rows.append(ln)
    seq = []
    pairs = []
    for row in rows:
        cols = row.split()
        if len(cols) < 3:
            continue
        base = cols[1]
        pair = int(cols[2])
        seq.append(base)
        pairs.append(pair)
    dot = _pairs_to_dotbracket(pairs)
    name = os.path.splitext(os.path.basename(path))[0]
    return [(name, "".join(seq), dot)]
