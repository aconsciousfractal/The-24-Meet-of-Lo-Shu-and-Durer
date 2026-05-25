# Exact-V4 Structural Characterization

Status: Phase O finite structural characterization audit

## Scope

This audit works inside the `236` terminal-24 order-four
square-mask records.  It asks which conditions are equivalent to
the `144`-pair exact canonical `V4` subclass, and which conditions
are only broader filters.

## Equivalent Single Conditions

- `cell_value_affine`
- `full_translation_terminal_v4`
- `preserves_all_140_domain_affine_planes`
- `preserves_all_24_permutation_diagonal_planes`
- `zero_affine_defect`

Thus, within the terminal-24 atlas, the exact canonical `V4`
class is equivalently:

```text
global affine cell-value class
zero affine-defect class
full translation terminal-V4 class
class preserving all 140 domain affine planes
class preserving all 24 permutation-diagonal affine planes
```

## Too-Broad Conditions

- `pure_terminal_affine_transport`: count `184`, false positives `40`
- `selected_mask_affine`: count `176`, false positives `32`
- `selected_values_11_12_15_16`: count `176`, false positives `32`
- `terminal_affine_count_36`: count `176`, false positives `32`
- `terminal_count_96`: count `184`, false positives `40`
- `translation_subset_terminal`: count `196`, false positives `52`

The key broad filter is selected-mask affineness / selected values
`{11,12,15,16}`.  It gives the `176`-pair main class, not the
`144` exact-`V4` class.

## Composite Checks

- `selected_mask_affine_and_cell_value_affine`: count `144`, equivalent `True`
- `selected_values_11_12_15_16_and_cell_value_affine`: count `144`, equivalent `True`
- `selected_mask_affine_and_full_translation_terminal_v4`: count `144`, equivalent `True`
- `terminal_affine_count_36_and_zero_affine_defect`: count `144`, equivalent `True`

## Defect Stratification

- `exact | selected_affine=True | mismatch=0 | planes=140 | perm_diags=24`: `144`
- `nonexact | selected_affine=False | mismatch=4 | planes=76 | perm_diags=8`: `32`
- `nonexact | selected_affine=False | mismatch=6 | planes=44 | perm_diags=0`: `28`
- `nonexact | selected_affine=True | mismatch=4 | planes=76 | perm_diags=8`: `32`

## Nonexact Near Misses

- `nonselected_defect4`: `32`
- `nonselected_defect6`: `28`
- `selected_affine_defect4`: `32`

## Interpretation

Phase O upgrades the Phase-J equality into a sharper finite
characterization.  The `144` class is not merely the terminal
word set `{0123,1032,2301,3210}`.  It is the zero-defect global
affine class, equivalently the class whose terminal diagonal set
is the full translation `V4` in the canonical `F2^2` model.

The `32` selected-affine extras are the first near-miss layer:
their selected mask is affine and their selected values are
`{11,12,15,16}`, but they have affine defect `4` rather than `0`.

## Guardrail

This is still a finite characterization inside the `236`
terminal-24 records.  It is not a theorem for all order-four
endpoint classes and it does not explain the Lo Shu side of the
meet.
