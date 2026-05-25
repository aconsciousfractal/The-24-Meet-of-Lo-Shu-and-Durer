# Exact-V4 Structural Characterization

Status: Phase O finite structural characterization audit

## Purpose

Phase O sharpens the Phase-J/J2 result.  Instead of only recording that
`exact canonical V4` and affine cell-value labeling have the same `144`
records, it asks which internal conditions are exactly equivalent to that
class inside the `236` terminal-24 atlas.

Replay artifacts:

```text
scripts/analyze_exact_v4_structural_characterization.py
tests/test_exact_v4_structural_characterization.py
results/exact_v4_structural_characterization.json
results/EXACT_V4_STRUCTURAL_CHARACTERIZATION_REPORT.md
```

## Result

Inside the `236` terminal-24 square-mask pairs, the following single
conditions are equivalent:

```text
exact canonical V4
cell-value affine
zero affine defect
full translation terminal V4
preserves all 140 domain affine planes
preserves all 24 permutation-diagonal affine planes
```

Thus the `144` class is not just a word-list artifact.  It is the zero-defect
global affine class, equivalently the class whose terminal diagonal set is
the full translation `V4` in the canonical `F2^2` row/column model.

## Broad Filters

Several natural conditions contain all `144` exact-`V4` records but are too
broad:

```text
selected-mask affine: 176 records
selected values {11,12,15,16}: 176 records
terminal affine count 36: 176 records
pure terminal affine transport: 184 records
terminal quaterne count 96: 184 records
translation-subset terminal set: 196 records
```

The important broad filter is the main `176` class:

```text
176 = 144 exact V4 / zero-defect global affine
    + 32 selected-affine defect-4 extras
```

## Defect Stratification

The `236` terminal-24 records split by global affine defect as:

```text
144 exact selected-affine records:
  mismatch 0, preserved planes 140/140, preserved permutation diagonals 24/24

32 selected-affine non-exact records:
  mismatch 4, preserved planes 76/140, preserved permutation diagonals 8/24

32 nonselected non-exact records:
  mismatch 4, preserved planes 76/140, preserved permutation diagonals 8/24

28 nonselected non-exact records:
  mismatch 6, preserved planes 44/140, preserved permutation diagonals 0/24
```

## Interpretation

The strongest current characterization is finite but structural:

```text
exact V4 = zero-defect global affine terminal-24 class.
```

The `32` extras are not noise.  They are the first near-miss layer: they have
the same affine selected high-value mask as the `144` class, but they fail the
global affine condition by defect `4`.

## Guardrail

This is not yet a general theorem for all order-four endpoint classes.  It is
a certified characterization inside the `236` terminal-24 atlas, and it does
not explain the Lo Shu side of the meet.
