# Terminal Parallel-Class Torsor

Status: Phase O5b follow-up audit, outside the paper

## Purpose

Phase O5 showed that the value-bit kernel `V4` and the terminal translation
`V4` should not be identified.  The remaining positive question was whether
the terminal translation `V4` still defines a torsor over the selected value
plane through the four parallel cosets visible in `F2^4`.

Replay artifacts:

```text
scripts/analyze_terminal_parallel_torsor_o5b.py
tests/test_terminal_parallel_torsor_o5b.py
results/terminal_parallel_torsor_o5b.json
results/TERMINAL_PARALLEL_TORSOR_O5B_REPORT.md
```

## Main Finding

The torsor statement is true, and it is broader than terminal-24.

Across all globally affine square-mask pairs:

```text
records: 3456
translation image direction balanced: true for all 3456
selected direction complementary to translation direction: true for all 3456
intersection pattern with selected plane: (1,1,1,1) for all 3456
translation-to-selected point map bijective: true for all 3456
translation-to-selected point map affine: true for all 3456
```

Thus the fixed domain translation subgroup gives a four-coset parallel class
in value space, and the selected value plane is a section of the quotient by
that balanced direction.

## Terminal Subclass

In the full-translation terminal subclass:

```text
records: 1968
same torsor statement: true for all 1968
```

Here the fixed translation subgroup is not merely a background affine
structure; it is the terminal `V4`.

For the terminal-24 exact-`V4` class:

```text
records: 144
selected direction: 0,1,4,5
balanced complements to selected direction: 9
used terminal directions: 6
distribution: 6 directions x 24 records
```

So the terminal-24 class uses six of the nine balanced complements to the
selected terminal plane direction.

## Kernel Guardrail

The value-bit kernel still does not act as the terminal translation group on
the selected plane:

```text
setwise stabilizer size in the kernel: 2
point-orbit pattern on the selected plane: (1,1,2)
full kernel orbit size on selected planes: 2
```

So the kernel does not act transitively on the four points of the selected
plane.  The correct structure is not equality or conjugacy of the two `V4`
actions, but a quotient-section relation:

```text
F2^4 -> F2^4 / W
```

where `W` is the balanced translation-image direction and the selected value
plane is a section.

## Next Question

The next natural problem is to explain why terminal-24 uses exactly six of
the nine balanced complements to the selected plane direction, and whether
that six-of-nine split is controlled by the same matching structure that
organizes the `432 = 3 x 144` affine representatives.
