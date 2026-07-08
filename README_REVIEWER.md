# Reviewer Guide

Companion documentation added 2026-07-08, after publication; it does not
modify the paper.

## Ten-Minute Path

1. Read `docs/CLAIM_REGISTER.md` — every claim ID cited by the manuscript
   (M24-C.../M24-N...) mapped to a public statement, role/status, and
   certificate pointer.
2. Read `docs/EXECUTABLE_REPLAY_SCOPE.md` — what is included as replay and,
   critically, the four "Not Included As Claims" items.
3. Spot-open one certificate: `results/magic24_certificate_pack.json`
   (e.g. section `lo_shu_bounded_spectrum` vs register row M24-C02).

## Thirty-Minute Path

4. Run the test suite: `python -m pytest -q`
   (148 tests, ~4 min; green on 2026-07-08).
5. Follow one full chain: register row → docs note (e.g.
   `docs/STRONG_MEET_THEOREM.md`) → results JSON → test file.
6. Read `docs/CLAIM_CROSSWALK.md` for the manuscript-to-register mapping.
7. Read `docs/PUBLIC_CLAIM_BOUNDARY.md` for the quoting boundary.

## Main Claims

- Meet_weak = {24, 27}, Meet_strong = {24} under the stated rules (main
  theorem row).
- A large set of registered finite propositions with per-row certificate
  pointers (bounded spectra, retraction shadow, tesseract layer, polytope
  audits, endpoint-24 atlas).

## Known Limits

- The four explicitly-excluded claim families in
  `docs/EXECUTABLE_REPLAY_SCOPE.md`.
- Register roles are the claim-strength authority; guardrail rows carry
  their own negative scopes.
- No git tags; cite by commit (HEAD at retrofit: cf52df8).
