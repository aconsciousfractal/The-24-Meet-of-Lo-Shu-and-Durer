# Hilbert-Style Semigroup Audit

Status: Phase H finite atom/decomposition audit

## Scope

This is not a complete Hilbert-basis theorem.  It enumerates
nonnegative diagonal-magic squares up to magic sum `8`,
extracts indecomposable atoms in that range, and tests decompositions
of the Magic 24 targets in the generated atom set.

## Atom Census

- square counts by sum: `{'1': 8, '2': 48, '3': 200, '4': 675, '5': 1904, '6': 4736, '7': 10608, '8': 21925}`
- atom counts by sum: `{'1': 8, '2': 12, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}`
- atom support counts by sum: `{'1': {'4': 8}, '2': {'7': 8, '8': 4}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}, '8': {}}`
- total checked atoms: `20`
- atom magic-sum distribution: `{'1': 8, '2': 12}`

## Named Decompositions

### durer_source_D

- magic sum: `34`
- decomposition: `{'success': True, 'min_atom_count': 18, 'support_size': 7, 'atom_magic_sum_coefficient_counts': {'1': 2, '2': 16}, 'coefficients': [{'atom_index': 3, 'atom_magic_sum': 1, 'coefficient': 1}, {'atom_index': 4, 'atom_magic_sum': 1, 'coefficient': 1}, {'atom_index': 8, 'atom_magic_sum': 2, 'coefficient': 1}, {'atom_index': 10, 'atom_magic_sum': 2, 'coefficient': 6}, {'atom_index': 12, 'atom_magic_sum': 2, 'coefficient': 3}, {'atom_index': 13, 'atom_magic_sum': 2, 'coefficient': 5}, {'atom_index': 17, 'atom_magic_sum': 2, 'coefficient': 1}], 'reconstruction_matches': True}`

### durer_terminal_D10

- magic sum: `24`
- decomposition: `{'success': True, 'min_atom_count': 18, 'support_size': 8, 'atom_magic_sum_coefficient_counts': {'1': 12, '2': 6}, 'coefficients': [{'atom_index': 0, 'atom_magic_sum': 1, 'coefficient': 2}, {'atom_index': 2, 'atom_magic_sum': 1, 'coefficient': 1}, {'atom_index': 4, 'atom_magic_sum': 1, 'coefficient': 6}, {'atom_index': 5, 'atom_magic_sum': 1, 'coefficient': 3}, {'atom_index': 8, 'atom_magic_sum': 2, 'coefficient': 2}, {'atom_index': 10, 'atom_magic_sum': 2, 'coefficient': 1}, {'atom_index': 13, 'atom_magic_sum': 2, 'coefficient': 2}, {'atom_index': 18, 'atom_magic_sum': 2, 'coefficient': 1}], 'reconstruction_matches': True}`

## Terminal-24 Endpoint Decompositions

- pair count: `236`
- failed decompositions: `0`
- min atom-count distribution: `{'12': 4, '13': 4, '14': 24, '15': 8, '16': 44, '17': 16, '18': 100, '19': 8, '20': 20, '22': 8}`
- class min atom-count distributions: `{'exact_v4': {'14': 16, '16': 24, '18': 80, '20': 16, '22': 8}, 'main_extra': {'12': 4, '14': 8, '16': 4, '18': 12, '20': 4}, 'outside_main': {'13': 4, '15': 8, '16': 16, '17': 16, '18': 8, '19': 8}}`
- degree-profile distribution: `{"(('1', 10), ('2', 7))": 16, "(('1', 12), ('2', 6))": 100, "(('1', 14), ('2', 5))": 8, "(('1', 16), ('2', 4))": 20, "(('1', 2), ('2', 11))": 4, "(('1', 20), ('2', 2))": 8, "(('1', 4), ('2', 10))": 24, "(('1', 6), ('2', 9))": 8, "(('1', 8), ('2', 8))": 44, "(('2', 12),)": 4}`

## Guardrail

The audit shows that the tested targets decompose in the finite atom
set found through sum 8.  It does not prove that no higher-degree
Hilbert-basis atoms exist in the full cone.
