# F2^4 Tesseract Layer

Status: Phase F exact finite replay plus structural lemma upgrade

## Purpose

This note audits the external-agent proposal that the Durer/Sagrada cell has
an intrinsic `F2^4` layer.  The model follows the Durer-tesseract viewpoint:
label each Durer cell by its value minus one, hence by a point of
`{0,...,15}=F2^4`.

A four-cell set is an affine plane in this cell model exactly when the xor of
its four labels is zero.

The second audit pass verifies the stronger claim suggested by the external
agent: the Durer value-minus-one labeling is not merely a convenient
enumeration of `F2^4`; in the current orientation it is a linear automorphism
from row/column bits to value bits.  The exact displayed formula depends on
bit order, so this note fixes the convention used by the certificate script.

The replay artifact is:

```text
results/f2_tesseract_analysis.json
results/F2_TESSERACT_REPORT.md
scripts/analyze_f2_tesseract.py
tests/test_f2_tesseract.py
```

## Verified Claims

### Linear Tesseract Coordinatization

Write the row and column indices in high/low bits:

```text
r = (r0,r1)
c = (c0,c1)
```

Write `D[r,c]-1` in MSB-to-LSB bits:

```text
(l0,l1,l2,l3).
```

Then the certificate verifies the linear formula over `F2`:

```text
l0 = r1 + c0 + c1
l1 = r0 + c0 + c1
l2 = r0 + r1 + c0
l3 = r0 + r1 + c1
```

The associated `4 x 4` matrix has rank `4` over `F2`, so this is an
automorphism of `F2^4`.  This also explains why all `24` permutation
diagonals are affine planes: the graph of any permutation of the four points
of `F2^2` is affine, since `AGL(2,2) ~= S4`, and the Durer value labeling
transports those graphs linearly into `F2^4`.

### One-Incidence Masks

There are `8` one-incidence masks.  All `8` are affine planes in the
`F2^4` cell model.

Therefore the affine-plane property alone does not select the Sagrada mask.
The Sagrada mask `2013` is selected only after adding the Durer bounded
terminal condition:

```text
terminal-24 affine-plane masks: 2013
```

This is the right refinement of the external-agent statement:

```text
affine plane + one-incidence + Durer terminal sum 24
```

not simply:

```text
affine plane
```

### Durer Quaternes

In the ambient `F2^4` cell model there are:

```text
four-cell sets: 1820
affine planes: 140
```

The Durer `34`-quaternes split as:

```text
|H_34(D)| = 86
affine / non-affine = 52 / 34
```

Against the Sagrada mask, the source `H_34(D)` split by incidence and
affineness is:

```text
incidence 0:  8 affine, 11 non-affine
incidence 1: 36 affine, 14 non-affine
incidence 2:  8 affine,  9 non-affine
```

Thus the 50 source quaternes transported from `34` to `24` split as:

```text
36 affine + 14 non-affine
```

The structural explanation is now certified.  There are `35` two-dimensional
directions in `F2^4`, each with `4` affine cosets, hence `140` affine planes.
Among those directions, exactly `13` are balanced, meaning no coordinate bit
is constant on the direction.  For the integer weight

```text
w(l0,l1,l2,l3) = 1 + 8l0 + 4l1 + 2l2 + l3
```

with the corresponding bit convention, the cosets of exactly these balanced
directions have Durer source sum `34`.  Therefore:

```text
52 affine H_34 quaternes = 13 balanced directions x 4 cosets.
```

### Terminal `H_24(D(10))`

The terminal hypergraph has:

```text
|H_24(D(10))| = 96
affine / non-affine = 36 / 60
```

The finer decomposition is:

```text
source 24, incidence 0: 25 non-affine
source 34, incidence 1: 36 affine + 14 non-affine
source 44, incidence 2: 21 non-affine
```

So the terminal affine planes are exactly the transported source-34
incidence-1 affine planes.  This is a new useful sharpening beyond the
external analysis: the affine part of `H_24(D(10))` is pure transport, while
the extra `25+21` terminal quaternes are non-affine in this model.

The refined direction-level explanation is:

```text
Sagrada direction W = {0,1,4,5}
balanced directions complementary to W: 9
balanced directions meeting W in a line: 4
```

The `9` complementary balanced directions contribute one Sagrada point in
each coset, hence:

```text
36 terminal affine planes = 9 complementary balanced directions x 4 cosets.
```

The remaining `4` balanced directions meet the Sagrada direction in a line,
and their cosets split as:

```text
8 incidence-0 cosets
8 incidence-2 cosets
```

So the pure transport statement is no longer only a replay count; it is a
finite-affine-geometry fact.

### Diagonal Break

The Phase-D break

```text
D4 -> V4
```

has a clean `F2^2` affine-map reading on the row/column index set
`{0,1,2,3}=F2^2`.

The source `D4` diagonals are the union of two affine-map families:

```text
4 translations:          x -> x + b
4 bit-swap translations: x -> swap(x) + b
```

The terminal `V4` diagonals are exactly the translation subgroup:

```text
V4 = {x -> x + b : b in F2^2}
```

This gives a stronger algebraic wording for the Phase-D finite fact without
forcing `D4` or `V4` into Type-A poset cones.

## What This Adds

The `F2^4` layer explains why the Durer/Sagrada cell is more structured than a
plain terminal-24 endpoint:

- The Durer value-minus-one labeling is a linear automorphism of `F2^4`.
- All 24 permutation diagonals are affine planes in this model.
- Sagrada is an affine-plane mask, but so are all one-incidence masks.
- The real selection is the bounded terminal condition inside Durer.
- The 86 Durer quaternes contain a large affine-plane sublayer,
  `52 = 13 x 4`.
- The terminal affine `24`-quaternes are exactly the transported affine part,
  `36 = 9 x 4`.
- The diagonal symmetry break is a translation-subgroup projection.

This turns the next research branch from "more counting" into a concrete
geometry problem:

```text
affine planes in F2^4
transport along the Sagrada ray
terminal H_24 hypergraph structure
D4/V4 as affine-map families on F2^2
```

## Guardrails

Do not claim:

- `24` is universal.
- the affine-plane property alone selects Sagrada.
- all `86` Durer quaternes are affine planes.
- the `F2^4` layer turns `D4` or `V4` into standard Type-A poset cones.
- this layer gives a direct theorem on the Lo Shu side.
- the displayed linear formula is bit-order-free; only the automorphism claim
  is invariant under convention changes.

The correct status is narrower and stronger: this is a Durer-side structural
layer that enriches the already certified strong meet.

## Next Questions

1. Compute automorphism groups of `H_34(D)` and `H_24(D(10))` with affine and
   non-affine quaternes colored separately.
2. Compare the 52 affine source quaternes with Sudbery's tesseract families
   and the Ollerenshaw-Bondi/Frenicle part-sum language.
3. Extend the structural direction counts (`13 x 4`, `9 x 4`) to the
   associated/complement-fixed and panmagic/most-perfect control branches.

The 236-pair and exact canonical `V4` subclass checks are now recorded in
`docs/ORDER4_F2_EXTENSION.md`.

The colored automorphism audit is recorded in
`docs/F2_HYPERGRAPH_AUTOMORPHISMS.md`.

The family-control and orientation-stability closure notes are recorded in
`docs/F2_FAMILY_CONTROLS.md` and `docs/F2_ORIENTATION_STABILITY.md`.
