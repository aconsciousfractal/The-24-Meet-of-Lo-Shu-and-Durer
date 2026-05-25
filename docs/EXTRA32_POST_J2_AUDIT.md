# Extra-32 Post-J2 Audit

Status: Phase K1 targeted invariant audit

## Purpose

Phase J2 separated the `144` exact canonical `V4` records from the `32`
selected-mask-affine extras.  The exact `V4` class has global affine
cell-value labeling; the extras do not, even though their selected masks are
affine and their terminal set-system signature is in the main `176` class.

This audit tests whether three lightweight invariants explain the remaining
`32` extras:

- exact support of the four affine-interpolation mismatches;
- position in the existing small-move Markov graph;
- finite Hilbert-style atom decomposition profile from Phase H.

This is not a complete Markov-basis or Hilbert-basis theorem.

## Certificate

Run:

```powershell
python "scripts/analyze_extra32_post_j2.py" --write
```

Artifacts:

- `results/extra32_post_j2_audit.json`
- `results/EXTRA32_POST_J2_AUDIT_REPORT.md`

## Main Results

The `32` extras keep the Phase-H terminal-set split:

```text
two_diagonal_pair: 16
v4_like_0213:      8
v4_like_1302:      8
```

The affine defect is uniform in size but not in support.  Every extra has
exactly four affine-interpolation mismatches, distributed over four support
patterns:

```text
(r1c1,r1c2,r3c1,r3c2): 9
(r1c1,r1c3,r2c1,r2c3): 7
(r1c2,r1c3,r2c2,r2c3): 9
(r2c1,r2c2,r3c1,r3c2): 7
```

The mismatch support never equals the selected mask:

```text
mismatch support equals selected mask: 0 / 32
mismatch-mask intersection sizes: 0 -> 22, 2 -> 10
```

The small-move Markov graph refines the extras without collapsing them:

```text
degree 0: 12
degree 1: 20
```

The finite Hilbert-style min atom-counts also refine the extras:

```text
12:  4
14:  8
16:  4
18: 12
20:  4
```

## By Terminal-Set Class

### `two_diagonal_pair`

```text
count: 16
source diagonal sizes: 2 -> 12, 4 -> 4
complement-fixed: true -> 8, false -> 8
Hilbert min atom-counts: 14 -> 4, 18 -> 12
Markov degrees: 0 -> 10, 1 -> 6
```

### `v4_like_0213`

```text
count: 8
source diagonal size: 4 -> 8
complement-fixed: false -> 8
Hilbert min atom-counts: 14 -> 4, 20 -> 4
Markov degrees: 0 -> 1, 1 -> 7
```

### `v4_like_1302`

```text
count: 8
source diagonal size: 4 -> 8
complement-fixed: false -> 8
Hilbert min atom-counts: 12 -> 4, 16 -> 4
Markov degrees: 0 -> 1, 1 -> 7
```

## Interpretation

The tested invariants show that the extras are structured, not random.  They
also show that the current invariants do not give a single conceptual
classification.  The best current reading is:

```text
144 exact V4 = affine cell-value class
32 extras    = selected-mask-affine, globally affine-defective frontier
```

Phase K should therefore keep a stop rule: unless a stronger invariant appears,
the `32` extras remain a controlled frontier/appendix layer rather than a
central theorem.

## Guardrails

- Do not claim that the `32` extras form one closed family under the tested
  invariants.
- Do not claim a complete Markov-basis theorem from the small-move graph.
- Do not claim a complete Hilbert-basis theorem from the finite atom audit.
- Do not promote the extras over the cleaner `144` exact canonical `V4`
  affine class unless a new invariant explains them.
