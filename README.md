# medimage-model

**License-preflight scaffold for a planned commercial-use-friendly brain-MR multimodal model. No weights, training code, or serving code exist yet.**

`medimage-model` is the fully-permissive track of the GOATnote medical imaging stack. Its purpose is to train only on commercial-use-friendly data (OpenNeuro CC0, permissive open corpora, NVIDIA Open Model License synthesis), enforced by a license preflight gate at ingest. Today, the gate and two seed manifests are what exists.

> Status: pre-v0.1 scaffold. There is no model here yet — no checkpoints, no training or serving entry points, no eval adapter. The research-track sibling is [`medimage-model-research`](https://github.com/GOATnote-Inc/medimage-model-research) — same scaffold, different data-license boundary.

## Not for clinical use

Nothing in this repository — and no model eventually published from it — is a medical device or a substitute for clinical judgment. Outputs of any future model must not be used for diagnosis or treatment decisions without a separate, regulated clearance process. See `medimage_model.CLINICAL_DISCLAIMER`, which any future serving path is required to emit.

## Implemented

- **License preflight gate** (`scripts/license_preflight.py`) — SPDX allowlist + forbidden-substring blocklist + `commercial_use` flag check over `data/permissive_only/manifests/`; rejects CC BY-NC-*, CC BY-ND-*, research-only, and PhysioNet-credentialed terms with exit 2; fails closed when the manifest directory is missing or empty. Runs in CI on every push and PR, with a negative NC fixture exercised end-to-end.
- **Manifest schema** (`src/medimage_model/data/manifest.py`) — pydantic v2 `DatasetManifest`/`DatasetLicense` mirror of the gate's contract.
- **Seed manifests** — OpenNeuro `ds002785` (CC0, verified against OpenNeuro metadata) and UCSF-BMSR (recorded as CC BY 4.0; verify on the UCSF portal before this becomes a training input).

## Planned (not yet built)

The intended stack, none of which exists in this repository today:

- Image encoder: MAISI-v2 latents; MedImageInsight / MedSAM2 backbones for other modalities
- Text decoder: Nemotron-3-Nano-30B-A3B via PEFT/LoRA
- Synthesis: NV-Generate-MR-Brain for long-tail augmentation with strata caps and per-sample tagging
- Training: Megatron + SGLang + GRPO with verifiable rewards
- Eval: [`medimage-eval`](https://github.com/GOATnote-Inc/medimage-eval) substrate (declared as a pinned optional extra; not yet consumed by any code here)
- Receipted releases: per-release attestation of code commit, data manifest hash, eval results hash

## Why a parallel commercial-OK track

Most large open medical-imaging paired-report corpora (MR-RATE, CT-RATE) are CC BY-NC-SA. Models trained on them carry a research-only cloud. This track avoids that: every dataset entering training must pass the preflight gate first. See [`docs/LICENSE_MAP.md`](docs/LICENSE_MAP.md).

## Install

Not on PyPI (and there is little to install yet — the package ships the manifest schema and a CLI stub):

```bash
pip install git+https://github.com/GOATnote-Inc/medimage-model.git@main
```

Run the gate:

```bash
python scripts/license_preflight.py data/permissive_only/manifests
```

## License

Code: Apache License 2.0 (full text in `LICENSE`; scope notes in `NOTICE`). Any future trained weights would be released under their own documented license per release. Training-data licenses: see [`docs/LICENSE_MAP.md`](docs/LICENSE_MAP.md).
