# Six Of Nine For Every Selected Plane

Status: Phase O5d follow-up audit, outside the paper

## Question

Does the O5c split

```text
9 balanced complements = 6 invertible graphs + 3 rank-one graphs
```

hold for every selected value plane in the globally affine layer,
rather than only for `{11,12,15,16}`?

## Answer

Yes.  The split is uniform across all `24` selected value planes.

Counters:

- affine square-mask pairs: `3456`
- selected value planes: `24`
- selected directions: `6`
- plane record counts: `{'144': 24}`
- used direction counts per plane: `{'6': 24}`
- used direction multiplicities per plane: `{'(24, 24, 24, 24, 24, 24)': 24}`
- balanced complement rank split: `{'(6, 3)': 24}`
- all planes use exactly invertible complements: `True`
- violations: `0`

Thus each selected plane has `144` affine square-mask records and uses
six translation directions, each appearing `24` times.

## Interpretation

For each selected plane direction `U`, let `Q` be its coordinate
partner in the matching.  The nine balanced complements to `U` are
graphs of binary maps `Q -> U` with no zero rows.  The affine layer
uses exactly the six invertible graphs.  This is the uniform version
of the terminal-24 O5c result.
