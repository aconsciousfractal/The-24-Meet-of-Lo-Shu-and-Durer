# Reproducing The Companion Checks

This repository is a standalone public companion for the 24-meet paper.

## Environment

- Python 3.10+
- `pytest`
- A LaTeX distribution for rebuilding the paper

Install the Python test dependency:

```bash
pip install -r requirements.txt
```

Run the public test suite:

```bash
python -m pytest -q
```

Run the bundled reproducibility smoke/audit command.  This regenerates the
central public replay artifacts and writes
`results/public_reproducibility_check.json`:

```bash
python scripts/run_all_reproducibility_checks.py
```

## Core Replay Commands

The most central replay commands are:

```bash
python scripts/magic24_certificates.py --write
python scripts/analyze_f2_tesseract.py --write
python scripts/analyze_affine_normal_count_derivation.py --write
python scripts/analyze_forbidden_shadow_split_p6.py --write
```

Additional scripts in `scripts/` regenerate the corresponding JSON artifacts
in `results/`.

The public all-in-one replay may rewrite canonical JSON files under
`results/`.  It is designed as a reproducibility/update command, not as a
read-only checker.

## Paper Build

From `paper/` run:

```bash
pdflatex -interaction=nonstopmode -halt-on-error the_24_meet_of_lo_shu_and_durer.tex
bibtex the_24_meet_of_lo_shu_and_durer
pdflatex -interaction=nonstopmode -halt-on-error the_24_meet_of_lo_shu_and_durer.tex
pdflatex -interaction=nonstopmode -halt-on-error the_24_meet_of_lo_shu_and_durer.tex
```

## Main Artifact Map

| Paper layer | Canonical artifacts |
|---|---|
| Strong meet and Sagrada ray | `results/magic24_certificate_pack.json` |
| D4 -> V4 and Type-A guardrail | `results/s4_chamber_fingerprints.json`, `results/s4_poset_cone_comparison.json` |
| F_2^4 tesseract transport | `results/f2_tesseract_analysis.json` |
| Polytope guardrail | `results/bounded_magic_polytope.json`, `results/fixed_sum24_polytope_audit.json` |
| Order-four terminal atlas | `data/order4_normal_essential_880.json`, `results/order4_endpoint_spectrum.json` |
| Exact V4 affine class | `results/exact_v4_affine_class_audit.json`, `results/order4_f2_extension.json` |
| O5/Johnson refinement | `results/johnson_*`, `results/*o5*`, `results/forbidden_shadow_split_p6.json` |

## Scope Boundary

The scripts replay finite enumerations and produce JSON summaries.  The
mathematical proofs and interpretations are in the paper.  See
`docs/EXECUTABLE_REPLAY_SCOPE.md` for what is included and what is deliberately
outside this public package.
