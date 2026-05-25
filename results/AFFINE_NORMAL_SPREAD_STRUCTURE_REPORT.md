# Affine Normal Spread Structure Audit

Status: Phase O3 spread/matching explanation

## Purpose

Phase O2 found the finite uniformity

```text
3456 = 24 selected value planes x 144 pairs.
```

This audit explains the first structural layer behind that uniformity.

## Square-Level Structure

- globally affine representatives: `432`
- affine square-mask pairs: `3456`
- selected value planes: `24`
- per-square selected plane counts: `{'8': 432}`
- per-square selected direction counts: `{'2': 432}`

Each globally affine representative sends the eight admissible masks to
exactly eight selected value planes: all four cosets of one coordinate
2-plane direction and all four cosets of a complementary coordinate
2-plane direction.

## Coordinate-Axis Matchings

- matchings: `3`
- matching distribution: `{'1,2 | 4,8': 144, '1,4 | 2,8': 144, '1,8 | 2,4': 144}`
- plane-set count distribution: `{'144': 3}`

The three matchings are the three partitions of the four coordinate axes
into two unordered pairs.

## Value-Bit Symmetry

- value-bit permutations tested: `24`
- preserving the affine normal layer: `24`
- induced matching actions: `6`
- action preimage distribution: `{'4': 6}`
- matching stabilizer sizes: `{'1,2 | 4,8': 8, '1,4 | 2,8': 8, '1,8 | 2,4': 8}`

All `24` permutations of the four value bits preserve the globally
affine normal layer.  Their induced action on the three coordinate-axis
matchings has `6` actions, each with `4` preimages.  Equivalently, this
is the natural `S4 -> S3` action on the three perfect matchings of four
axes.  Each matching has stabilizer size `8`, hence the three matching
classes have equal size.

## Matching Details

### `1,2 | 4,8`

- square count: `144`
- selected planes: `8`
- selected plane count distribution: `{'144': 8}`
- endpoint distribution: `{'22': 144, '26': 144, '30': 144, '31': 144, '32': 144, '33': 144, '34': 288}`

- `1,2,3,4`: `144`
- `1,5,9,13`: `144`
- `13,14,15,16`: `144`
- `2,6,10,14`: `144`
- `3,7,11,15`: `144`
- `4,8,12,16`: `144`
- `5,6,7,8`: `144`
- `9,10,11,12`: `144`

### `1,4 | 2,8`

- square count: `144`
- selected planes: `8`
- selected plane count distribution: `{'144': 8}`
- endpoint distribution: `{'24': 144, '26': 144, '29': 144, '30': 144, '32': 144, '33': 144, '34': 288}`

- `1,2,5,6`: `144`
- `1,3,9,11`: `144`
- `11,12,15,16`: `144`
- `2,4,10,12`: `144`
- `3,4,7,8`: `144`
- `5,7,13,15`: `144`
- `6,8,14,16`: `144`
- `9,10,13,14`: `144`

### `1,8 | 2,4`

- square count: `144`
- selected planes: `8`
- selected plane count distribution: `{'144': 8}`
- endpoint distribution: `{'25': 144, '26': 144, '28': 144, '30': 144, '32': 144, '33': 144, '34': 288}`

- `1,2,9,10`: `144`
- `1,3,5,7`: `144`
- `10,12,14,16`: `144`
- `2,4,6,8`: `144`
- `3,4,11,12`: `144`
- `5,6,13,14`: `144`
- `7,8,15,16`: `144`
- `9,11,13,15`: `144`

## Interpretation

The number `144` is explained at the first structural level by two
nested facts:

```text
432 affine representatives = 3 coordinate-axis matchings x 144
each affine representative contributes 8 planes = 2 directions x 4 cosets
therefore 3456 affine pairs = 24 planes x 144 pairs
```

The terminal-24 exact-V4 class is the high selected value plane
`{11,12,15,16}` inside one of these three matchings.

## Remaining Conceptual Gap

The group action explains the equality of the three matching classes.
The remaining proof target is narrower: derive the total `432` count
of globally affine essential representatives without enumerating the
full order-4 normal-square atlas.
