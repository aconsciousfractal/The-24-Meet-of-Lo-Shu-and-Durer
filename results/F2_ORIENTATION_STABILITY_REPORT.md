# F2 Orientation Stability Report

Status: Phase F closing micro-audit

## Summary

- all D4 domain transforms affine automorphisms: `True`
- essential squares: `880`
- orientation affine-count distribution: `{'0': 448, '8': 432}`
- affine flag stable for all 880 D4 orbits: `True`
- raw oriented affine/non-affine counts: `3456` / `3584`
- direct value-complement stable count: `880`
- canonical value-complement stable count: `880`
- terminal-24 pairs checked: `236`
- terminal-24 D4 pair profiles stable: `True`

## Interpretation

The affine cell-value criterion is stable under the 8 square symmetries
used for essential canonicalization, because those symmetries act as
affine automorphisms on the row/column bit domain.  It is also stable
under value complement, both directly and after canonicalizing the
complement.

The fixed phrase `exact canonical V4` remains orientation wording: it
names the canonical representative's terminal diagonal set.  The
underlying affine cell-value criterion itself is orientation stable.
