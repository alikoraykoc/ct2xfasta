ct2xfasta

Convert RNA secondary structures from CT / DBN (Vienna) / BPSEQ into 4SALE‑compatible XFasta.

XFasta layout:

>SequenceName
ACGUACGUACGU...
(((....)))....

<!-- Optional CI badge: replace USER/REPO -->



⸻

Features
	•	Multiple input formats: .ct, .dbn / .dot / .vienna / .b (Vienna), .bpseq
	•	Solid CLI:
	•	Files and/or directories
	•	-r/--recursive directory traversal
	•	--glob patterns (quote them!)
	•	--name-map TSV (basename → desired name)
	•	Output:
	•	XFasta (default): >name, SEQUENCE, STRUCTURE
	•	--dot-bracket mode: >name, STRUCTURE (no sequence)
	•	Quality‑of‑life flags: --rna (T→U), --upper/--lower, --strip-gaps
	•	Multi‑structure CT: parse multiple structures in a single .ct file; --structure N to select one
	•	Validation (--validate): basic checks + non‑canonical pairs report
	•	Works with MFold, ViennaRNA, RNAstructure outputs (dot‑bracket supported; MFold .b treated as DBN)

⸻

Install (local dev)

pip install -e .

Tip: Use a virtual environment (e.g. python -m venv .venv && source .venv/bin/activate).

⸻

Quick start

# Single CT file → XFasta
ct2xfasta -i sample.ct -o sample.xfasta

# Vienna/MFold .b (dot‑bracket) with validation
ct2xfasta -i myfile.b --validate -o myfile_valid.xfasta

# Directory with recursion (quote globs for zsh/bash consistency)
ct2xfasta -i data/ -r --glob "*.ct" "*.b" -o all.xfasta

# Select structure #2 from a multi-structure CT
ct2xfasta -i multi.ct --structure 2 -o second.xfasta

# Output only dot‑bracket (no sequences)
ct2xfasta -i samples/*.dbn --dot-bracket -o structs.fa

# Rename sequences via TSV (basename<TAB>desired_name)
ct2xfasta -i data/ --name-map samples.tsv -o named.xfasta


⸻

Input formats
	•	CT (.ct): Supports single or multiple structures per file.
The parser reads the length/header line and the following n rows per structure.
	•	DBN (Vienna dot‑bracket): .dbn, .dot, .vienna, .b (MFold “bracket”).
	•	Both headerless:

SEQUENCE
STRUCTURE [optional energy]

and FASTA‑style:

>name
SEQUENCE
STRUCTURE [optional energy]


	•	Any trailing energy like (-155.74) is ignored.

	•	BPSEQ (.bpseq, .bp): three columns per line (index base pair_index); # comments allowed.

If unsure, the CLI guesses by extension (or use --format {ct,dbn,bpseq}).

⸻

Output formats
	•	XFasta (default)

>name
SEQUENCE
STRUCTURE


	•	Dot‑bracket only (--dot-bracket)

>name
STRUCTURE



⸻

CLI options (summary)

-i, --input         One or more files and/or directories (required)
-r, --recursive     Recurse into subdirectories (when inputs include directories)
--glob              Glob patterns for directory inputs (default: "*.ct" "*.dbn" "*.bpseq" "*.b")
-o, --output        Output file (default: output.xfasta)
--format            Force input format: ct | dbn | bpseq
--dot-bracket       Write only names + dot-bracket (no sequences)
--name-map          TSV mapping file: basename<TAB>desired_name
--structure N       If a file has multiple structures, select the Nth (1-based)

# Quality-of-life
--rna               Convert T->U (DNA→RNA)
--upper             Uppercase sequences
--lower             Lowercase sequences
--strip-gaps        Remove '-', '.' and spaces from sequences

--validate          Report basic issues + non-canonical pairs

Note for zsh users: Always quote glob patterns to let the tool expand them:

ct2xfasta -i data/ -r --glob "*.ct" "*.b"


⸻

Validation

Enable with --validate to print messages to stderr:
	•	Length mismatch between sequence and structure
	•	Unbalanced parentheses
	•	Non‑canonical pairs (reports up to the first 20):
canonical set includes A‑U, U‑A, G‑C, C‑G, G‑U, U‑G (wobble).

⸻

XFasta in 4SALE

Open 4SALE and use Load Aligned Structures to import the generated XFasta.
Each record provides the primary sequence and matching dot‑bracket structure.

⸻

Name mapping

Provide a simple TSV file mapping input basenames to desired FASTA headers:

myfile.b	ITS2_Sample_A
sample.ct	Species_B

Then:

ct2xfasta -i data/ --name-map samples.tsv -o named.xfasta

If a file contributes multiple structures, the tool appends _1, _2, … to keep names unique.

⸻

Tests & CI
	•	Run tests locally:

pip install pytest
pytest -q


	•	GitHub Actions workflow (.github/workflows/ci.yml) runs ruff, black (check), and pytest on each push/PR.

⸻

Roadmap
	•	Optional input FASTA + dot‑bracket pairing (two‑file mode)
	•	Non‑canonical filter/override options
	•	Pre‑commit hooks (ruff + black)
	•	PyPI release (pipx install ct2xfasta)

⸻

License

MIT — see LICENSE.

⸻

Citation / Acknowledgements

If you find this useful in your ITS2 / secondary structure workflows, please cite the repository.
Thanks to MFold, ViennaRNA, and the 4SALE team for their tools and formats that inspired this converter.

⸻

Author: Ali Koray Koç
Issues and contributions are welcome!