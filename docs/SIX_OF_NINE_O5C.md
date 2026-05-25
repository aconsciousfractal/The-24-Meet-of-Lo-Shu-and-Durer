# Six Of Nine Balanced Complements

Status: Phase O5c follow-up audit, outside the paper

## Purpose

Phase O5b showed that the terminal translation `V4` gives a quotient-section
torsor: the selected value plane intersects the four cosets of a balanced
direction in one point each.

For the terminal-24 exact-`V4` class, the selected direction has nine balanced
complements, but only six occur as terminal directions.  This note explains
that split.

Replay artifacts:

```text
scripts/analyze_six_of_nine_o5c.py
tests/test_six_of_nine_o5c.py
results/six_of_nine_o5c.json
results/SIX_OF_NINE_O5C_REPORT.md
```

## Setup

Let `U` be the selected terminal value-plane direction:

```text
U = {0,1,4,5}
```

Its coordinate partner in the matching is:

```text
Q = {0,2,8,10}
```

Every balanced complement `W` to `U` can be written as a graph of a binary
linear map:

```text
Q -> U
```

## Result

The nine balanced complements split as:

```text
9 balanced complements = 6 invertible graphs + 3 rank-one graphs
```

The terminal-24 exact-`V4` class uses exactly the six invertible graphs:

```text
terminal directions: 6
distribution: 6 directions x 24 records
terminal graph rank: 2 for all 144 records
```

Equivalently, the terminal directions are the balanced directions
complementary to both `U` and `Q`.

## Excluded Three

The three unused balanced complements are:

```text
{0,2,13,15}
{0,7,8,15}
{0,7,10,13}
```

They are still transverse to `U`, but their graph maps `Q -> U` have rank
one.  Equivalently, they intersect the partner direction `Q` nontrivially.

## Interpretation

The `6 of 9` split is structural:

```text
6 = |GL(2,2)|
```

The terminal-24 exact-`V4` class selects the invertible part of the balanced
complement graph.  This closes the O5 torsor refinement at the finite
linear-algebra level.
