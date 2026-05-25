# Terminal-24 Markov-Style Graph

Status: Phase H first small-move connectivity audit

## Scope

Nodes are the `236` terminal endpoint squares `Q-tM` from the Phase-C
terminal-24 records.  Edges use primitive fixed-sum diagonal-magic
kernel moves with entries in `{-1,0,1}`.

This is not a full Markov-basis theorem.

## Summary

- nodes: `236`
- primitive moves up to sign: `109`
- signed moves: `218`
- move support distribution up to sign: `{'10': 16, '12': 12, '16': 8, '4': 2, '6': 24, '8': 47}`
- edges: `247`
- degree distribution: `{'0': 50, '1': 36, '2': 8, '3': 130, '4': 10, '6': 2}`
- components: `98`
- component size distribution: `{'1': 50, '2': 13, '4': 28, '6': 4, '8': 3}`

## Class Interaction

- edge class counts: `{"('exact_v4', 'exact_v4')": 218, "('exact_v4', 'outside_main')": 8, "('main_extra', 'main_extra')": 3, "('main_extra', 'outside_main')": 14, "('outside_main', 'outside_main')": 4}`
- class degree distributions: `{'exact_v4': {'1': 2, '3': 130, '4': 10, '6': 2}, 'main_extra': {'0': 12, '1': 20}, 'outside_main': {'0': 38, '1': 14, '2': 8}}`
- component class profiles: `{'exact_v4:4': 28, 'exact_v4:4,main_extra:2,outside_main:2': 2, 'exact_v4:4,outside_main:2': 4, 'exact_v4:8': 1, 'main_extra:1': 12, 'main_extra:1,outside_main:1': 10, 'main_extra:2': 3, 'outside_main:1': 38}`

## Interpretation

The small-move graph is highly disconnected.  It mostly connects exact
`V4` records to other exact `V4` records, while many outside-main and
main-extra records are isolated or only lightly attached.

## Guardrail

Do not claim endpoint-24 Markov connectivity from this graph.  The
computed graph is a conservative first audit using only primitive
`{-1,0,1}` kernel moves.
