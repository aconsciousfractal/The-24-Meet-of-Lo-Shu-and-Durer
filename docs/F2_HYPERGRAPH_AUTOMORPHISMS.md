# F2 Hypergraph Automorphisms

Status: Phase F colored automorphism audit

## Purpose

This note audits automorphism groups of the Durer/Sagrada quaterne
hypergraphs in the value-label model:

```text
cell label = D[i,j] - 1 in F2^4.
```

The hypergraphs are:

```text
H_34(D)      = four-label sets with source sum 34
H_24(D(10))  = four-label sets with terminal sum 24
```

The replay artifacts are:

```text
scripts/analyze_f2_hypergraph_automorphisms.py
tests/test_f2_hypergraph_automorphisms.py
results/f2_hypergraph_automorphisms.json
results/F2_HYPERGRAPH_AUTOMORPHISM_REPORT.md
```

## Method

Each hypergraph is encoded as a colored incidence graph:

```text
16 cell vertices
one edge vertex per quaterne
cell-edge incidences
```

Automorphisms are graph automorphisms preserving node kind and edge colors.
The computation uses NetworkX VF2 on these finite incidence graphs.

## Results

```text
H34_all:                    |Aut| = 2
H34_affine_colored:         |Aut| = 2
H34_affine_only:            |Aut| = 384
H24_all:                    |Aut| = 16
H24_affine_colored:         |Aut| = 2
H24_source_colored:         |Aut| = 1
H24_source_affine_colored:  |Aut| = 1
```

The source `H_34(D)` hypergraph has only identity and value-complement
symmetry when all 86 quaternes are present.  Its affine sublayer alone is much
more symmetric:

```text
H34_affine_only group order: 384
cell action: transitive on all 16 labels
Sagrada mask orbit count: 24
Sagrada mask stabilizer order: 16
```

The terminal `H_24(D(10))` hypergraph has a modest uncolored symmetry:

```text
H24_all group order: 16
cell orbits: 8 fixed labels and 4 two-label orbits
Sagrada mask orbit count: 16
```

But the moment the terminal hypergraph remembers the Phase-F transport
mechanism, it becomes rigid:

```text
H24_source_colored group order: 1
H24_source_affine_colored group order: 1
```

Here `source_colored` means edge colors record:

```text
source_24_incidence_0
source_34_incidence_1
source_44_incidence_2
```

and `source_affine_colored` further distinguishes affine/non-affine quaternes.

## Interpretation

This is a useful negative/positive result.

Positive:

```text
the affine source sublayer has a large autonomous symmetry group
```

Negative/guardrail:

```text
the full terminal transport decomposition is rigid
```

So `H_24(D(10))` does not appear to carry a hidden large automorphism group
once the source/incidence mechanism is remembered.  Its structure is not
"more symmetric" in that sense; it is a bounded endpoint with a rigid
transport certificate.

## Guardrails

Do not claim:

- the terminal `96`-quaterne hypergraph has a large hidden symmetry after
  source/incidence coloring;
- the affine source sublayer symmetry is a symmetry of the full `H_34(D)`;
- the automorphism audit characterizes endpoint `24` across all order-4
  squares.

The correct statement is local and exact: in the Durer/Sagrada value-label
model, the affine source layer is highly symmetric, while the colored
terminal transport hypergraph is rigid.
