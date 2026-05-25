# Exact-V4 Affine Mechanism Audit

Status: Phase J2 mechanism / orientation / defect pass

## Purpose

This audit expands Phase J in the three requested directions:

```text
1. linear mechanism behind the 144 exact-canonical V4 records;
2. orientation reading of the V4 wording;
3. affine-defect profile of the 32 selected-mask-affine extras.
```

Replay artifacts:

```text
scripts/analyze_exact_v4_affine_mechanism.py
tests/test_exact_v4_affine_mechanism.py
results/exact_v4_affine_mechanism_audit.json
results/EXACT_V4_AFFINE_MECHANISM_AUDIT_REPORT.md
```

## Linear Mechanism

Every permutation diagonal is read as an affine map:

```text
F2^2 -> F2^2
```

on row/column bit indices.  In this model:

```text
{0123,1032,2301,3210}
```

is exactly the full translation subgroup.

The audit confirms:

```text
exact-V4 terminal sets that are full translation V4: 144/144
selected-affine extras that are full translation V4: 0/32
selected-affine extras that are translation subsets: 16/32
```

Thus the exact-`V4` class is not merely a word-list accident: in the canonical
`F2^2` row/column model it is the full translation terminal subgroup.

## Orientation Reading

Under the eight square symmetries used in the project, the canonical
translation `V4` set has orbit size:

```text
1
```

So the set is stable under those square symmetries.  The broader guardrail
still stands: the literal word set is tied to the chosen row/column bit model
and canonical representative language.  The robust object is:

```text
affine cell-value labeling + transformed-mask F2^4 profile.
```

## Affine Defect

The `144` exact-`V4` records have zero global affine defect:

```text
basis interpolation mismatch:       0
preserved domain affine planes:     140 / 140
preserved permutation diagonals:    24 / 24
```

The `32` selected-mask-affine extras have a uniform nonzero defect:

```text
basis interpolation mismatch:       4
preserved domain affine planes:     76 / 140
preserved permutation diagonals:     8 / 24
```

This is the clean negative control.  The extras keep the same affine
high-value mask / selected-value layer, but the full square is not an affine
cell-value model.

## Interpretation

Phase J2 upgrades the Phase-J finite equivalence into a mechanism-level
finite statement:

```text
exact canonical V4
  = full translation V4 terminal diagonal set
  = global affine cell-value labeling
  = preservation of all 140 domain affine planes
  = preservation of all 24 permutation-diagonal affine planes
```

The broader `176` class is now explained as:

```text
176 selected-mask-affine records
  = 144 globally affine exact-V4 records
  + 32 locally affine-mask but globally defective records.
```

## Consequence

Phase J has become useful enough to keep as a serious follow-up result, not
just appendix bookkeeping.  It still does not prove a universal theorem about
`24`; it explains the internal structure of the exact-`V4` terminal subclass.

## Guardrails

Do not claim:

- selected-mask affineness alone characterizes exact `V4`;
- the 32 extras are noise;
- this is already a general theorem for all order-4 endpoint classes;
- the result explains the Lo Shu side of the meet.
