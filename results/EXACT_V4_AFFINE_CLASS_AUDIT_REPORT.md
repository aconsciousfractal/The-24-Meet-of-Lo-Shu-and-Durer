# Exact-V4 Affine Class Audit

Status: Phase J finite characterization pass

## Summary

- terminal-24 pairs: `236`
- selected-mask affine / values `{11,12,15,16}`: `176`
- affine cell-value labeling pairs: `144`
- exact canonical `V4` pairs: `144`
- exact canonical `V4` equals affine cell-value labeling: `True`
- selected-mask affine equals selected values `{11,12,15,16}`: `True`
- exact canonical `V4` equals selected-mask affine plus affine cell-value labeling: `True`

## Minimal Filter Ladder

- `terminal24`: `236`
- `selected_values_11_12_15_16_or_selected_mask_affine`: `176`
- `plus_affine_cell_value_labeling`: `144`
- `exact_canonical_v4`: `144`

## Main 176 Split

`{'cell_affine_exact_v4': 144, 'cell_non_affine_non_exact': 32}`

The selected-mask affine class has `176` pairs.  It splits as
`144` affine cell-value labelings, all exact canonical `V4`, plus
`32` non-affine cell-value labelings, none exact canonical `V4`.

## Extra Terminal Sets

`{'0123,0213,3120,3210': 8, '0123,1302,2031,3210': 8, '0123,3210': 16}`

## Orientation Reading

- `affine_cell_value_criterion_stable_under_d4`: `True`
- `affine_cell_value_criterion_stable_under_complement`: `True`
- `terminal24_pair_f2_profiles_stable_under_d4`: `True`
- `canonical_v4_wording_orientation_free`: `False`

## Interpretation

Within the terminal-24 dataset, the strongest current Phase-J
statement is a finite equivalence:

```text
exact canonical V4
  <=> affine cell-value labeling
  <=> selected-mask affine plus affine cell-value labeling
```

The first filter `selected-mask affine` is too broad: it is the
`176`-pair main class.  The affine cell-value condition removes
exactly the `32` structured extras.

The affine cell-value criterion is stable under square symmetries
and value complement, but the literal phrase `exact canonical V4`
is still canonical-orientation wording.

## Paper Consequence

Do not delay paper v2 for a conceptual proof beyond this finite
equivalence.  The result is strong enough as an appendix-backed
finite theorem; a broader conceptual explanation belongs to a
follow-up Type-A/subgroup-tiler project.
