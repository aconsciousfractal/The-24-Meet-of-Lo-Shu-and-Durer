# F2^4 Tesseract Report

Status: Phase F exact finite replay plus structural finite-affine lemmas

## Model

Each Durer cell is labeled by `value-1`, hence by a point of `F2^4`.
A four-cell set is treated as an affine plane exactly when the xor of
its four labels is zero.

## Linear Tesseract Coordinatization

With row and column written in high/low bits `(r0,r1)` and `(c0,c1)`,
and with `D[r,c]-1` written MSB-to-LSB as `(l0,l1,l2,l3)`, the value
labeling is the following linear map over `F2`:

```text
l0 = r1 + c0 + c1
l1 = r0 + c0 + c1
l2 = r0 + r1 + c0
l3 = r0 + r1 + c1
```

- matrix rank over `F2`: `4`
- linear automorphism: `True`
- all cells match formula: `True`
- all 24 permutation diagonals are affine planes: `True`

## One-Incidence Masks

- one-incidence masks: `8`
- all one-incidence masks affine: `True`
- terminal-24 affine masks: `['2013']`

The affine-plane property does not by itself single out Sagrada.  All
eight one-incidence masks have it; Sagrada is singled out only after
adding the Durer bounded terminal condition.

## Quaternes

- ambient four-cell sets: `1820`
- affine planes in the ambient `F2^4` cell model: `140`
- `H_34(D)` count: `86`
- `H_34(D)` affine split: `{'affine': 52, 'non_affine': 34}`
- transported `H_34` incidence-1 affine split: `{'affine': 36, 'non_affine': 14}`
- `H_24(D(10))` count: `96`
- `H_24(D(10))` affine split: `{'affine': 36, 'non_affine': 60}`
- terminal affine planes are exactly transported source-34 incidence-1 planes: `True`

## Balanced Directions

- 2-dimensional directions in `F2^4`: `35`
- direction cosets / affine planes: `140`
- direction cosets equal ambient affine planes: `True`
- balanced directions: `13`
- balanced direction cosets: `52`
- balanced cosets equal affine part of `H_34(D)`: `True`
- relation of balanced directions to Sagrada direction: `{'complementary_to_sagrada_direction': 9, 'line_intersection_with_sagrada_direction': 4}`
- incidence of balanced cosets by relation: `{'complementary_to_sagrada_direction_1': 36, 'line_intersection_with_sagrada_direction_0': 8, 'line_intersection_with_sagrada_direction_2': 8}`
- terminal affine planes equal complementary balanced cosets: `True`

Thus the source affine count is not an opaque replay: it is
`13` balanced directions times `4` cosets.  The terminal affine count
is the `9` balanced directions complementary to the Sagrada direction,
again times `4` cosets.

## Diagonal Groups

- source `D4` affine-family counts: `{'bit_swap_linear_part_translation': 4, 'identity_linear_part_translation': 4}`
- terminal `V4` affine-family counts: `{'identity_linear_part_translation': 4}`
- terminal `V4` is the translation subgroup of `F2^2`: `True`

## Guardrail

This layer strengthens the structure of the Durer/Sagrada cell, but it
does not make `24` universal.  It also does not turn `D4` or `V4` into
standard Type-A poset cones.
