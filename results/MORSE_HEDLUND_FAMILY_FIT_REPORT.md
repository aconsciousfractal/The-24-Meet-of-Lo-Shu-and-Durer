# Morse-Hedlund / Prouhet Family-Fit Report

Status: Phase G family-fit test

## Transform Scope

- transforms checked: `2304`
- scope: optional transpose, arbitrary row permutation, arbitrary column
  permutation, and optional value complement.

## Identity Orientation

- source in family: `True`
- terminal in family: `False`
- negative mask direction in linear family: `False`
- ray in family: `False`
- source parameters: `{'a': 14, 'b': 15, 'c': 16, 'd': 13, 'k1': -4, 'k2': -8, 'magic_sum': 34}`

## Fit Counts

- source fits: `256`
- terminal fits: `0`
- direction fits: `0`
- full ray fits: `0`

## Conclusion

- source fits family: `True`
- terminal fits family: `False`
- direction fits linear family: `False`
- full Sagrada ray fits family under tested scope: `False`

The source Durer-complement square is exactly in the displayed family
in the identity orientation.  The Sagrada perturbation direction is not
in the family's linear tangent space under the tested transform scope,
so the bounded Sagrada ray is not a specialization of this family in
the tested sense.
