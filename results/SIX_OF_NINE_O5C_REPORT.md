# Six Of Nine Balanced Complements

Status: Phase O5c follow-up audit, outside the paper

## Question

In the terminal-24 exact-`V4` affine class, why do the terminal
directions use six of the nine balanced complements to the selected
plane direction?

## Answer

Let `U` be the selected terminal value-plane direction and `Q` its
coordinate partner in the matching:

- `U = [0, 1, 4, 5]`
- `Q = [0, 2, 8, 10]`

Every balanced complement `W` to `U` is a graph of a binary linear
map:

```text
Q -> U
```

The nine balanced complements are exactly the maps with no zero rows.
The six terminal-24 directions are exactly the invertible maps.

Counters:

- balanced complements to `U`: `9`
- graph-rank distribution: `{'1': 3, '2': 6}`
- complements also transverse to `Q`: `{'False': 3, 'True': 6}`
- terminal directions: `6`
- terminal direction distribution: `{'0,3,12,15': 24, '0,3,13,14': 24, '0,6,11,13': 24, '0,6,9,15': 24, '0,7,11,12': 24, '0,7,9,14': 24}`
- terminal graph-rank distribution: `{'2': 144}`
- terminal directions equal invertible complements: `True`

## Interpretation

The six-of-nine split is therefore not accidental:

```text
9 balanced complements = 6 invertible graphs + 3 rank-one graphs
terminal-24 exact-V4 uses the 6 invertible graphs
```

Equivalently, the terminal directions are the balanced directions
complementary to both directions in the selected coordinate-axis
matching.  The three excluded directions are still transverse to the
selected plane, but they meet the partner direction nontrivially.
