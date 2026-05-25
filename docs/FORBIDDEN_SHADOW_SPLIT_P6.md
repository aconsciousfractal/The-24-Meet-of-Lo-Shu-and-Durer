# Phase P6 - Forbidden-Shadow Split

Phase P6 is a small follow-up to Phase P5.

## Linear Lemma

Let `V = F2^4`, let `W0` be the two-dimensional direction of the fixed
translation `V4` spread, and let `A = a + L` be a domain-affine plane.

Under the quotient map

```text
pi: V -> V / W0
```

the image `pi(A)` is an affine subspace of dimension `r = 0, 1, 2`.
Every nonempty fiber of `pi|A` has the same size `2^(2-r)`.  Therefore the
sorted intersection profile of `A` with the four spread blocks can only be:

```text
r = 0: 4,0,0,0
r = 1: 2,2,0,0
r = 2: 1,1,1,1
```

The shadow `2,1,1,0` is impossible for a domain-affine plane.  It is a
quotient-affinity obstruction, not just an empirical fingerprint.

## Extra-32 Split

The P5 split

```text
F_2110 = 12: 16 records
F_2110 = 16: 16 records
```

matches the older terminal-set split exactly:

```text
F_2110 = 12
  <=> terminal_set_class = two_diagonal_pair
  <=> terminal set is the translation subset {0123,3210}

F_2110 = 16
  <=> terminal_set_class in {v4_like_0213, v4_like_1302}
  <=> terminal set has two translations plus two non-translation diagonals
```

Thus the `32` extras are now organized as:

```text
16 two-diagonal translation-subset extras:
  F_1111=16, F_2200=8, F_4000=0, F_2110=12

8 v4_like_0213 extras:
  F_1111=12, F_2200=8, F_4000=0, F_2110=16

8 v4_like_1302 extras:
  F_1111=12, F_2200=8, F_4000=0, F_2110=16
```

## Reading

The obstruction `F_2110 > 0` separates the `32` extras from the exact `144`
inside the main `176`.  Phase P6 adds that the internal `12/16` split is not
a new independent invariant; it is the quotient-shadow expression of the
terminal diagonal-set split already present in the extra-32 audits.

Artifacts:

```text
scripts/analyze_forbidden_shadow_split_p6.py
tests/test_forbidden_shadow_split_p6.py
results/forbidden_shadow_split_p6.json
results/FORBIDDEN_SHADOW_SPLIT_P6_REPORT.md
```
