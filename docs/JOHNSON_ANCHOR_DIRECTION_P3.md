# Phase P3 - Anchored Johnson Direction Explanation

Phase P2 showed that Johnson profiles anchored by the fixed translation
`V4 = {0123,1032,2301,3210}` separate the exact `V4` class, the selected-affine
extras, and the outside-main records.

Phase P3 explains the exact `144` profile directionally.

The four fixed translation diagonals partition the 16 cells.  Relative to the
translation direction `W0`, a domain-affine quaterne has only three possible
coset-intersection shadows:

```text
same direction as W0        -> 4,0,0,0
line intersection with W0   -> 2,2,0,0
complementary direction     -> 1,1,1,1
```

For all `144` exact-`V4` records, the terminal affine quaternes have the same
direction inventory:

```text
same direction:       1 direction,  4 quaternes
line intersection:    5 directions, 20 quaternes
complement direction: 3 directions, 12 quaternes
non-domain-affine terminal affine quaternes: 0
```

Thus the exact anchored Johnson profile

```text
4*(4,0,0,0) + 20*(2,2,0,0) + 12*(1,1,1,1)
```

is the quotient shadow of a uniform `1+5+3` direction inventory.  The `32`
selected-affine extras and `60` outside-main records do not share this
inventory.

Guardrail: this is an O5-anchored Johnson invariant.  It is not a mask-only
Johnson invariant, and it does not explain the strong meet itself.

Artifacts:

```text
scripts/analyze_johnson_anchor_direction_p3.py
tests/test_johnson_anchor_direction_p3.py
results/johnson_anchor_direction_p3.json
results/JOHNSON_ANCHOR_DIRECTION_P3_REPORT.md
```
