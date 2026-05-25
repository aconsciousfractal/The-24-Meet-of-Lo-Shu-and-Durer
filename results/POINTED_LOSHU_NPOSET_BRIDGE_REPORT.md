# Pointed Lo Shu / N-Poset Bridge Report

Status: Phase G pointed five-state bridge audit

## Summary

- natural Lo Shu graph isomorphic to N-poset graph: `False`
- pointed Lo Shu graph isomorphic to N-poset graph: `True`
- pointed Lo Shu graph isomorphic to `J(A2+)`: `True`
- N-poset graph isomorphic to `J(A2+)`: `True`
- explicit Lo Shu -> N-poset mapping verified: `True`
- explicit Lo Shu -> A2 mapping verified: `True`
- all boundary marks give isomorphic graphs: `True`

## N-Poset Linear Extensions

```text
acbd
acdb
cabd
cadb
cdab
```

## Explicit Pointed Map

Lo Shu mark `E` is the degree-3 vertex and `O` is the pendant vertex.

```text
E -> cadb
O -> cdab
N -> acdb
W -> acbd
S -> cabd
```

## Interpretation

The bare cardinality `5=5` is not enough: the natural Lo Shu lattice
adjacency graph is not the N-poset linear-extension graph.  The
isomorphism appears only after adding a boundary cycle and marking one
boundary point to attach the center.

This is a coherent branch, but it is pointed rather than canonical.  The
open mathematical question is whether the marked boundary point can be
selected non-arbitrarily from Sagrada terminality, `D4 -> V4`, APD/PTE,
or the `F2^4` layer.
