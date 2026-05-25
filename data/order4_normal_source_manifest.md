# Order-4 Normal Magic Squares Source Manifest

Status: Public deterministic dataset manifest
Date: 2026-05-24

## Decision

The public package uses a deterministic generator as the primary dataset
source.

No external dataset is required for the first pass.

## Scope

The dataset reconstructs normal `4 x 4` magic squares:

- entries are exactly `1,2,...,16`;
- every row sums to `34`;
- every column sums to `34`;
- both main diagonals sum to `34`.

The generator produces:

- `7040` raw oriented/reflected squares;
- `880` essential representatives after quotienting by the 8 square
  symmetries.

## Generator

```text
scripts/enumerate_order4_endpoints.py
```

Generation strategy:

1. Enumerate all ordered rows of four distinct values from `1..16` summing to
   `34`.
2. Choose disjoint first and second rows.
3. Choose a disjoint third row.
4. Determine the fourth row from the column sums.
5. Check row, column, diagonal, and normality constraints.
6. Canonicalize each square under the 8 dihedral symmetries of the square by
   lexicographic minimum.

This is an exact finite replay. No randomized sampling is used.

## Outputs

Dataset:

```text
data/order4_normal_essential_880.json
```

Endpoint spectrum:

```text
results/order4_endpoint_spectrum.json
```

## Verification Gates

Tests:

```powershell
python -m pytest tests/test_order4_internal_dataset.py -q
```

Required checks:

- raw count is `7040`;
- essential representative count is `880`;
- all essential representatives pass exact magic-square validation;
- normal-square symmetry orbits have size `8`;
- the Durer-complement square is present in the canonical dataset;
- the Sagrada mask on the Durer-complement square has terminal sum `24`;
- endpoint-spectrum pair counts are internally consistent.

## Literature Role

Ollerenshaw-Bondi and later order-4 classifications remain literature anchors
for the known `880` essential count. In this project they are used as a sanity
target and bibliography source, not as the dataset itself.
