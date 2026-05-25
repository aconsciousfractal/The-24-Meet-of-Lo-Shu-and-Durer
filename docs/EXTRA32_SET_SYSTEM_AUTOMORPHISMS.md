# Extra-32 Set-System Automorphisms

Status: Phase H focused audit of the 32 structured extras inside the main
inside-out terminal signature.

The previous split gave:

```text
176 main inside-out signature pairs
  144 exact canonical V4
   32 non-exact-canonical-V4 extras
```

This audit tests whether the 32 extras have a small colored set-system
automorphism distinction.

## Result

For every one of the 32 extra pairs, the colored automorphism tuple is:

```text
(lines_plus_mask, source, terminal, combined) = (1,1,1,1)
```

So the colored set-system automorphism audit does not split them further.
They are rigid at this resolution.

## Terminal-Set Classes

The useful split remains the terminal-set/source-size split:

```text
two_diagonal_pair: 16
v4_like_0213:      8
v4_like_1302:      8
```

### `two_diagonal_pair`

```text
pair count: 16
terminal set: 0123,3210
source diagonal sizes: 2:12, 4:4
complement-fixed: 8
automorphism tuple: (1,1,1,1) in all 16
```

### `v4_like_0213`

```text
pair count: 8
terminal set: 0123,0213,3120,3210
source diagonal size: 4 in all 8
complement-fixed: 0
automorphism tuple: (1,1,1,1) in all 8
```

### `v4_like_1302`

```text
pair count: 8
terminal set: 0123,1302,2031,3210
source diagonal size: 4 in all 8
complement-fixed: 0
automorphism tuple: (1,1,1,1) in all 8
```

## Interpretation

The 32 extras are not explained by a residual colored automorphism group:
they are already rigid once rows, columns, diagonals, mask, source quaternes,
and terminal transport colors are remembered.

The best current small invariant is therefore:

```text
terminal-set class + source diagonal size + complement-fixed status
```

not automorphism order.

## Guardrail

Do not claim:

```text
the 32 extras have hidden colored symmetry;
the automorphism audit separates exact canonical V4 from the extras;
rigidity implies mathematical insignificance.
```

The established claim is narrower:

```text
all 32 extras are rigid under the tested colored set-system automorphism
model, and they split as 16+8+8 by terminal-set class.
```

## Artifacts

```text
scripts/analyze_extra32_set_system_automorphisms.py
tests/test_extra32_set_system_automorphisms.py
results/extra32_set_system_automorphisms.json
results/EXTRA32_SET_SYSTEM_AUTOMORPHISM_REPORT.md
```
