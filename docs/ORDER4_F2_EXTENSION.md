# Order-4 F2 Extension

Status: Phase F extension across the Phase-C terminal-24 records

## Purpose

This note extends the `F2^4` / tesseract classifier from the single
Durer/Sagrada pair to all `236` terminal-24 square-mask pairs in the internal
880-essential-square dataset.

For each normal order-4 square `Q`, label a cell by:

```text
Q[i,j] - 1 in {0,...,15} = F2^4.
```

This gives two different tests:

1. whether the selected mask is an affine plane in value-label space;
2. whether the whole cell-value map `(row,column) -> Q[i,j]-1` is affine from
   row/column bits to value bits.

The replay artifacts are:

```text
scripts/analyze_order4_f2_extension.py
tests/test_order4_f2_extension.py
results/order4_f2_extension.json
results/ORDER4_F2_EXTENSION_REPORT.md
```

## Main Result

Across the `236` terminal-24 pairs:

```text
all 880 essential squares with affine cell-value labeling: 432
all 880 essential squares with non-affine cell-value labeling: 448
selected mask affine plane: 176
selected mask non-affine: 60
cell-value labeling affine automorphism: 144
exact canonical V4 pairs: 144
```

The key equality is:

```text
terminal-24 pairs with affine cell-value labeling
= exact canonical V4 terminal subclass
```

This is a new Phase-F discriminator.  It does not make endpoint `24` unique,
but it gives the exact canonical `V4` subclass a clean finite-affine
characterization in the chosen essential-square orientation.

## Exact Canonical V4 Subclass

All `144` exact canonical `V4` pairs satisfy:

```text
cell-value labeling is an affine automorphism of F2^4
selected mask is an affine plane
selected mask direction is {0,1,4,5}
terminal affine layer is pure transport
terminal affine count = 36
transported source-34 incidence-1 affine count = 36
```

Thus the Durer/Sagrada Phase-F structure is not unique to the 8-pair Durer
cell.  It persists across the full exact canonical `V4` subclass.

## Selected-Value Profiles

The affine mask property is controlled by the selected values.  The dominant
signature is:

```text
values {11,12,15,16}: 176 pairs
mask affine: true
terminal count: 96
terminal affine count: 36
pure transport: true
```

Other terminal-24 selected signatures are non-affine in value-label space.
One non-affine signature also has pure terminal affine transport:

```text
values {11,13,14,15}: 8 pairs
terminal affine count: 30
pure transport: true
```

So pure transport alone is weaker than the full exact canonical `V4`
fingerprint.  The strong Phase-F package is:

```text
affine cell-value labeling
+ affine selected mask direction {0,1,4,5}
+ exact canonical V4 terminal diagonal set
+ terminal affine count 36
```

## Guardrails

Do not claim:

- the `F2^4` structure isolates the Durer/Sagrada 8-cell;
- all terminal-24 masks are affine planes;
- pure terminal affine transport alone characterizes exact canonical `V4`;
- affine cell-value labeling is orientation-free before checking how the
  880 essential representatives were canonicalized.

The correct statement is narrower and useful: in the current Phase-C essential
orientation, affine cell-value labeling exactly matches the 144-pair exact
canonical `V4` terminal subclass.
