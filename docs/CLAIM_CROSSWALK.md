# Public Claim Crosswalk

This is the public, paper-facing claim map.  It keeps only the statements used
by the paper and omits development-only roadmap rows.  For the resolvable
`M24-C...` and `M24-N...` identifiers cited in the manuscript, see
`docs/CLAIM_REGISTER.md`.

| Paper statement | Public artifact coverage |
|---|---|
| Bounded Lo Shu spectrum and strong-meet inputs | `results/magic24_certificate_pack.json`, `docs/LO_SHU_LATTICE_POLYGON.md` |
| Sagrada one-incidence ray terminality and unique terminal-24 mask | `results/magic24_certificate_pack.json` |
| Quaterne transport `86 -> 50 -> 96` | `results/magic24_certificate_pack.json`, `results/inside_out_set_system_audit.json` |
| `D4 -> V4` permutation-diagonal subgroup drop | `results/magic24_certificate_pack.json` |
| Type-A guardrail: `D4` and `V4` are subgroup/coset chamber tilers, not standard poset cones | `docs/TYPE_A_SUBGROUP_TILERS.md`, `docs/TYPE_A_POSET_CONE_COMPARISON.md`, `results/s4_chamber_fingerprints.json`, `results/s4_poset_cone_comparison.json` |
| Durer value-minus-one model is a rank-4 `F_2^4` affine coordinatization | `docs/F2_TESSERACT_LAYER.md`, `results/f2_tesseract_analysis.json`, `tests/test_f2_tesseract.py` |
| Affine source/terminal transport counts `52 -> 36` | `docs/F2_TESSERACT_LAYER.md`, `results/f2_tesseract_analysis.json` |
| Bounded-polytope non-vertex guardrail | `docs/BOUNDED_MAGIC_POLYTOPE.md`, `docs/FIXED_SUM24_POLYTOPE_AUDIT.md`, `results/bounded_magic_polytope.json`, `results/fixed_sum24_polytope_audit.json` |
| Order-four atlas `7040/880/236`, exact `144`, main `176=144+32` | `data/order4_normal_essential_880.json`, `results/order4_endpoint_spectrum.json`, `results/order4_f2_extension.json`, `results/exact_v4_affine_class_audit.json`, `results/inside_out_main_signature_split.json` |
| Affine-normal-layer explanation of `432`, `3456`, and `24 x 144` | `results/affine_normal_layer.json`, `results/affine_normal_spread_structure.json`, `results/affine_normal_count_derivation.json` |
| O5/Johnson quotient-section and forbidden-shadow refinements | `results/kernel_v4_o5.json`, `results/terminal_parallel_torsor_o5b.json`, `results/six_of_nine_o5c.json`, `results/selected_plane_six_of_nine_o5d.json`, `results/torsor_parametrization_o5e_o5f.json`, `results/johnson_*.json`, `results/o5e_collision_forbidden_shadow_p5.json`, `results/forbidden_shadow_split_p6.json` |

## Blocked Claims

- No universal `24` invariant claim.
- No claim that the terminal square is more perfect than the Durer source.
- No claim that the terminal square is a polytope vertex.
- No claim that `V4` is a Type-A poset cone.
- No claim that `F_2^4` isolates only the historical Durer/Sagrada cell.
- No complete Markov-basis or Hilbert-basis theorem.
- No canonical Lo Shu/N-poset bridge.
