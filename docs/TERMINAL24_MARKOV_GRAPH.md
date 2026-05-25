# Terminal-24 Markov-Style Graph

Status: Phase H first small-move connectivity audit.

This is not a full Markov-basis computation.  It is a conservative graph on
the `236` terminal endpoint squares.

## Move Model

Nodes are terminal endpoint squares:

```text
T = Q - tM
```

for the `236` Phase-C terminal-24 records.

Edges use primitive fixed-sum diagonal-magic kernel moves whose cell entries
lie in:

```text
{-1,0,1}
```

The fixed-sum line system uses rows, columns, main diagonal, and anti-diagonal.

The move census is:

```text
primitive moves up to sign: 109
signed moves: 218
support distribution up to sign:
  4: 2
  6: 24
  8: 47
  10: 16
  12: 12
  16: 8
```

## Graph Result

The graph has:

```text
nodes: 236
edges: 247
components: 98
```

Degree distribution:

```text
0: 50
1: 36
2: 8
3: 130
4: 10
6: 2
```

Component size distribution:

```text
1: 50
2: 13
4: 28
6: 4
8: 3
```

So under this small-move model, the endpoint-24 terminal records are highly
disconnected.

## Class Interaction

Using the Phase-H classes:

```text
exact_v4      = 144 exact canonical V4 records
main_extra    = 32 structured extras inside the main inside-out signature
outside_main  = 60 remaining terminal-24 records
```

Edge classes:

```text
exact_v4 -- exact_v4:       218
exact_v4 -- outside_main:     8
main_extra -- main_extra:     3
main_extra -- outside_main:  14
outside_main -- outside_main: 4
```

Class degree distributions:

```text
exact_v4:
  degree 1: 2
  degree 3: 130
  degree 4: 10
  degree 6: 2

main_extra:
  degree 0: 12
  degree 1: 20

outside_main:
  degree 0: 38
  degree 1: 14
  degree 2: 8
```

Component class profiles:

```text
exact_v4:4:                              28
exact_v4:8:                               1
exact_v4:4,outside_main:2:                4
exact_v4:4,main_extra:2,outside_main:2:   2
main_extra:1:                            12
main_extra:2:                             3
main_extra:1,outside_main:1:             10
outside_main:1:                          38
```

## Interpretation

The exact canonical `V4` branch has the most internal small-move structure:
`218` of the `247` edges are exact-`V4` to exact-`V4`.

The `32` main-extra records are mostly peripheral:

```text
12 isolated
20 degree-one
```

The `60` outside-main records are also mostly peripheral:

```text
38 isolated
14 degree-one
8 degree-two
```

This supports the idea that exact canonical `V4` is not only an affine/SNF
subclass but also the densest part of the first small-move endpoint graph.

## Guardrail

Do not claim:

```text
the 236 terminal-24 pairs are Markov-connected;
this move set is a complete Markov basis;
disconnectedness under {-1,0,1} moves proves disconnectedness under all
Markov bases.
```

The established statement is:

```text
under primitive {-1,0,1} fixed-sum diagonal-magic kernel moves, the
terminal-24 graph has 98 connected components and 50 isolated vertices.
```

## Artifacts

```text
scripts/analyze_terminal24_markov_graph.py
tests/test_terminal24_markov_graph.py
results/terminal24_markov_graph.json
results/TERMINAL24_MARKOV_GRAPH_REPORT.md
```
