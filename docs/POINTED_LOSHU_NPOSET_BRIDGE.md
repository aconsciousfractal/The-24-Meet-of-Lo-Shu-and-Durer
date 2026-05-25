# Pointed Lo Shu / N-Poset Bridge

Status: Phase G micro-audit

Certificate:

```text
scripts/analyze_pointed_loshu_nposet.py
results/pointed_loshu_nposet_bridge.json
results/POINTED_LOSHU_NPOSET_BRIDGE_REPORT.md
tests/test_pointed_loshu_nposet.py
```

## Question

The Lo Shu `S=24` bounded fiber has five lattice points.  In the Type-A
`S4` poset-cone catalogue, the non-tiler cones of size `5` are represented
by posets such as the `N`-poset.

The raw cardinality match is not enough.  This audit tests whether there is
an actual five-state structure.

## Lo Shu Side

For `S=24`, the Lo Shu parametrization has `g=8` and the five parameter
points:

```text
O = ( 0,  0)
E = ( 1,  0)
N = ( 0,  1)
W = (-1,  0)
S = ( 0, -1)
```

The natural lattice adjacency graph is the star:

```text
O--E, O--N, O--W, O--S
```

It has degree sequence:

```text
1,1,1,1,4
```

This graph is not isomorphic to the `N`-poset linear-extension graph.

## Pointed Lo Shu Graph

Add two pieces of structure:

1. the boundary cycle on the four noncentral points;
2. one marked boundary point where the center is attached.

With mark `E`, the edges are:

```text
E--N, N--W, W--S, S--E, E--O
```

This graph has degree sequence:

```text
1,2,2,2,3
```

All four choices of boundary mark give isomorphic pointed graphs.

## N-Poset Side

Use the `N`-poset on `{a,b,c,d}` with relations:

```text
a < b
c < b
c < d
```

Its five linear extensions are:

```text
acbd
acdb
cabd
cadb
cdab
```

The adjacent-swap linear-extension graph has edges:

```text
acbd--acdb
acbd--cabd
acdb--cadb
cabd--cadb
cadb--cdab
```

This is the same graph type as the pointed Lo Shu graph: a 4-cycle with one
pendant vertex.

## Explicit Isomorphism

For the Lo Shu graph pointed at `E`, the certificate verifies:

```text
E -> cadb
O -> cdab
N -> acdb
W -> acbd
S -> cabd
```

This preserves all five edges exactly.

## A2 Order-Ideal Reading

The same five-state graph is also realized by the Hasse graph of
`J(A2+)`, the order-ideal lattice of the positive root poset of type `A2`.

The positive root poset has:

```text
alpha < alpha+beta
beta  < alpha+beta
```

The five order ideals are:

```text
{}
{alpha}
{beta}
{alpha,beta}
{alpha,beta,alpha+beta}
```

The certificate verifies:

```text
pointed Lo Shu graph ~= N-poset linear-extension graph
pointed Lo Shu graph ~= J(A2+) Hasse graph
N-poset linear-extension graph ~= J(A2+) Hasse graph
```

## Interpretation

This is a coherent Phase-G branch, but it is pointed rather than canonical.

What is established:

```text
pointed Lo Shu S=24 graph ~= G_lin.ext(N) ~= Hasse(J(A2+))
```

What is not established:

```text
bare 5=5 gives a natural bridge
unpointed Lo Shu S=24 canonically selects the N-poset graph
the marked boundary point is selected by the current certificate
```

The open problem is to find a non-arbitrary source for the marked Lo Shu
boundary point.  Candidate selectors are:

```text
Sagrada terminal lower-bound hit
D4 -> V4 quotient/coset data
APD/PTE deformation data
F2^4 Sagrada affine-plane direction
```

Until one of these selectors is certified, this branch should be used as a
controlled structural analogy, not as an independent characterization of
`24`.
