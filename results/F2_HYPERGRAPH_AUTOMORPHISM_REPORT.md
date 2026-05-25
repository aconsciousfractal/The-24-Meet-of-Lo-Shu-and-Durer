# F2 Hypergraph Automorphism Report

Status: Phase F colored automorphism audit

## Method

Each hypergraph is encoded as a colored incidence graph with 16 cell
vertices and one edge-node per quaterne.  Automorphisms are graph
automorphisms preserving node kind and color.

## Results

### H34_all

- edges: `86`
- edge colors: `{'edge': 86}`
- automorphism group order: `2`
- cell orbit sizes: `{2: 8}`
- edge orbit sizes: `{1: 28, 2: 29}`
- Sagrada mask orbit count: `2`
- Sagrada mask stabilizer order: `1`
- cycle type profile: `{'1^16': 1, '2^8': 1}`

### H34_affine_colored

- edges: `86`
- edge colors: `{'affine': 52, 'non_affine': 34}`
- automorphism group order: `2`
- cell orbit sizes: `{2: 8}`
- edge orbit sizes: `{1: 28, 2: 29}`
- Sagrada mask orbit count: `2`
- Sagrada mask stabilizer order: `1`
- cycle type profile: `{'1^16': 1, '2^8': 1}`

### H34_affine_only

- edges: `52`
- edge colors: `{'affine': 52}`
- automorphism group order: `384`
- cell orbit sizes: `{16: 1}`
- edge orbit sizes: `{12: 1, 16: 1, 24: 1}`
- Sagrada mask orbit count: `24`
- Sagrada mask stabilizer order: `16`
- cycle type profile: `{'1^16': 1, '1^2 2^1 4^3': 48, '1^4 2^6': 12, '1^4 3^4': 32, '1^8 2^4': 12, '2^2 6^2': 96, '2^8': 51, '4^4': 84, '8^2': 48}`

### H24_all

- edges: `96`
- edge colors: `{'edge': 96}`
- automorphism group order: `16`
- cell orbit sizes: `{1: 8, 2: 4}`
- edge orbit sizes: `{1: 8, 2: 12, 4: 16}`
- Sagrada mask orbit count: `16`
- Sagrada mask stabilizer order: `1`
- cycle type profile: `{'1^10 2^3': 4, '1^12 2^2': 6, '1^14 2^1': 4, '1^16': 1, '1^8 2^4': 1}`

### H24_affine_colored

- edges: `96`
- edge colors: `{'affine': 36, 'non_affine': 60}`
- automorphism group order: `2`
- cell orbit sizes: `{1: 8, 2: 4}`
- edge orbit sizes: `{1: 8, 2: 44}`
- Sagrada mask orbit count: `2`
- Sagrada mask stabilizer order: `1`
- cycle type profile: `{'1^16': 1, '1^8 2^4': 1}`

### H24_source_colored

- edges: `96`
- edge colors: `{'source_24_incidence_0': 25, 'source_34_incidence_1': 50, 'source_44_incidence_2': 21}`
- automorphism group order: `1`
- cell orbit sizes: `{1: 16}`
- edge orbit sizes: `{1: 96}`
- Sagrada mask orbit count: `1`
- Sagrada mask stabilizer order: `1`
- cycle type profile: `{'1^16': 1}`

### H24_source_affine_colored

- edges: `96`
- edge colors: `{'source_24_incidence_0_non_affine': 25, 'source_34_incidence_1_affine': 36, 'source_34_incidence_1_non_affine': 14, 'source_44_incidence_2_non_affine': 21}`
- automorphism group order: `1`
- cell orbit sizes: `{1: 16}`
- edge orbit sizes: `{1: 96}`
- Sagrada mask orbit count: `1`
- Sagrada mask stabilizer order: `1`
- cycle type profile: `{'1^16': 1}`

## Interpretation

- `H34_all` has only the identity and value-complement symmetry.
- The affine sublayer `H34_affine_only` is much more symmetric, with
  group order `384` and transitive action on the 16 labels.
- `H24_all` has a 16-element automorphism group, but affine coloring
  collapses it to order `2`.
- Coloring `H24` by source sum and mask incidence collapses the group
  to the identity.

## Guardrail

The terminal hypergraph has nontrivial uncolored symmetries, but the
transport decomposition `25+50+21` is rigid in the fixed value-label
model.
