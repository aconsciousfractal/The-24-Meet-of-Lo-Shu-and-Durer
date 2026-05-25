# Lemma Suite

Status: Phase B paper-facing draft
Date: 2026-05-24

This file converts the Phase-A certificate pack into a paper-facing lemma
chain.  The statements below are intended to be close to paper prose while
keeping certificate dependencies explicit and auditable.

Primary certificate:

```text
results/magic24_certificate_pack.json
```

Primary replay script:

```text
scripts/magic24_certificates.py
```

## Notation

Let

```text
B(n,m,S)
```

be the set of integer `n x n` magic squares with all row sums, column sums,
and the two main diagonal sums equal to `S`, with entries in `[1,m]`.
Repeated entries are allowed.

Use the Lo Shu square

```text
4 9 2
3 5 7
8 1 6
```

with magic sum `15`.

Use the Durer-complement square

```text
1  14 15 4
12 7  6  9
8  11 10 5
13 2  3  16
```

with magic sum `34`.

The Sagrada/Durer mask is the permutation mask

```text
2013 = {(0,2), (1,0), (2,1), (3,3)}.
```

Define

```text
D(t) = D - t M.
```

## Main Theorem - Strong Bounded Meet

The weak meet of the Lo Shu bounded upward spectrum and the Durer/Sagrada
bounded downward ray is:

```text
Meet_weak = {24,27}.
```

The strong meet, after requiring non-degeneration on the `3 x 3` side and
terminality on the `4 x 4` side, is:

```text
Meet_strong = {24}.
```

This is the core theorem of the first Magic 24 note.  The proof is the short
combination of Lemmas 1, 2, and 3 below.  A standalone paper-ready version is
kept in:

```text
docs/STRONG_MEET_THEOREM.md
```

## Lemma 1 - Lo Shu Bounded Spectrum

Statement:

```text
Spec^+_{3,9}(15) = {18,21,24,27}.
```

More precisely, the counts for `B(3,9,S)` are:

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

At `S=24`, the fiber has five squares.  At `S=27`, the fiber is the single
constant all-9 square.

Proof route:

Every `3 x 3` magic square has the integer parametrization

```text
g+a     g-a-b   g+b
g-a+b   g       g+a-b
g-b     g+a+b   g-a
```

with magic sum `S=3g`.  Bounding every entry by `[1,9]` gives exactly the
finite fibers replayed in the certificate.

Certificate pointer:

```text
lo_shu_bounded_spectrum
```

Claim IDs:

```text
M24-C01, M24-C02, M24-C03
```

## Lemma 2 - Durer/Sagrada Terminality

Statement:

Among the 8 admissible one-incidence masks of the Durer-complement square,
the Sagrada/Durer mask `2013` is the unique mask whose bounded terminal sum is
`24`.

Proof route:

An admissible mask is a permutation mask with exactly one selected cell on
each of the two main diagonals.  For a mask `p`, the largest allowed descent is

```text
t_max(p) = min(D_{i,p(i)} - 1).
```

The certificate enumerates all 24 permutation masks, retains the 8 admissible
ones, and computes `34 - t_max(p)`.

The unique terminal-24 row is:

```text
p = 2013
values = 15,12,11,16
t_max = 10
terminal sum = 24
```

Certificate pointer:

```text
durer_one_incidence_masks
```

Claim IDs:

```text
M24-C04, M24-C05
```

## Lemma 3 - Weak And Strong Meet

Statement:

```text
Meet_weak = {24,27}
Meet_strong = {24}
```

Proof route:

The Lo Shu bounded upward side above `15` is

```text
{18,21,24,27}.
```

The Durer/Sagrada bounded downward ray below `34` is

```text
{24,25,26,27,28,29,30,31,32,33}.
```

Their intersection is:

```text
{24,27}.
```

The strong meet keeps only points that are non-degenerate on the `3 x 3` side
and terminal on the `4 x 4` side.  The point `24` satisfies both conditions:
it has a 5-element `3 x 3` fiber and is the terminal Sagrada/Durer endpoint.
The point `27` fails both strong criteria: it is the constant all-9 square on
the `3 x 3` side and is not terminal on the `4 x 4` side.

Certificate pointers:

```text
lo_shu_bounded_spectrum
durer_one_incidence_masks
```

Claim ID:

```text
M24-C06
```

