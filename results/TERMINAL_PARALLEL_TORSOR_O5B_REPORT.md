# Terminal Parallel-Class Torsor

Status: Phase O5b follow-up audit, outside the paper

## Question

After Phase O5 ruled out direct equality of the two `V4` objects,
does the terminal translation `V4` still define a torsor over the
selected terminal value plane?

## Certified Answer

Yes, and the statement is broader than terminal-24.  Across the
full globally affine square-mask layer, the four fixed translation
diagonals map to four cosets of one balanced value direction.  The
selected value plane is a transversal to those cosets.  In the
full-translation terminal subclass, this fixed translation `V4` is
the terminal `V4`.

Full affine-layer counters:

- all affine square-mask records: `3456`
- translation directions balanced: `{'True': 3456}`
- translation direction complementary to selected direction: `{'True': 3456}`
- transversal intersection patterns: `{'(1, 1, 1, 1)': 3456}`
- translation-to-selected point map affine: `{'True': 3456}`

Full-translation terminal-subclass counters:

- full-translation records: `1968`
- terminal torsor affine maps: `{'True': 1968}`

Terminal-24 exact-`V4` counters:

- selected direction distribution: `{'0,1,4,5': 144}`
- terminal direction distribution: `{'0,3,12,15': 24, '0,3,13,14': 24, '0,6,11,13': 24, '0,6,9,15': 24, '0,7,11,12': 24, '0,7,9,14': 24}`
- terminal directions balanced: `{'True': 144}`
- terminal direction complementary to selected direction: `{'True': 144}`
- transversal intersection patterns: `{'(1, 1, 1, 1)': 144}`
- terminal-to-selected point map bijective: `{'True': 144}`
- terminal-to-selected point map affine: `{'True': 144}`

Thus the map

```text
terminal translation label -> unique point of P in the corresponding W-coset
```

is an affine bijection for every terminal-24 exact-`V4` record, and
the same fixed-translation torsor statement holds for all `3456`
globally affine square-mask pairs.

## Kernel Guardrail

The value-bit kernel is still not the terminal translation group:

- kernel setwise stabilizer sizes: `{'2': 144}`
- kernel setwise point-orbit sizes on P: `{'(1, 1, 2)': 144}`
- full kernel orbit size on selected planes: `{'2': 144}`

Only a size-2 subgroup of the value-bit kernel stabilizes the selected
plane, and its point-orbit pattern is `(1,1,2)`, not a transitive
`V4` action on the four points.

## Interpretation

The correct structure is a quotient-section relation in `F2^4`: the
selected value plane is a section for the quotient by the balanced
translation-image direction.  When the terminal set is the full
translation subgroup, the terminal translation `V4` is identified
with the four quotient cosets through this section.
