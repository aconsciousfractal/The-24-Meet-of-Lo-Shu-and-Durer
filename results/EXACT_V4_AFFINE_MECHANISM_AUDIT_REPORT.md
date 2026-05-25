# Exact-V4 Affine Mechanism Audit

Status: Phase J2 mechanism / orientation / defect pass

## Summary

- terminal-24 pairs: `236`
- exact canonical `V4` pairs: `144`
- selected-affine extras: `32`

## Linear Mechanism

- exact-`V4` terminal sets that are full translation `V4`: `144`
- exact-`V4` all full translation `V4`: `True`
- selected-affine extras that are translation subsets: `16`
- selected-affine extras that are full translation `V4`: `0`

The exact-`V4` class is therefore literally the full translation
subgroup in the canonical `F2^2` row/column model.  The extras may
contain translation subsets, but never the full translation `V4`.

## Orientation

- square-symmetry orbit size of canonical `V4`: `1`
- all exact-`V4` terminal sets lie in that orbit: `True`
- selected-affine extra terminal sets in that orbit: `0`

The literal word set remains orientation language.  The stable object
is the affine cell-value criterion plus the transformed-mask `F2^4`
profile.

## Affine Defect

- exact-`V4` basis mismatch distribution: `{'0': 144}`
- extra basis mismatch distribution: `{'4': 32}`
- exact-`V4` preserved domain affine planes: `{'140': 144}`
- extra preserved domain affine planes: `{'76': 32}`
- exact-`V4` preserved permutation diagonals as affine planes: `{'24': 144}`
- extra preserved permutation diagonals as affine planes: `{'8': 32}`

This gives the clean negative control: the 32 extras have the same
selected affine high-value mask, but their full cell-value map fails
to preserve all affine planes and all permutation-diagonal planes.

## Interpretation

Phase J2 upgrades the finite equivalence into a mechanism-level finite
statement:

```text
exact canonical V4
  = full translation V4 terminal diagonal set
  = global affine cell-value labeling
  = preservation of all 140 domain affine planes
  = preservation of all 24 permutation-diagonal affine planes
```

The 32 extras explain why selected-mask affineness is insufficient:
they retain the affine high-value mask but have a nonzero global
affine defect.
