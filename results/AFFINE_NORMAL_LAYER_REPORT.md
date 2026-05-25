# Affine Normal Order-4 Layer Audit

Status: Phase O2 generalization pass

## Scope

This audit leaves the terminal-24 atlas and studies all globally
affine essential normal order-4 representatives across all eight
one-incidence masks.

## Counts

- essential representatives: `880`
- globally affine representatives: `432`
- affine square-mask pairs: `3456`
- selected value planes: `24`
- selected directions: `6`

## Uniformity

- selected value plane count distribution: `{'144': 24}`
- selected direction count distribution: `{'576': 6}`

Thus the `3456` affine square-mask pairs split uniformly as

```text
24 selected value planes x 144 pairs.
```

## Endpoint-24 Layer

- terminal-24 affine pairs: `144`
- terminal-24 selected value planes: `{'11,12,15,16': 144}`
- terminal-24 terminal sets: `{'0123,1032,2301,3210': 144}`
- terminal-24 all full translation V4: `True`

So the `144` exact-`V4` records arise as one selected value plane
inside the global affine normal layer:

```text
selected values {11,12,15,16}
  -> endpoint 24
  -> full translation terminal V4.
```

## Interpretation

This is the first explanation of the number `144` beyond the
terminal-24 atlas: among globally affine normal order-4 squares,
the admissible masks distribute uniformly over `24` selected value
planes.  The terminal-24 plane is exactly one of them.

## Guardrail

This is still a finite normal-order-4 statement.  It does not prove
a universal endpoint theorem and it does not include non-affine
terminal-24 records.
