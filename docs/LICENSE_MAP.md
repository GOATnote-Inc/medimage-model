# License map

## Code
**Apache License 2.0** for everything under `src/`, `scripts/`, `tests/`, `docs/`.

## Training data
This repo ingests **only commercial-use-friendly data**. Every manifest in `data/permissive_only/manifests/` must pass `scripts/license_preflight.py` at every CI run.

### Allowed
| SPDX | Examples | Notes |
|---|---|---|
| `CC0-1.0` | OpenNeuro datasets (default) | Public domain dedication, max permissive |
| `CC-BY-4.0` | UCSF-BMSR | Attribution required |
| `CC-BY-SA-4.0` | some BraTS years | Share-alike but commercial OK |
| `Apache-2.0`, `MIT`, `BSD-*` | various open corpora | Standard permissive |
| `NVIDIA-Open-Model-License` | NV-Generate-MR-Brain | Commercial use OK per NVIDIA |

### Forbidden (preflight rejects)
- Any `CC-BY-NC-*` (e.g. MR-RATE, CT-RATE, VinDr-CXR) — the **research track** repo `medimage-model-research` is the place for those.
- Any `CC-BY-ND-*` — incompatible with training (no derivatives).
- `research-only` / `PhysioNet-Credentialed` / custom-NC licenses.

## Trained model weights
Published per release in `releases/vX.Y/model_card.md` under the **NVIDIA Open Model License** (commercial-OK). This rests on NVIDIA's position that model weights are not copyright-derivative works of training data; we add the further protection that this repo never sees NC data.

## Synthetic samples
NV-Generate-MR-Brain is released under the NVIDIA Open Model License, royalty-free for inference and fine-tuning. Synthetic samples are tagged in the manifest and capped per stratum.
