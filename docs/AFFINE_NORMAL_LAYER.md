# Affine Normal Order-4 Layer

Status: Phase O2 generalization pass

## Purpose

Phase O characterized the `144` exact-`V4` records inside the `236`
terminal-24 atlas.  Phase O2 asks whether the number `144` has a larger
source before applying the terminal-24 filter.

The answer is yes: it comes from a uniform selected-value-plane distribution
inside the globally affine normal order-four layer.

Replay artifacts:

```text
scripts/analyze_affine_normal_layer.py
tests/test_affine_normal_layer.py
results/affine_normal_layer.json
results/AFFINE_NORMAL_LAYER_REPORT.md
```

## Result

Among the `880` essential normal order-four representatives:

```text
globally affine cell-value representatives: 432
admissible masks per representative: 8
affine square-mask pairs: 3456
```

These `3456` affine square-mask pairs distribute uniformly over:

```text
24 selected value planes x 144 pairs.
```

Equivalently:

```text
selected value plane count distribution: 144 repeated 24 times
selected direction count distribution: 576 repeated 6 times
```

## Endpoint-24 Consequence

Within this globally affine layer, endpoint `24` is exactly one selected
value plane:

```text
selected values {11,12,15,16}: 144 pairs
```

and all of these have terminal diagonal set:

```text
{0123,1032,2301,3210}
```

which is the full translation `V4` in the canonical `F2^2` row/column model.

Thus the exact-`V4` `144` class is explained as:

```text
one selected value plane inside the globally affine normal layer
```

rather than as an isolated count inside the terminal-24 atlas.

## Interpretation

This is the strongest current explanation of the `144` count:

```text
432 affine representatives x 8 masks = 3456 affine mask records
3456 / 24 selected value planes = 144
```

The terminal-24 plane is the high plane `{11,12,15,16}`.  It inherits full
translation terminal `V4`.

## Guardrail

This is a finite normal-order-four statement.  It does not include the
non-affine terminal-24 records, and it does not claim a universal theorem
for all magic-square categories.
