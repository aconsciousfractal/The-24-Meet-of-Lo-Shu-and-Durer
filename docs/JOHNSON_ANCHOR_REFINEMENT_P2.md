# Phase P2 - Anchored Johnson Refinement

Status: second Phase-P audit complete.

## Question

Phase P1 showed that mask-only Johnson profiles are useful but too coarse:

```text
they separate 176 from outside-main;
they do not separate 144 exact-V4 from 32 selected-affine extras.
```

Phase P2 asks whether the `144/32` boundary becomes visible after adding the
O5 translation anchor:

```text
V4_translation = {0123, 1032, 2301, 3210}.
```

For each terminal quaterne `Q`, compute the sorted intersection vector:

```text
( |Q cap T_1|, |Q cap T_2|, |Q cap T_3|, |Q cap T_4| )
```

where `T_i` are the four fixed translation diagonals.

## Result

Class counts:

```text
exact_v4:     144
extra32:       32
outside_main:  60
```

Terminal set sizes:

```text
exact_v4:     4 -> 144
extra32:      2 -> 16, 4 -> 16
outside_main: 2 -> 36, 3 -> 12, 4 -> 8, 5 -> 4
```

The fixed-translation anchored Johnson profiles separate all three classes:

```text
fixed_translation_terminal_anchor_profile:
  exact_v4 signatures:    1
  extra32 signatures:     4
  outside_main signatures:14
  pairwise intersections: 0,0,0

fixed_translation_terminal_affine_anchor_profile:
  exact_v4 signatures:    1
  extra32 signatures:     2
  outside_main signatures:11
  pairwise intersections: 0,0,0
```

The uniform exact-`V4` terminal anchored profile is:

```text
(1,1,1,1) -> 16
(2,1,1,0) -> 48
(2,2,0,0) -> 20
(3,1,0,0) -> 8
(4,0,0,0) -> 4
```

The uniform exact-`V4` terminal-affine anchored profile is:

```text
(1,1,1,1) -> 12
(2,2,0,0) -> 20
(4,0,0,0) -> 4
```

## Interpretation

This is a real refinement of P1:

```text
mask-only Johnson:
  separates 176 from 60, not 144 from 32

translation-anchored Johnson:
  separates 144, 32, and 60
```

Guardrail:

```text
The separation uses the O5 fixed translation V4 anchor.
It is not a mask-only Johnson invariant.
```

So the `144/32` boundary is visible in an anchored
Johnson/association-scheme profile. This supports a clean paper remark if
we want one, but it should be described as an O5-anchored refinement.

## Artifacts

```text
scripts/analyze_johnson_anchor_refinement_p2.py
tests/test_johnson_anchor_refinement_p2.py
results/johnson_anchor_refinement_p2.json
results/JOHNSON_ANCHOR_REFINEMENT_P2_REPORT.md
```
