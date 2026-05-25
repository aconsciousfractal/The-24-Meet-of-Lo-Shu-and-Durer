# Kernel V4 Versus Terminal Translation V4

Status: Phase O5 follow-up audit, intentionally outside the paper

## Question

Does the terminal translation `V4` coincide, through the global
cell-value affine map, with the kernel of the value-bit action
`S4 -> S3` on coordinate-axis matchings?

## Verdict

No: the direct identification is false in the certified exact-V4 affine
class.

## Evidence

- terminal affine records: `144`
- value-bit kernel size: `4`
- selected-plane kernel stabilizer sizes: `{'2': 144}`
- selected-plane kernel orbit sizes: `{'2': 144}`
- kernel orbit equals terminal translation image planes: `{'False': 144}`
- kernel orbit intersection with terminal image planes: `{'0': 144}`

Thus the value-bit kernel does not produce the terminal translation
planes directly.

## Positive Structure

- terminal translation image plane counts: `{'4': 144}`
- terminal translation image direction counts: `{'1': 144}`
- terminal translation image directions balanced: `{'True': 144}`
- selected-plane intersection patterns: `{'(1, 1, 1, 1)': 144}`

For every record, the terminal translation diagonals become four cosets
of one balanced value direction, and each coset intersects the selected
terminal plane in exactly one point.  This is the real structural
relationship behind the terminal full-translation `V4`.

## Guardrail

Do not claim that the two `V4` objects coincide.  They live in related
but different actions: value-bit symmetries on coordinate matchings
versus permutation diagonals in the row/column domain.
