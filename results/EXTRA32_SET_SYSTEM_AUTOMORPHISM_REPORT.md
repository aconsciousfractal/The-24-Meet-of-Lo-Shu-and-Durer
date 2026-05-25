# Extra-32 Set-System Automorphism Audit

Status: Phase H focused audit of the 32 structured extras

## Summary

- extra pairs: `32`
- automorphism tuple order: `lines_plus_mask, source, terminal, combined`
- automorphism tuple counts: `{'(1, 1, 1, 1)': 32}`

## Terminal-Set Classes

### two_diagonal_pair

`{'pair_count': 16, 'mask_counts': {'1320': 1, '2013': 4, '2130': 2, '3021': 5, '3102': 4}, 'source_diagonal_size_counts': {'2': 12, '4': 4}, 'automorphism_tuple_counts': {'(1, 1, 1, 1)': 16}, 'complement_fixed_count': 8}`

### v4_like_0213

`{'pair_count': 8, 'mask_counts': {'1320': 2, '2130': 1, '3021': 2, '3102': 3}, 'source_diagonal_size_counts': {'4': 8}, 'automorphism_tuple_counts': {'(1, 1, 1, 1)': 8}, 'complement_fixed_count': 0}`

### v4_like_1302

`{'pair_count': 8, 'mask_counts': {'2013': 4, '2130': 2, '3021': 2}, 'source_diagonal_size_counts': {'4': 8}, 'automorphism_tuple_counts': {'(1, 1, 1, 1)': 8}, 'complement_fixed_count': 0}`

## Interpretation

This audit tests whether the 32 structured extras are separated by a
small colored set-system automorphism signature.  The result should be
read together with the terminal-set and source-diagonal-size split.

## Guardrail

This is still a finite fingerprint audit.  It does not prove that the
extras form a natural family outside the tested invariants.
