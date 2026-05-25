# Kernel V4 Versus Terminal Translation V4

Status: Phase O5 follow-up audit, outside the paper

## Purpose

Phase O3/O4 exposed the natural value-bit action:

```text
S4 -> S3
```

on the three coordinate-axis matchings.  Its kernel is a Klein four group.
Since the terminal exact-`V4` class also has a Klein four group of permutation
diagonals, the natural question was whether these two `V4` objects coincide
after transport through the cell-value affine map.

Replay artifacts:

```text
scripts/analyze_kernel_v4_o5.py
tests/test_kernel_v4_o5.py
results/kernel_v4_o5.json
results/KERNEL_V4_O5_REPORT.md
```

## Verdict

The direct identification is false.

Across the `144` terminal-24 exact-`V4` affine records:

```text
value-bit kernel size: 4
selected-plane kernel stabilizer size: 2
selected-plane kernel orbit size: 2
kernel orbit equals terminal translation image planes: never
kernel orbit intersection with terminal image planes: always 0
```

So the value-bit kernel `V4` and the terminal translation `V4` live in related
but different actions.

## Positive Structure

The failed direct identification leaves a uniform positive statement.

For every one of the `144` records, the four terminal translation diagonals
map to:

```text
four cosets of one balanced value direction
```

and each of those four planes intersects the selected terminal value plane
in exactly one point:

```text
intersection pattern: (1,1,1,1)
```

The image direction is not fixed; it is distributed uniformly over six
balanced directions:

```text
6 directions x 24 records = 144
```

Thus the real relationship is not equality of the two `V4` groups, but a
parallel-class/coset relation between terminal translation diagonals and the
selected terminal value plane.

## Guardrail

Do not claim:

```text
terminal translation V4 = value-bit kernel V4
```

The safe claim is:

```text
In the exact-V4 affine terminal-24 class, the terminal translation V4 maps to
a four-coset parallel class whose members meet the selected terminal plane in
one point each.
```

## Next Question

The natural follow-up is to decide whether this parallel-class structure is a
small local fact or part of a broader Johnson-scheme description of quaterne
transport.
