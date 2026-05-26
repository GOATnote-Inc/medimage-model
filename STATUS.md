# STATUS

## Active task
**v0.2 — wire medimage-eval + first dataloader.** The scaffold and the license-preflight gate are merged. Next is connecting the eval substrate as a real consumer and standing up the first dataloader against the manifest schema.

## Exit criteria for current pickup
- `src/medimage_model/eval/runner.py` consumes `medimage_eval.DualJudge` and produces per-manifest eval results
- `src/medimage_model/data/loader.py` reads a permissive-only manifest and yields tensor batches from a hermetic fixture (tiny NIfTI committed under `tests/fixtures/`)
- `make lint` green; `make test` green
- A smoke entry point (`make smoke`) walks: manifest load → loader yield → `DualJudge.evaluate` against a stub model output

## Verify command
```
make lint && make test
```

## Already shipped (do not re-do)
- **PR #1** — `scripts/license_preflight.py` standalone gate, pydantic v2 `DatasetManifest` + `DatasetLicense` schema with SPDX allowlist and forbidden-substring blocklist, OpenNeuro CC0 (`ds002785`) + UCSF-BMSR CC-BY-4.0 seed manifests, e2e subprocess tests against fixtures

## Next-up after this pickup
1. Expand `data/permissive_only/manifests/` with the rest of the OpenNeuro CC0 seed (3-5 more datasets)
2. BraTS-permissive year + open chest corpora (CXR) manifests
3. First contrastive-pretraining smoke run on the seed (CPU stub OK)
4. medimage-eval CSGG reporter integration (once that ships on the substrate side)

## Hard constraints
- **NO CC BY-NC-SA data, ever.** `scripts/license_preflight.py` + pydantic schema both refuse it; CI gates on it.
- Trained weights publish under **NVIDIA Open Model License** (commercial-OK)
- Sibling research-track repo is [`medimage-model-research`](https://github.com/GOATnote-Inc/medimage-model-research) — do NOT cross-pollinate data manifests

## Branch protection
Not yet enabled on this repo. Follow-up: add the four-context baseline (lint, secrets-scan, unit, manifest-determinism) once the dataloader ships.

## Last updated
2026-05-26 — end of scaffolding session (PR #1 merged)
