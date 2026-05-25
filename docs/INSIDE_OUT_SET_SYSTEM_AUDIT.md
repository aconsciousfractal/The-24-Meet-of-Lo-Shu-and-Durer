# Inside-Out Set-System Audit

Status: Phase H first certificate.

This note turns the inside-out / magic-labelling vocabulary into a concrete
finite set-system for the Durer/Sagrada object.  It does not yet compute an
Ehrhart function, a Hilbert basis, or a Markov basis.

## Set Systems

The cell set is the `4 x 4` Durer grid.  The audited edge systems are:

```text
magic_lines      rows, columns, main diagonal, anti-diagonal
lines_plus_mask  magic_lines plus the Sagrada mask
source           lines_plus_mask plus H_34(D), colored by Sagrada incidence
terminal         lines_plus_mask plus H_24(D(10)), colored by source sum and incidence
combined         source and terminal hyperedges together
```

The quaterne counts are the project baseline:

```text
|H_34(D)| = 86
|H_24(D(10))| = 96
```

## Incidence Results

The first structural change is caused by the Sagrada mask itself.

```text
magic_lines:
  edges = 10
  rank_Q = 9
  rank_F2 = 8
  right kernel dimension = 7
  SNF = 1^8, 2
  colored cell automorphism order = 8

lines_plus_mask:
  edges = 11
  rank_Q = 10
  rank_F2 = 9
  right kernel dimension = 6
  SNF = 1^9, 2
  colored cell automorphism order = 1
```

So the row/column/diagonal system still has the expected square symmetry, but
adding the distinguished Sagrada mask makes the colored set-system rigid.

The source, terminal, and combined hypergraph systems are all full-rank over
`Q` on the 16 cell labels:

```text
source:
  edges = 97
  rank_Q = 16
  rank_F2 = 14
  right kernel dimension = 0
  left dependency dimension = 81
  SNF = 1^14, 2, 40
  colored automorphism order = 1

terminal:
  edges = 107
  rank_Q = 16
  rank_F2 = 14
  right kernel dimension = 0
  left dependency dimension = 91
  SNF = 1^14, 2, 20
  colored automorphism order = 1

combined:
  edges = 193
  rank_Q = 16
  rank_F2 = 14
  right kernel dimension = 0
  left dependency dimension = 177
  SNF = 1^14, 2, 20
  colored automorphism order = 1
```

The persistent `rank_F2=14` and nonunit SNF factors show that the set-system
has integral/parity structure not visible from rational rank alone.

## Transport Decomposition

The source edge colors recover the known Durer incidence split:

```text
H_34(D), Sagrada incidence:
  incidence 0: 19
  incidence 1: 50
  incidence 2: 17
```

The terminal edge colors recover the source-sum transport decomposition:

```text
H_24(D(10)):
  source 24, incidence 0: 25
  source 34, incidence 1: 50
  source 44, incidence 2: 21
```

This gives the inside-out set-system substrate for the earlier quaterne
transport claims.

## Interpretation

The useful Phase-H result is not a new uniqueness theorem for `24`.  It is a
clean finite object:

```text
(cells, rows/columns/diagonals, Sagrada mask, H_34(D), H_24(D(10)))
```

with exact rank, SNF, kernel, and colored automorphism data.  This is the
right base object for later Hilbert-basis, Markov-move, and inside-out
polytope computations.

## Guardrail

Do not claim:

```text
the inside-out polytope has been enumerated;
D(10) is Hilbert-special;
endpoint-24 Markov connectivity is known;
the rank/SNF audit alone characterizes Durer/Sagrada among terminal-24 pairs.
```

The certificate only establishes the incidence substrate and its first exact
invariants.

## Artifacts

```text
scripts/analyze_inside_out_set_system.py
tests/test_inside_out_set_system.py
results/inside_out_set_system_audit.json
results/INSIDE_OUT_SET_SYSTEM_AUDIT_REPORT.md
```
