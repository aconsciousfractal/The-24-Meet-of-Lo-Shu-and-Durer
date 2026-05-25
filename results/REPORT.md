# Magic 24 Certificate Report

Generated from:

```text
scripts/magic24_certificates.py
```

Primary artifact:

```text
magic24_certificate_pack.json
```

## Verified Spine

### Lo Shu bounded spectrum

For `B(3,9,S)`:

| S | Count |
|---:|---:|
| 3 | 1 |
| 6 | 5 |
| 9 | 13 |
| 12 | 25 |
| 15 | 41 |
| 18 | 25 |
| 21 | 13 |
| 24 | 5 |
| 27 | 1 |

Thus:

```text
Spec^+_{3,9}(15) = {18,21,24,27}
```

The `S=24` fiber has 5 squares. The `S=27` fiber is the unique all-9 square.

### Durer one-incidence masks

There are 8 admissible one-incidence permutation masks. The unique mask with
terminal sum `24` is:

```text
2013
```

It touches values:

```text
15, 12, 11, 16
```

and has:

```text
t_max = 10
terminal_sum = 24
```

### Durer quaterne transport

```text
|H_34(D)| = 86
incidence distribution = {0:19, 1:50, 2:17}
|H_24(D(10))| = 96
```

The `D(10)` quaternes summing to `24` decompose as:

```text
source_sum_34, incidence_1: 50
source_sum_24, incidence_0: 25
source_sum_44, incidence_2: 21
```

### Permutation diagonals

At `t=0`, the target diagonals are:

```text
0123, 0213, 1032, 1302, 2031, 2301, 3120, 3210
```

They form an 8-element subgroup.

Its element-order profile is:

```text
{1:1, 2:5, 4:2}
```

This is the order profile of the dihedral group of order 8.

For every `t=1..10`, the target diagonals are:

```text
0123, 1032, 2301, 3210
```

They form `V_4`.

Its element-order profile is:

```text
{1:1, 2:3}
```

The common precedence relations for `V_4` are empty, so its standard Type-A
common-halfspace closure has size `24`. Therefore `V_4` is not a standard
poset cone `L(P)`.

### APD and determinant

The generated coefficient convention is ascending powers of `t`.

```text
APD_1 = 0
APD_2 = 0
APD_3 = -1536 t + 480 t^2 - 24 t^3
det Ehat = -256 t + 80 t^2 - 4 t^3
```

Hence:

```text
APD_3 = 6 det Ehat
```

## Test Status

```text
5 passed
```

## Next Review Step

Promote this report into the Phase-B lemma suite after checking whether the
8-element `G_34` subgroup should be named `D_4` in the paper by an explicit
generator presentation.
