# The 24-Meet of Lo Shu and Dürer

Public companion repository for the paper:

```text
The 24-Meet of Lo Shu and Dürer:
Bounded Magic Spectra, Sagrada Rays, and F2^4 Transport
```

Author: Oleksiy Babanskyy

This repository contains the paper source/PDF, curated finite replay
artifacts, human-readable certificate notes, and Python scripts/tests for the
bounded Lo Shu/Dürer 24-meet project.  It is a public companion package, not a
dump of the development workspace.

## Layout

```text
paper/      manuscript source, PDF, bibliography, and build notes
data/       curated input data used by the order-four atlas checks
docs/       claim crosswalk, replay scope note, and certificate notes
scripts/    standard-library replay and audit scripts
tests/      pytest smoke/regression tests for the public scripts
results/    canonical JSON and Markdown replay outputs
```

## Quick Check

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
python -m pytest -q
```

The checks are computational reproducibility aids.  They do not replace the
mathematical arguments in the paper; their executable scope is described in
`docs/EXECUTABLE_REPLAY_SCOPE.md`.

Expected result: all public tests pass.  On the reference export this is
`148 passed`; runtime is normally several minutes on a laptop, depending on
Python and filesystem speed.  If GitHub Actions is blocked by platform or
account status, the workflow badge is not a mathematical evidence source;
reviewers should use the local commands and committed replay summary instead.

To regenerate the central public replay artifacts and write
`results/public_reproducibility_check.json`, run:

```bash
python scripts/run_all_reproducibility_checks.py
```

This command intentionally rewrites canonical JSON summaries.  A clean rerun
should preserve the same semantic results; the summary file records return
code `0` for each replay command.

## Paper

The paper lives in `paper/`:

```text
paper/the_24_meet_of_lo_shu_and_durer.tex
paper/refs.bib
paper/the_24_meet_of_lo_shu_and_durer.pdf
paper/BUILD.md
```

## Citation And License

See `CITATION.cff` for citation metadata.  This repository is released under
the MIT license; see `LICENSE`.  Unless otherwise stated, the paper source,
scripts, curated data, and replay artifacts in this companion repository are
covered by that license.
