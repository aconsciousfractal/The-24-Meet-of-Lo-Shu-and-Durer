# Affine Normal Spread Structure

Status: Phase O3 conceptualization pass

## Purpose

Phase O2 showed that the `144` exact-`V4` class is one selected value plane
inside the globally affine normal order-4 layer:

```text
432 globally affine representatives x 8 masks = 3456
3456 = 24 selected value planes x 144 pairs
```

Phase O3 explains the first structural reason for this uniformity.

Replay artifacts:

```text
scripts/analyze_affine_normal_spread_structure.py
tests/test_affine_normal_spread_structure.py
results/affine_normal_spread_structure.json
results/AFFINE_NORMAL_SPREAD_STRUCTURE_REPORT.md
```

## Result

Every globally affine essential representative sends the eight admissible
one-incidence masks to exactly:

```text
8 selected value planes = 2 coordinate directions x 4 cosets.
```

The two directions form one of the three matchings of the four coordinate
axes:

```text
1,2 | 4,8
1,4 | 2,8
1,8 | 2,4
```

The `432` globally affine representatives split evenly:

```text
1,2 | 4,8: 144 squares
1,4 | 2,8: 144 squares
1,8 | 2,4: 144 squares
```

Therefore each of the `24` selected value planes appears in exactly `144`
square-mask pairs.

## Value-Bit Symmetry

The equal `144,144,144` split is not just a numerical coincidence.  The `24`
permutations of the four value bits preserve the globally affine normal
layer.  Their induced action on the three coordinate-axis matchings has:

```text
6 induced matching actions
4 value-bit permutations above each action
matching stabilizer size 8
```

This is the natural quotient action:

```text
S4 on four value-coordinate axes
  -> S3 on the three perfect matchings of those axes.
```

Since this action is transitive on the three matchings and preserves the
globally affine normal layer, the three matching classes have equal size.
The finite replay then gives:

```text
432 / 3 = 144.
```

## Terminal-24 Placement

The terminal-24 exact-`V4` class is the high selected value plane inside the
matching:

```text
1,4 | 2,8
```

namely:

```text
{11,12,15,16}: 144 pairs
```

Those `144` pairs have full translation terminal `V4`.

## Interpretation

The current best explanation of `144` is now:

```text
432 affine representatives
  = 3 coordinate-axis matchings x 144 representatives

each representative contributes
  8 selected planes = 2 directions x 4 cosets

therefore
  3456 affine square-mask pairs = 24 selected planes x 144 pairs
```

This is stronger than a flat terminal-24 atlas count.  It shows that the
terminal-24 class is one plane in a uniform affine-spread layer.

## Closure By Phase O4

The group action explains the equal split among the three matchings.  Phase
O4 then closes the remaining total-count gap by deriving:

```text
216 good linear parts x 16 offsets = 3456 raw affine normal squares
3456 / 8 square symmetries = 432 essential affine representatives
```

Thus the `144` story is complete at the finite `F2^4` linear-algebra level.
