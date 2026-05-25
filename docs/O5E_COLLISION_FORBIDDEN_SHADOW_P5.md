# Phase P5 - O5e Collisions And Forbidden Shadows

Phase P5 closes two follow-up questions.

## O5e Collision-Matching Lemma

Each `(P,W)` fiber in the globally affine square-mask layer has `24`
records.  The point-map collision graph is always a matching:

```text
distinct point maps: 24 -> 96 fibers, 0 collision edges
distinct point maps: 20 -> 16 fibers, 4 collision edges
distinct point maps: 16 -> 32 fibers, 8 collision edges
```

No point map has multiplicity above `2`.  The direction pair

```text
(selected_plane_direction, translation_direction)
```

classifies the collision type with no ambiguity across the `36` direction
pairs.

## Forbidden Quotient-Shadow Obstruction

Let the fixed translation `V4` spread partition the 16 cells into four
blocks.  A domain-affine plane has quotient image of dimension `0`, `1`, or
`2` after quotienting by the fixed translation direction.  Therefore its
sorted block shadow can only be:

```text
4,0,0,0
2,2,0,0
1,1,1,1
```

The ambient `140` domain-affine planes have profile:

```text
1,1,1,1 -> 64
2,2,0,0 -> 72
4,0,0,0 -> 4
2,1,1,0 -> 0
```

Thus `2,1,1,0` is a forbidden quotient shadow for domain-affine planes.

Inside the main `176 = 144 + 32` selected-affine signature:

```text
exact_v4:
  count=144
  F_1111=12, F_2200=20, F_4000=4, F_2110=0

extra32 type A:
  count=16
  F_1111=12, F_2200=8, F_4000=0, F_2110=16

extra32 type B:
  count=16
  F_1111=16, F_2200=8, F_4000=0, F_2110=12
```

Equivalently, inside the main `176`:

```text
exact_v4 <=> F_2110 = 0
extra32  <=> F_2110 > 0
F_2110 = non-domain-affine terminal-affine count
```

This makes the `32` extras positive defect objects: they preserve much of
the terminal-affine code profile, but introduce forbidden quotient-shadow
mass relative to the fixed translation spread.

Artifacts:

```text
scripts/analyze_o5e_collision_and_forbidden_shadow_p5.py
tests/test_o5e_collision_forbidden_shadow_p5.py
results/o5e_collision_forbidden_shadow_p5.json
results/O5E_COLLISION_FORBIDDEN_SHADOW_P5_REPORT.md
```
