# Affine Normal Count Derivation

Status: Phase O4 linear-algebra derivation

## Purpose

Phase O2/O3 reduced the `144` exact-V4 story to the globally affine
normal order-4 layer.  This audit derives the total `432` count without
enumerating the `880` essential representatives.

## Linear-Algebra Count

- 2-dimensional subspaces of `F2^4`: `35`
- balanced directions: `13`
- ordered pairwise-complementary balanced triples: `36`
- maps per image triple: `6`
- good linear parts: `216`
- complementarity graph triangles: `6`

The three relevant domain directions are row, column, and diagonal
direction.  The main and anti-diagonal are parallel affine planes, so
they share the same direction.

A linear part is good exactly when those three directions map to balanced
directions in value space.  The count is:

```text
36 balanced image triples x 6 maps per triple = 216 linear parts
```

Equivalently, the complementarity graph on the 13 balanced directions
has 6 triangles, and each triangle has 6 orderings.

## From Linear Parts To Essential Representatives

Offsets are free: adding an affine offset in value space translates all
labels and preserves the balanced-direction line sums.

```text
216 linear parts x 16 offsets = 3456 raw affine normal squares
3456 / 8 square symmetries = 432 essential representatives
```

The division by `8` is valid for normal squares because all entries are
distinct, so no nontrivial square symmetry can fix a square cellwise.
The same square-symmetry group acts freely and transitively on the
eight admissible one-incidence masks:

```text
{'admissible_mask_count': 8, 'square_symmetry_count': 8, 'orbit_count': 1, 'orbit_size_distribution': {'8': 8}, 'stabilizer_size_distribution': {'1': 8}, 'is_free_transitive': True}
```

## Link To The 144 Class

Combining this with Phase O3 gives:

```text
432 globally affine essential representatives
  = 3 coordinate-axis matchings x 144

432 x 8 admissible masks
  = 3456 affine square-mask pairs
  = 24 selected value planes x 144
```

The terminal-24 exact-V4 class is the high value plane
`{11,12,15,16}`.

## Guardrail

This is a finite F2-linear count, not a classification theorem for non-affine order-4 magic squares or for higher orders.
