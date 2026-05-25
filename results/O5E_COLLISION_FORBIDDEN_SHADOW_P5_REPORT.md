# Phase P5 Collision And Forbidden-Shadow Audit

## O5e Collision-Matching Table

```text
fiber_count=144
direction_pair_count=36
distinct_point_map_distribution={'16': 32, '20': 16, '24': 96}
collision_edge_distribution={'0': 96, '4': 16, '8': 32}
max_multiplicity_distribution={'1': 96, '2': 48}
matching_collision_graph_holds=True
direction_pair_classifier_holds=True
```

Direction-pair table:

```text
U=0,1,2,3 W=0,5,10,15 fibers=4 maps=24 edges=0
U=0,1,2,3 W=0,5,11,14 fibers=4 maps=24 edges=0
U=0,1,2,3 W=0,6,11,13 fibers=4 maps=24 edges=0
U=0,1,2,3 W=0,6,9,15 fibers=4 maps=24 edges=0
U=0,1,2,3 W=0,7,10,13 fibers=4 maps=24 edges=0
U=0,1,2,3 W=0,7,9,14 fibers=4 maps=24 edges=0
U=0,1,4,5 W=0,3,12,15 fibers=4 maps=16 edges=8
U=0,1,4,5 W=0,3,13,14 fibers=4 maps=16 edges=8
U=0,1,4,5 W=0,6,11,13 fibers=4 maps=24 edges=0
U=0,1,4,5 W=0,6,9,15 fibers=4 maps=24 edges=0
U=0,1,4,5 W=0,7,11,12 fibers=4 maps=24 edges=0
U=0,1,4,5 W=0,7,9,14 fibers=4 maps=24 edges=0
U=0,1,8,9 W=0,3,12,15 fibers=4 maps=16 edges=8
U=0,1,8,9 W=0,3,13,14 fibers=4 maps=16 edges=8
U=0,1,8,9 W=0,5,10,15 fibers=4 maps=20 edges=4
U=0,1,8,9 W=0,5,11,14 fibers=4 maps=20 edges=4
U=0,1,8,9 W=0,7,10,13 fibers=4 maps=24 edges=0
U=0,1,8,9 W=0,7,11,12 fibers=4 maps=24 edges=0
U=0,2,4,6 W=0,3,12,15 fibers=4 maps=16 edges=8
U=0,2,4,6 W=0,3,13,14 fibers=4 maps=16 edges=8
U=0,2,4,6 W=0,5,10,15 fibers=4 maps=20 edges=4
U=0,2,4,6 W=0,5,11,14 fibers=4 maps=20 edges=4
U=0,2,4,6 W=0,7,10,13 fibers=4 maps=24 edges=0
U=0,2,4,6 W=0,7,11,12 fibers=4 maps=24 edges=0
U=0,2,8,10 W=0,3,12,15 fibers=4 maps=16 edges=8
U=0,2,8,10 W=0,3,13,14 fibers=4 maps=16 edges=8
U=0,2,8,10 W=0,6,11,13 fibers=4 maps=24 edges=0
U=0,2,8,10 W=0,6,9,15 fibers=4 maps=24 edges=0
U=0,2,8,10 W=0,7,11,12 fibers=4 maps=24 edges=0
U=0,2,8,10 W=0,7,9,14 fibers=4 maps=24 edges=0
U=0,4,8,12 W=0,5,10,15 fibers=4 maps=24 edges=0
U=0,4,8,12 W=0,5,11,14 fibers=4 maps=24 edges=0
U=0,4,8,12 W=0,6,11,13 fibers=4 maps=24 edges=0
U=0,4,8,12 W=0,6,9,15 fibers=4 maps=24 edges=0
U=0,4,8,12 W=0,7,10,13 fibers=4 maps=24 edges=0
U=0,4,8,12 W=0,7,9,14 fibers=4 maps=24 edges=0
```

## Forbidden Quotient-Shadow Obstruction

Domain-affine planes relative to the fixed translation spread have
only the quotient shadows `4,0,0,0`, `2,2,0,0`, and `1,1,1,1`:

```text
ambient_domain_affine_plane_count=140
ambient_domain_affine_shadow_profile={'1,1,1,1': 64, '2,2,0,0': 72, '4,0,0,0': 4}
ambient_has_forbidden_2110=False
```

Inside the main `176 = 144 + 32` selected-affine signature:

```text
exact_v4 count=144 F1111=12 F2200=20 F4000=4 F2110=0 non_domain=0
extra32 count=16 F1111=12 F2200=8 F4000=0 F2110=16 non_domain=16
extra32 count=16 F1111=16 F2200=8 F4000=0 F2110=12 non_domain=12
exact_v4_iff_F2110_zero=True
F2110_equals_non_domain=True
```

## Interpretation

The O5e collision graph is always a matching: no point-map has
multiplicity above `2`.  The three cases have `0`, `4`, or `8`
collision edges, and the direction pair `(U,W)` classifies which
case occurs.

The `32` extras are no longer just unexplained near-misses.  Within
the main `176` signature, exact-`V4` is equivalent to zero
forbidden-shadow mass `F_2110=0`; the `32` extras are exactly the
positive forbidden-shadow records, split as `F_2110=12` and
`F_2110=16`.
