# F2 Orientation Stability

Status: Phase F closing micro-audit

## Purpose

This note closes the main Phase-F guardrail: the affine cell-value criterion

```text
(row,column) -> Q[row,column] - 1 in F2^4
```

was first computed on lexicographically canonical essential representatives.
The audit checks whether the criterion is an artifact of that chosen
orientation.

The replay artifacts are:

```text
scripts/analyze_f2_orientation_stability.py
tests/test_f2_orientation_stability.py
results/f2_orientation_stability.json
results/F2_ORIENTATION_STABILITY_REPORT.md
```

## Result

Every one of the 8 square symmetries acts as an affine automorphism on the
row/column bit domain.  Consequently, affine cell-value labeling is stable
across each full `D4` orientation orbit.

Across the 880 essential representatives:

```text
orientation affine-count distribution:
  0 affine orientations: 448 squares
  8 affine orientations: 432 squares

unstable orientation orbits: 0
```

Equivalently, across the 7040 raw oriented/reflected squares:

```text
affine cell-value labeling:     3456
non-affine cell-value labeling: 3584
total:                          7040
```

The criterion is also stable under value complement:

```text
direct value-complement stable count:    880
canonical value-complement stable count: 880
```

Finally, the terminal-24 pair-level `F2^4` profiles are stable under jointly
transforming the square and selected mask through all 8 square symmetries:

```text
terminal-24 pairs checked: 236
unstable pair profiles:   0
```

## Interpretation

The phrase `exact canonical V4` is still orientation language: it names the
terminal diagonal set in the chosen canonical representative.  But the
underlying affine cell-value criterion is not a canonicalization artifact. It
is invariant across the full square-symmetry orbit and under value complement.

This is enough to close Phase F cleanly:

```text
F2^4 affine cell-value structure is orientation-stable.
F2^4 exact-V4 wording remains canonical-representative wording.
```

## Guardrail

Do not claim that the literal word `V4 = {0123,1032,2301,3210}` is
orientation-free.  Under square symmetries, permutation-diagonal sets are
renamed.  The stable object is the affine cell-value criterion and the
transport profile after transforming the mask along with the square.
