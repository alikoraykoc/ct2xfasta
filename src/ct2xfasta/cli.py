import argparse
import glob
import os
import sys

from . import parsers, utils, writer


def collect_input_files(inputs, recursive: bool = False, patterns=None):
    if patterns is None:
        patterns = ["*.ct", "*.dbn", "*.bpseq", "*.b"]
    files = []
    for inp in inputs:
        if os.path.isdir(inp):
            for pat in patterns:
                pat_path = os.path.join(inp, "**", pat) if recursive else os.path.join(inp, pat)
                files.extend(glob.glob(pat_path, recursive=recursive))
        else:
            files.append(inp)
    # de-duplicate, keep order
    seen = set()
    uniq = []
    for f in files:
        if f not in seen:
            uniq.append(f)
            seen.add(f)
    return uniq


def parse_file(path: str, forced_fmt: str | None = None):
    fmt = forced_fmt or utils.guess_format(path)
    if fmt == "ct":
        return parsers.parse_ct(path)
    if fmt == "dbn":
        return parsers.parse_dbn(path)
    if fmt == "bpseq":
        return parsers.parse_bpseq(path)
    raise ValueError(f"Unsupported format: {fmt}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Convert CT/DBN/BPSEQ RNA structures to 4SALE XFasta.")
    p.add_argument(
        "-i",
        "--input",
        nargs="+",
        required=True,
        help="Input files and/or directories.",
    )
    p.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recurse into subdirectories for directory inputs.",
    )
    p.add_argument(
        "--glob",
        nargs="+",
        default=["*.ct", "*.dbn", "*.bpseq", "*.b"],
        help="Glob patterns for directory inputs (quote in zsh).",
    )
    p.add_argument(
        "-o",
        "--output",
        default="output.xfasta",
        help="Output filename (XFasta or dot-bracket).",
    )
    p.add_argument(
        "--format",
        choices=["ct", "dbn", "bpseq"],
        help="Force input format; otherwise guessed from extension.",
    )
    p.add_argument(
        "--dot-bracket",
        action="store_true",
        help="Write only names + dot-bracket (no sequences).",
    )
    p.add_argument(
        "--name-map",
        help="TSV mapping: basename<TAB>desired_name.",
    )
    # QoL
    p.add_argument("--rna", action="store_true", help="Convert T->U (DNA to RNA).")
    p.add_argument("--upper", action="store_true", help="Uppercase sequences.")
    p.add_argument("--lower", action="store_true", help="Lowercase sequences.")
    p.add_argument(
        "--strip-gaps",
        action="store_true",
        help="Remove '-', '.' and spaces from sequences.",
    )
    # validation & selection
    p.add_argument(
        "--validate",
        action="store_true",
        help="Report basic structure issues and non-canonical pairs.",
    )
    p.add_argument(
        "--structure",
        type=int,
        help="If a file has multiple structures, select the Nth (1-based).",
    )

    args = p.parse_args(argv)

    files = collect_input_files(args.input, args.recursive, args.glob)
    if not files:
        print("[ERROR] No input files found.", file=sys.stderr)
        return 1

    name_map = utils.read_name_map(args.name_map) if args.name_map else {}

    out_records = []
    for path in files:
        try:
            recs = parse_file(path, args.format)
        except Exception as e:
            print(f"[WARN] Skipping {path}: {e}", file=sys.stderr)
            continue

        # Select one structure if requested
        if args.structure is not None:
            if args.structure < 1 or args.structure > len(recs):
                print(
                    f"[WARN] {os.path.basename(path)} has {len(recs)} structure(s); "
                    f"--structure {args.structure} is out of range",
                    file=sys.stderr,
                )
                continue
            recs = [recs[args.structure - 1]]

        base = os.path.basename(path)
        for idx, (name, seq, dot) in enumerate(recs, start=1):
            # apply name-map; keep suffix for multi-structure
            newname = name_map.get(base)
            if newname:
                name = f"{newname}_{idx}" if len(recs) > 1 else newname

            seq2 = utils.normalize_sequence(
                seq,
                to_upper=args.upper,
                to_lower=args.lower,
                rna=args.rna,
                strip_gaps=args.strip_gaps,
            )
            # validation reports
            if args.validate:
                from . import validate

                errs = validate.basic_consistency(seq2, dot)
                for e in errs:
                    print(
                        f"[VALIDATE] {os.path.basename(path)}::{name}: {e}",
                        file=sys.stderr,
                    )
                noncanon = validate.noncanonical_pairs(seq2, dot)
                if noncanon:
                    for j, b1, i2, b2 in noncanon[:20]:
                        print(
                            "[VALIDATE] "
                            f"{os.path.basename(path)}::{name}: "
                            f"non-canonical pair {j}{b1}-{i2}{b2}",
                            file=sys.stderr,
                        )
                    if len(noncanon) > 20:
                        print(
                            f"[VALIDATE] ... and {len(noncanon) - 20} more",
                            file=sys.stderr,
                        )

            out_records.append((name, seq2, dot))

    if not out_records:
        print("[ERROR] No structures parsed.", file=sys.stderr)
        return 2

    with open(args.output, "w", encoding="utf-8") as fh:
        if args.dot_bracket:
            writer.write_dotbracket(out_records, fh)
        else:
            writer.write_xfasta(out_records, fh)

    print(f"[INFO] Wrote {len(out_records)} record(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
