# Extra-32 Post-J2 Audit

Status: Phase K1 targeted invariant audit

## Scope

This audit focuses only on the `32` selected-mask-affine extras left
after the Phase J2 mechanism audit.  It crosses three targeted
invariants: affine-interpolation mismatch support, the existing
small-move Markov graph, and the finite Hilbert-style decompositions.

It deliberately does not rerun the full project suite.

## Summary

- extra pairs: `32`
- terminal-set class distribution: `{'two_diagonal_pair': 16, 'v4_like_0213': 8, 'v4_like_1302': 8}`
- affine mismatch support distribution: `{"('r1c1', 'r1c2', 'r3c1', 'r3c2')": 9, "('r1c1', 'r1c3', 'r2c1', 'r2c3')": 7, "('r1c2', 'r1c3', 'r2c2', 'r2c3')": 9, "('r2c1', 'r2c2', 'r3c1', 'r3c2')": 7}`
- mismatch/mask intersection distribution: `{'0': 22, '2': 10}`
- mismatch support equals selected mask: `0`
- Hilbert min atom-count distribution: `{'12': 4, '14': 8, '16': 4, '18': 12, '20': 4}`
- Markov degree distribution: `{'0': 12, '1': 20}`
- Markov component profiles: `{'exact_v4:4,main_extra:2,outside_main:2': 4, 'main_extra:1': 12, 'main_extra:1,outside_main:1': 10, 'main_extra:2': 6}`

## By Terminal-Set Class

### two_diagonal_pair

- count: `16`
- source diagonal size distribution: `{'2': 12, '4': 4}`
- complement-fixed distribution: `{'False': 8, 'True': 8}`
- mismatch support distribution: `{"('r1c1', 'r1c2', 'r3c1', 'r3c2')": 4, "('r1c1', 'r1c3', 'r2c1', 'r2c3')": 4, "('r1c2', 'r1c3', 'r2c2', 'r2c3')": 5, "('r2c1', 'r2c2', 'r3c1', 'r3c2')": 3}`
- mismatch/mask intersection distribution: `{'0': 10, '2': 6}`
- Hilbert min atom-count distribution: `{'14': 4, '18': 12}`
- Hilbert support-size distribution: `{'5': 3, '6': 4, '7': 3, '8': 6}`
- Markov degree distribution: `{'0': 10, '1': 6}`
- Markov component profiles: `{'main_extra:1': 10, 'main_extra:1,outside_main:1': 6}`

### v4_like_0213

- count: `8`
- source diagonal size distribution: `{'4': 8}`
- complement-fixed distribution: `{'False': 8}`
- mismatch support distribution: `{"('r1c1', 'r1c2', 'r3c1', 'r3c2')": 3, "('r1c1', 'r1c3', 'r2c1', 'r2c3')": 1, "('r1c2', 'r1c3', 'r2c2', 'r2c3')": 2, "('r2c1', 'r2c2', 'r3c1', 'r3c2')": 2}`
- mismatch/mask intersection distribution: `{'0': 6, '2': 2}`
- Hilbert min atom-count distribution: `{'14': 4, '20': 4}`
- Hilbert support-size distribution: `{'5': 2, '6': 4, '7': 2}`
- Markov degree distribution: `{'0': 1, '1': 7}`
- Markov component profiles: `{'main_extra:1': 1, 'main_extra:1,outside_main:1': 4, 'main_extra:2': 3}`

### v4_like_1302

- count: `8`
- source diagonal size distribution: `{'4': 8}`
- complement-fixed distribution: `{'False': 8}`
- mismatch support distribution: `{"('r1c1', 'r1c2', 'r3c1', 'r3c2')": 2, "('r1c1', 'r1c3', 'r2c1', 'r2c3')": 2, "('r1c2', 'r1c3', 'r2c2', 'r2c3')": 2, "('r2c1', 'r2c2', 'r3c1', 'r3c2')": 2}`
- mismatch/mask intersection distribution: `{'0': 6, '2': 2}`
- Hilbert min atom-count distribution: `{'12': 4, '16': 4}`
- Hilbert support-size distribution: `{'5': 1, '6': 3, '7': 2, '8': 2}`
- Markov degree distribution: `{'0': 1, '1': 7}`
- Markov component profiles: `{'exact_v4:4,main_extra:2,outside_main:2': 4, 'main_extra:1': 1, 'main_extra:2': 3}`

## Reading

The three tested invariants refine the extras but do not collapse them
to a single conceptual family.  The affine defect is uniform in size
but not in support; the Markov graph separates isolated, paired, and
mixed-component cases; the finite Hilbert profiles split the extras
further without matching the terminal-set classes exactly.

This supports the Phase K stop rule: unless a stronger invariant is
found, the `32` extras should remain a controlled frontier rather
than being promoted to a central theorem.
