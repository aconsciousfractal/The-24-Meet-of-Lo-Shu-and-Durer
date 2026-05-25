# Morse-Hedlund / Prouhet Family Fit

Status: Phase G family-fit test

Certificate:

```text
scripts/analyze_morse_hedlund_family_fit.py
results/morse_hedlund_family_fit.json
results/MORSE_HEDLUND_FAMILY_FIT_REPORT.md
tests/test_morse_hedlund_family_fit.py
```

## Family

The tested family is the displayed Morse-Hedlund/Prouhet-style `4 x 4`
family:

```text
d+k1+k2   a        b        c+k1+k2
c+k1      b+k2     a+k2     d+k1
c+k2      b+k1     a+k1     d+k2
d         a+k1+k2  b+k1+k2 c
```

with constraint:

```text
a+b = c+d
```

The common magic sum is:

```text
2(a+b+k1+k2)
```

## Transform Scope

The local test checks the Durer/Sagrada source, terminal, and direction under:

```text
optional transpose
arbitrary row permutation
arbitrary column permutation
optional value complement x -> 17-x
```

Total transforms checked:

```text
2304
```

This includes the square symmetries as a small subcase.

## Result

In the identity orientation, the Durer-complement source square is exactly in
the family:

```text
a  = 14
b  = 15
c  = 16
d  = 13
k1 = -4
k2 = -8
magic sum = 34
```

So the source Durer-complement square is compatible with the
Morse-Hedlund/Prouhet construction.

The Sagrada terminal point and perturbation direction do not fit:

```text
source fits:    256
terminal fits:    0
direction fits:   0
full ray fits:    0
```

## Interpretation

What may be said:

```text
The Durer-complement source square lies in the displayed Morse-Hedlund/Prouhet family.
```

What may not be said:

```text
The Sagrada bounded ray is a specialization of the Morse-Hedlund/Prouhet family.
The terminal D(10) point is explained by that family.
The endpoint 24 comes from the Morse-Hedlund/Prouhet parametrization.
```

The family is still useful as literature support for the source square, but
the bounded Sagrada descent remains a separate perturbation mechanism.

## Next

Possible follow-up, if useful later:

```text
classify all 880 essential squares by membership in this family under the
same transform scope
```

For the main Magic 24 line, this branch can now be treated as closed with a
guardrail.
