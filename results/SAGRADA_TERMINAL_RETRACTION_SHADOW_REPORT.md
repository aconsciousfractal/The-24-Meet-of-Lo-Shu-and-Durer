# Sagrada Terminal Retraction and Count Shadow

Status: public replay artifact for the Shu-Durer paper.

## Retraction

- fold direction: `1001`
- image size: `12`
- fiber-size distribution: `{1: 8, 2: 4}`
- subtraction equals retraction: `True`

## Terminal Duplicate Direction

| value | bits A | bits B | difference |
|---:|---|---|---|
| 1 | `0000` | `1001` | `1001` |
| 2 | `0100` | `1101` | `1001` |
| 5 | `0010` | `1011` | `1001` |
| 6 | `0110` | `1111` | `1001` |

## Terminal Quaternes

- `|H_24(D(10))| = 96`
- affine/nonaffine split: `36/60`
- nonaffine count-shadow vector: `[32, 12, 16]`

## Guardrails

- The 32/12/16 vector is a count-shadow only.
- The replay does not construct a record/profile lift to any endpoint-24 atlas class.
- The terminal square D(10) is non-normal and is not an endpoint-24 normal atlas record.
