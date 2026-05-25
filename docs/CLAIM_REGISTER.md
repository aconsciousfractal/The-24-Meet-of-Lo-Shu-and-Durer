# Public Claim Register

This register exposes the `M24-C...` and `M24-N...` identifiers cited by the
public manuscript.  It is a reduced public claim register: development-only
roadmap rows are omitted, while every ID cited in the paper is mapped to a
public statement and artifact pointer.

| Statement | Role / status | Claim IDs | Public proof or certificate pointer |
|---|---|---|---|
| The bounded Lo Shu count table is `1,5,13,25,41,25,13,5,1` for sums `3,6,...,27`. | finite proposition | M24-C01, M24-C57 | `results/magic24_certificate_pack.json`; `docs/LO_SHU_LATTICE_POLYGON.md`; tests `test_magic24_certificates.py`, `test_bounded_magic_polytope.py` |
| `Spec^+_{3,9}(15) = {18,21,24,27}`. | finite proposition | M24-C02 | `results/magic24_certificate_pack.json`, section `lo_shu_bounded_spectrum` |
| The `S=24` Lo Shu fiber has 5 bounded squares, while `S=27` is the unique all-9 degenerate fiber. | finite proposition | M24-C03 | `results/magic24_certificate_pack.json`; `docs/STRONG_MEET_THEOREM.md` |
| The Durer/Sagrada ray has terminal `t=10`, terminal sum `24`, inside `[1,16]`. | finite proposition | M24-C04, M24-C51 | `results/magic24_certificate_pack.json`; `results/bounded_magic_polytope.json` |
| The Sagrada mask `2013` is the unique one-incidence Durer mask with terminal sum `24`. | finite proposition | M24-C05, M24-C64 | `results/magic24_certificate_pack.json`; `results/f2_tesseract_analysis.json` |
| `Meet_weak = {24,27}` and `Meet_strong = {24}` under the non-degenerate/terminal rules. | main theorem | M24-C01, M24-C02, M24-C03, M24-C04, M24-C05, M24-C06 | `docs/STRONG_MEET_THEOREM.md`; `docs/LEMMA_SUITE.md` |
| The Durer square has `86` source quaternes summing to `34`, with Sagrada incidence split `19/50/17`. | finite proposition | M24-C07, M24-C08 | `results/magic24_certificate_pack.json`, section `durer_pattern_transport` |
| The terminal square `D(10)` has `96` quaternes summing to `24`, decomposed as `25+50+21` by source sum/incidence. | finite proposition | M24-C09, M24-C117 | `results/magic24_certificate_pack.json`; `results/inside_out_set_system_audit.json` |
| The source target permutation diagonals form an order-8 subgroup isomorphic to `D4`. | finite proposition | M24-C10 | `results/magic24_certificate_pack.json`, section `durer_permutation_diagonals` |
| For every `t>0` along the Sagrada ray, the target permutation diagonals form `V4 = {0123,1032,2301,3210}`. | finite proposition | M24-C11 | `results/magic24_certificate_pack.json`, section `durer_permutation_diagonals` |
| In the Type-A `A3` chamber model, `D4` and `V4` are subgroup/coset tilers but not standard poset cones `L(P)`. | finite proposition / scope theorem | M24-C12, M24-C41, M24-C42, M24-C43, M24-C49 | `docs/TYPE_A_SUBGROUP_TILERS.md`; `docs/TYPE_A_POSET_CONE_COMPARISON.md`; `results/s4_chamber_fingerprints.json`; `results/s4_poset_cone_comparison.json` |
| In the Durer value-minus-one `F2^4` cell model, the cell labeling is a rank-4 linear automorphism. | finite proposition | M24-C73 | `docs/F2_TESSERACT_LAYER.md`; `results/f2_tesseract_analysis.json`; `tests/test_f2_tesseract.py` |
| All 24 permutation diagonals are affine planes in the Durer `F2^4` model. | finite proposition | M24-C74 | `results/f2_tesseract_analysis.json`; `tests/test_f2_tesseract.py` |
| The affine part of `H_34(D)` is exactly `13` balanced directions times `4` cosets, hence `52` affine source quaternes. | finite proposition | M24-C65, M24-C75 | `docs/F2_TESSERACT_LAYER.md`; `results/f2_tesseract_analysis.json` |
| The terminal affine `H_24(D(10))` layer is exactly `9` Sagrada-complementary balanced directions times `4` cosets, hence `36` affine terminal quaternes. | finite proposition | M24-C67, M24-C76, M24-C77 | `docs/F2_TESSERACT_LAYER.md`; `results/f2_tesseract_analysis.json` |
| The terminal affine quaternes are exactly pure transport from source-34, incidence-1 affine planes. | finite proposition | M24-C66, M24-C67, M24-C77 | `results/f2_tesseract_analysis.json`; `tests/test_f2_tesseract.py` |
| `D(10)` is a terminal boundary point but not a vertex of the free-sum or fixed-sum bounded order-4 magic polytope. | guardrail proposition | M24-C52, M24-C56, M24-C63 | `docs/BOUNDED_MAGIC_POLYTOPE.md`; `docs/FIXED_SUM24_POLYTOPE_AUDIT.md`; `results/bounded_magic_polytope.json`; `results/fixed_sum24_polytope_audit.json` |
| The full fixed-sum `S=24` bounded order-4 polytope has dimension `7` and `292` vertices, with `180` integral and `112` semi-integral vertices. | finite proposition / appendix bridge | M24-C60, M24-C61 | `docs/FIXED_SUM24_POLYTOPE_AUDIT.md`; `results/fixed_sum24_polytope_audit.json` |
| The order-4 normal-square extension has `7040` raw squares, `880` essential representatives, and `236` terminal-24 square-mask pairs. | extension proposition | M24-C15, M24-C16, M24-C17 | `data/order4_normal_essential_880.json`; `results/order4_endpoint_spectrum.json` |
| Across terminal-24 pairs, affine cell-value labeling occurs in exactly `144` pairs and equals the exact canonical `V4` terminal subclass. | extension proposition | M24-C78, M24-C79, M24-C80, M24-C139 | `docs/ORDER4_F2_EXTENSION.md`; `docs/EXACT_V4_AFFINE_CLASS_AUDIT.md`; `results/order4_f2_extension.json`; `results/exact_v4_affine_class_audit.json` |
| The main inside-out terminal signature is a broad `176`-pair class: `144` exact canonical `V4` pairs plus `32` structured extras. | extension proposition | M24-C124, M24-C125, M24-C126, M24-C127 | `docs/ORDER4_INSIDE_OUT_PROFILES.md`; `docs/INSIDE_OUT_MAIN_SIGNATURE_SPLIT.md`; `results/order4_inside_out_profiles.json`; `results/inside_out_main_signature_split.json` |
| The selected-mask-affine `176`-pair class splits as `144` cell-affine exact-`V4` pairs plus `32` cell-non-affine non-exact pairs. | exact finite replay / follow-up theorem | M24-C138, M24-C139, M24-C140, M24-C141 | `docs/EXACT_V4_AFFINE_CLASS_AUDIT.md`; `results/exact_v4_affine_class_audit.json` |
