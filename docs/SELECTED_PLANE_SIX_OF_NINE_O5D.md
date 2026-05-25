# Six Of Nine For Every Selected Plane

Status: Phase O5d follow-up audit, outside the paper

## Purpose

Phase O5c explained the terminal-24 exact-`V4` split:

```text
9 balanced complements = 6 invertible graphs + 3 rank-one graphs
```

for the selected value plane `{11,12,15,16}`.  This note verifies the same
split for every selected value plane in the globally affine layer.

Replay artifacts:

```text
scripts/analyze_selected_plane_six_of_nine_o5d.py
tests/test_selected_plane_six_of_nine_o5d.py
results/selected_plane_six_of_nine_o5d.json
results/SELECTED_PLANE_SIX_OF_NINE_O5D_REPORT.md
```

## Result

The split is uniform across all selected value planes:

```text
affine square-mask pairs: 3456
selected value planes: 24
selected directions: 6
records per selected plane: 144
selected planes per selected direction: 4
```

For every selected value plane:

```text
balanced complements to its direction: 9
rank split: 6 invertible graphs + 3 rank-one graphs
used translation directions: exactly the 6 invertible graphs
usage: each of the 6 directions appears 24 times
violations: 0
```

## Interpretation

Let `U` be the selected value-plane direction and `Q` its coordinate partner
in the matching.  Then every balanced complement to `U` is a graph of a
binary map:

```text
Q -> U
```

The globally affine layer uses exactly the invertible maps.  Thus the
terminal-24 exact-`V4` result is not special to the high plane
`{11,12,15,16}`; it is one instance of a uniform affine-layer rule.

## Guardrail

This statement lives in the globally affine order-4 layer.  It does not
classify the non-affine terminal-24 records and does not replace the separate
inside-out/extra-32 audits.