## Lemma 4 - Durer Pattern Transport

Statement:

The Durer square has

```text
|H_34(D)| = 86
```

four-cell subsets summing to `34`.  Against the Sagrada mask, their incidence
distribution is:

```text
0 -> 19
1 -> 50
2 -> 17
```

At the terminal point `D(10)`,

```text
|H_24(D(10))| = 96.
```

These 96 quaternes decompose as:

```text
source sum 34, incidence 1 -> 50
source sum 24, incidence 0 -> 25
source sum 44, incidence 2 -> 21
```

Proof route:

Enumerate all `binom(16,4)` four-cell subsets.  For a quaterne `Q`,

```text
sum_{c in Q} D(10)_c = sum_{c in Q} D_c - 10 |Q cap M|.
```

This identity gives the source-sum/incidence decomposition.

Certificate pointer:

```text
durer_pattern_transport
```

Claim IDs:

```text
M24-C07, M24-C08, M24-C09
```

## Lemma 5 - Permutation-Diagonal Symmetry Break

Statement:

Let `f_A(sigma)` be the sum of entries of `A` on the permutation diagonal
indexed by `sigma in S_4`.

For the Durer-complement square,

```text
G_34(D) = {sigma in S_4 : f_D(sigma)=34}
```

is the 8-element set

```text
0123, 0213, 1032, 1302, 2031, 2301, 3120, 3210.
```

It is a subgroup of `S_4` with element-order profile:

```text
{1:1, 2:5, 4:2}
```

so it is isomorphic to the dihedral group of order 8.

For every `t=1,...,10`,

```text
G_{34-t}(D(t)) = {0123,1032,2301,3210}.
```

This is `V_4`, with element-order profile:

```text
{1:1, 2:3}
```

Thus the ray induces the break:

```text
D_4 -> V_4 subset A_4 subset S_4.
```

Proof route:

Enumerate all 24 permutations of `S_4`, compute their permutation-diagonal
sums for `D(t)`, and test closure, inverses, and element orders.

Certificate pointer:

```text
durer_permutation_diagonals
```

Claim IDs:

```text
M24-C10, M24-C11
```

## Lemma 6 - V4 Is Not A Standard Type-A Poset Cone

Statement:

The set

```text
V_4 = {0123,1032,2301,3210}
```

is not a standard Type-A poset cone `L(P)`.

Proof route:

In the Type-A halfspace convention, a poset cone is determined by precedence
relations common to all its words.  The common precedence relation set of
`V_4` is empty.  Therefore its common-halfspace closure is all `S_4`, of size
24, not `V_4`.

So the correct Type-A direction is not

```text
V_4 = L(P).
```

It is:

```text
V_4 <= S_4 is a subgroup/coset tiler.
```

Certificate pointer:

```text
durer_permutation_diagonals.poset_cone_tests
```

Claim ID:

```text
M24-C12
```

## Lemma 7 - APD And Centered Determinant

Statement:

Along the Sagrada/Durer ray:

```text
APD_1(D(t)) = 0
APD_2(D(t)) = 0
APD_3(D(t)) = -24 t(t-4)(t-16)
```

and, for the centered standard-subspace restriction,

```text
det Ehat(t) = -4 t(t-4)(t-16).
```

Therefore:

```text
APD_3(D(t)) = 6 det Ehat(t).
```

Proof route:

The certificate expands all 24 permutation-diagonal sums as linear polynomials
in `t` and computes the alternating even-minus-odd power sums.  It also expands
the determinant of the explicit `3 x 3` matrix:

```text
-t      24-t    24-2t
6-2t    12-t    10-t
6-t     20-2t   18-t
```

Certificate pointer:

```text
apd_centered_ray
```

Claim IDs:

```text
M24-C13, M24-C14
```

## Phase-B Output Target

The short paper can now use this lemma chain as its technical spine:

```text
Lemma 1 + Lemma 2 -> Lemma 3
Lemma 4 -> hypergraph evidence at 24
Lemma 5 + Lemma 6 -> Type-A / subgroup-coset bridge
Lemma 7 -> centered-operator / APD bridge
```

The core theorem should be phrased narrowly:

```text
The strong bounded Lo Shu/Durer-Sagrada meet is {24}.
```

The surrounding results explain why this endpoint is worth studying, without
promoting `24` to a universal invariant.
