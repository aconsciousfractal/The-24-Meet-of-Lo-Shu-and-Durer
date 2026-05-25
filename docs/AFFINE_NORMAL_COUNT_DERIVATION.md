# Affine Normal Count Derivation

Status: Phase O4 linear-algebra derivation

## Purpose

Phase O2/O3 explained why the `144` exact-`V4` class is one selected value
plane in the globally affine normal order-4 layer.  The remaining gap was the
total:

```text
432 globally affine essential representatives.
```

This note derives that number from a finite `F2^4` linear-algebra count,
without enumerating the full `880` essential order-4 atlas.

Replay artifacts:

```text
scripts/analyze_affine_normal_count_derivation.py
tests/test_affine_normal_count_derivation.py
results/affine_normal_count_derivation.json
results/AFFINE_NORMAL_COUNT_DERIVATION_REPORT.md
```

## Balanced Directions

A globally affine square has value labels:

```text
value - 1 = A x + b
```

with `A in GL(4,2)` and `b in F2^4`.

For a 4-cell affine plane to have value sum `34`, its direction must be
balanced: no coordinate bit is constant on that direction.  In `F2^4` there
are:

```text
35 two-dimensional subspaces
13 balanced directions
```

The row direction, column direction, and diagonal direction in the domain are
pairwise complementary 2-planes.  The main and anti-diagonal are parallel
affine planes, so they share the same direction.

## Linear Parts

A linear part is good exactly when it sends the row, column, and diagonal
directions to balanced directions.  The finite linear count is:

```text
ordered pairwise-complementary balanced image triples: 36
maps per image triple: 6
good linear parts: 36 x 6 = 216
```

The factor `6` is the stabilizer size of the ordered domain triple of row,
column, and diagonal directions.

## From Raw To Essential

Offsets are free:

```text
216 good linear parts x 16 offsets = 3456 raw affine normal squares
```

Every normal 4x4 square has distinct entries, so no nontrivial square symmetry
can fix it cellwise.  Thus every square-symmetry orbit has size `8`:

```text
3456 / 8 = 432 essential affine representatives.
```

## Link To The 144 Class

Phase O3 then supplies the final split:

```text
432 globally affine essential representatives
  = 3 coordinate-axis matchings x 144

432 x 8 admissible masks
  = 3456 affine square-mask pairs
  = 24 selected value planes x 144
```

The terminal-24 exact-`V4` class is the high selected value plane:

```text
{11,12,15,16}
```

## Guardrail

This is a finite `F2^4` theorem for globally affine normal order-4 squares.
It does not classify non-affine terminal-24 records and does not claim a
universal theorem for all magic-square categories.
