# Research Roadmap

Status: public research roadmap for follow-up work.  This file is not a claim
ledger and does not extend the theorems proved in the paper.  It records the
open bridge problems that remain after the finite retraction/count-shadow
extension.

## Current Baseline

The paper now establishes three separate facts around the strong meet value
`24`:

1. On the Lo Shu side, the bounded `S=24` fiber is the last non-degenerate
   upper fiber before the degenerate all-9 fiber at `27`.
2. On the Durer/Sagrada side, the Sagrada ray reaches terminal sum `24` at
   `D(10)`.
3. The terminal square `D(10)` is a finite retraction of the Durer-complement
   source along the terminally recovered direction `u=1001`; its non-affine
   terminal quaternes have the guarded count-shadow `60=32+12+16`.

These facts give a certified numerical and finite-structural meet.  They do
not yet give a canonical mathematical map from the Lo Shu `3x3` geometry to
the Durer/Sagrada `4x4` geometry.

## Primary Next Task: Common Invariant-Shadow

Search for a common invariant-shadow tying together:

1. the Lo Shu fiber at sum `24`;
2. the Durer/Sagrada terminal square `D(10)`;
3. the terminal count-shadow `60=32+12+16`;
4. the affine/parity-plane mechanism already certified in the paper.

The target is not a visual metaphor or a numerical coincidence, but an object
that can be computed on both sides and compared without changing the existing
claim boundary.  Candidate shadows include parity profiles, affine-defect
profiles, endpoint fibers, quotient directions, small graph shadows of the
Lo Shu `S=24` lattice diamond, or incidence distributions induced by the
terminal retraction direction `u=1001`.

A successful result should say exactly what is preserved, what is lost, and
whether the preservation is canonical or depends on a choice of marking.

## Open Bridge Problems

### 1. Direct Lift Problem

We have not proved a direct lift from `D(10)` to the endpoint-24 affine-defect
atlas classes.

Current status: the paper proves only a terminal count-shadow.  It does not
construct a record/profile lift from the non-normal terminal square `D(10)` to
normal endpoint-24 atlas records.

Task: define what a lift would mean at the record/profile level, then test
whether the terminal records can be sent to endpoint-24 records while
preserving the relevant profiles.

### 2. Same-Object Problem for `32/12/16`

We have not proved that the terminal `32/12/16` split and the endpoint-atlas
`32/12/16` split are the same mathematical object.

Current status: the equality of count vectors is treated as a guarded
count-shadow only.

Task: compare the two splittings by invariant data, not just by cardinality.
If the profiles match, isolate the responsible structure.  If they do not,
record the obstruction and keep the equality as a numerical shadow.

### 3. Record-by-Record Correspondence Problem

We have not transformed the count-shadow into a record-by-record
correspondence.

Current status: the terminal replay certifies aggregate counts and guardrails.
It does not pair individual terminal quaternes or orbit classes with individual
endpoint-atlas records.

Task: build a candidate matching relation and test it under increasingly
strict invariants: quotient direction, affine/non-affine status, incidence
profile, parity/defect profile, and stabilizer/orbit data.

### 4. Retraction Generality Problem

We do not yet know whether the Sagrada terminal retraction is an isolated
feature of the Durer/Sagrada ray or part of a more general principle.

Current status: the paper proves the retraction for the Sagrada terminal
`D(10)` only.

Task: scan the other admissible one-incidence Durer masks and, later, the
order-four endpoint atlas, looking for finite retractions of the same kind:
idempotent maps, small image loss, terminally recoverable duplicate directions,
and compatible quaterne shadows.

## Decision Criteria

A follow-up should move toward the paper only if it satisfies at least one of
these criteria:

- it produces a canonical invariant common to the Lo Shu and Durer/Sagrada
  sides;
- it upgrades the `32/12/16` count-shadow to a checked structural comparison;
- it proves that no direct lift or record-by-record bridge exists under a
  natural class of invariants;
- it turns the Sagrada retraction from a one-off fact into a classified family
  phenomenon.

Otherwise the result should remain an internal audit or a watch item.