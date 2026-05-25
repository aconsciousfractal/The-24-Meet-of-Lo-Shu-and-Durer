# Phase P6 Forbidden-Shadow Split

## Quotient-Shadow Lemma

For a domain-affine plane in `F2^4`, quotienting by the fixed
translation spread direction gives an affine subspace of dimension
`0`, `1`, or `2`.  Therefore the sorted block shadows are only:

```text
4,0,0,0
2,2,0,0
1,1,1,1
```

The profile `2,1,1,0` is forbidden because the nonempty quotient
fibers of an affine plane all have equal size.

## Extra-32 Split

```text
extra32_count=32
F_2110_distribution={'12': 16, '16': 16}
F_2110_by_terminal_set_class={'12': {'two_diagonal_pair': 16}, '16': {'v4_like_0213': 8, 'v4_like_1302': 8}}
F_2110_by_translation_subset={'12': {'True': 16}, '16': {'False': 16}}
```

Terminal profiles:

```text
count=16 F2110=12 class=two_diagonal_pair set=0123,3210 translation_subset=True linear_parts={'(2, 1)': 2} example={'square_index': 5, 'mask': '3021'}
count=8 F2110=16 class=v4_like_0213 set=0123,0213,3120,3210 translation_subset=False linear_parts={'(1, 2)': 2, '(2, 1)': 2} example={'square_index': 238, 'mask': '3102'}
count=8 F2110=16 class=v4_like_1302 set=0123,1302,2031,3210 translation_subset=False linear_parts={'(1, 2)': 2, '(2, 1)': 2} example={'square_index': 244, 'mask': '2013'}
```

Equivalences:

```text
{'F_2110_12_iff_two_diagonal_pair': True, 'F_2110_16_iff_v4_like': True, 'F_2110_12_iff_terminal_translation_subset': True}
```

## Interpretation

The `F_2110=12/16` split is not a new independent mystery.  It
is exactly the terminal-set split already seen in the extra-32
audit: the two-diagonal translation-subset records have
`F_2110=12`, while the two v4-like terminal-set classes have
`F_2110=16`.
