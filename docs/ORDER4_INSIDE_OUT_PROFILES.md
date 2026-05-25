# Order-4 Inside-Out Profile Extension

Status: Phase H terminal-24 rank/SNF/parity extension.

This note extends the first Durer/Sagrada inside-out set-system audit to all
`236` Phase-C terminal-24 square-mask pairs.

The scope is deliberately narrower than a full automorphism/Hilbert/Markov
audit: for each pair, it computes incidence rank over `Q`, rank over `F2`,
right-kernel dimension, left-dependency dimension, and Smith normal form for
three systems:

```text
source    rows/columns/diagonals + selected mask + H_34(Q)
terminal  rows/columns/diagonals + selected mask + H_24(Q-tM)
combined  source + terminal H_24(Q-tM)
```

## Global Result

Across the `236` terminal-24 pairs:

```text
source signatures: 6
terminal signatures: 8
combined signatures: 8
all source/terminal/combined systems are full-rank over Q
all source/terminal/combined systems have trivial right kernel over Q
```

So every terminal-24 pair is rigid at the rational incidence-rank level.  The
interesting variation is in `F2` rank, edge count, and SNF.

## Source Signatures

The source systems split as:

```text
180 pairs: edges 97, rank_F2 14, SNF 1^14,2,40
 16 pairs: edges 97, rank_F2 15, SNF 1^15,76
 16 pairs: edges 97, rank_F2 15, SNF 1^15,84
 12 pairs: edges 97, rank_F2 14, SNF 1^14,2,44
  8 pairs: edges 97, rank_F2 14, SNF 1^14,2,36
  4 pairs: edges 97, rank_F2 15, SNF 1^15,68
```

The Durer/Sagrada source signature belongs to the large 180-pair class.

## Terminal Signatures

The terminal systems split as:

```text
176 pairs: edges 107, rank_F2 14, SNF 1^14,2,20, terminal quaternes 96
 16 pairs: edges 118, rank_F2 15, SNF 1^15,36, terminal quaternes 107
 12 pairs: edges 122, rank_F2 14, SNF 1^14,4,8, terminal quaternes 111
  8 pairs: edges 101, rank_F2 14, SNF 1^14,4,12, terminal quaternes 90
  8 pairs: edges 106, rank_F2 15, SNF 1^15,44, terminal quaternes 95
  8 pairs: edges 107, rank_F2 15, SNF 1^15,44, terminal quaternes 96
  4 pairs: edges 109, rank_F2 14, SNF 1^14,2,20, terminal quaternes 98
  4 pairs: edges 97,  rank_F2 15, SNF 1^15,52, terminal quaternes 86
```

The Durer/Sagrada terminal signature is the large 176-pair class:

```text
edges 107, rank_Q 16, rank_F2 14, SNF 1^14,2,20
```

This class contains:

```text
144 exact canonical V4 pairs
32 non-exact-canonical-V4 pairs
176 selected-mask-affine pairs
176 terminal affine pure-transport pairs
```

Thus the terminal inside-out rank/SNF signature aligns exactly with selected
mask affineness and terminal affine pure transport, but it is broader than the
exact canonical `V4` subclass.

## Interpretation

The Phase-H extension gives a useful filtration:

```text
236 terminal-24 pairs
  -> 176 main terminal inside-out signature pairs
      -> 144 exact canonical V4 pairs
          -> 8 Durer/Sagrada quotient-cell pairs
```

So the rank/SNF/parity profile is informative but not isolating.

It is a broader incidence signature compatible with the `F2^4` pure-transport
layer.  It should be treated as another structural enrichment of endpoint
`24`, not as a characterization of the Durer/Sagrada cell.

## Guardrail

Do not claim:

```text
inside-out rank/SNF profiles isolate Durer/Sagrada;
the main 176-pair signature equals exact canonical V4;
these profiles compute Hilbert-basis or Markov connectivity data;
rank over Q distinguishes terminal-24 cases.
```

The strongest current statement is:

```text
all 236 terminal-24 pairs are full-rank over Q;
their terminal incidence systems split into 8 exact rank/SNF/parity signatures;
the Durer/Sagrada signature is the 176-pair class matching selected-mask
affineness and terminal affine pure transport.
```

## Artifacts

```text
scripts/analyze_order4_inside_out_profiles.py
tests/test_order4_inside_out_profiles.py
results/order4_inside_out_profiles.json
results/ORDER4_INSIDE_OUT_PROFILE_REPORT.md
```
