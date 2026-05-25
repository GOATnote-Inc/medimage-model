# medimage-model

**Open-source, commercial-use-friendly brain-MR multimodal reasoning model.**

`medimage-model` is the fully-permissive track of the GOATnote medical imaging stack. Trained only on commercial-use-friendly data (OpenNeuro CC0, UCSF-BMSR CC BY 4.0, open chest corpora, NVIDIA Open Model License synthesis) with the [`medimage-eval`](https://github.com/GOATnote-Inc/medimage-eval) substrate as the evaluation contract.

> Status: pre-v0.1 scaffold. The research-track sibling with MR-RATE training is [`medimage-model-research`](https://github.com/GOATnote-Inc/medimage-model-research) — published in parallel under the same substrate, different data-license boundary.

## Why a parallel commercial-OK track

Most large open medical-imaging paired-report corpora (MR-RATE, CT-RATE) are CC BY-NC-SA. Models trained on them carry an unclear-but-cautious "research-only" cloud. This repo deliberately avoids that contamination: every dataset entering training is verified permissive at ingest, and provenance is hashed into the model card.

## Stack

- **Image encoder**: MAISI-v2 latents (NVIDIA Open Model License, commercial-OK) for brain MR; MedImageInsight / MedSAM2 backbones for other modalities.
- **Text decoder**: Nemotron-3-Nano-30B-A3B-BF16 (NVIDIA Open Model License) via PEFT/LoRA on Mamba-2 + MoE projections.
- **Synthesis engine**: NV-Generate-MR-Brain (NVIDIA Open Model License, royalty-free fine-tune) for long-tail augmentation; strata caps + per-sample tagging.
- **Training**: Megatron + SGLang + GRPO (reused from `healthcraft` RL coupling).
- **Eval**: `medimage-eval` substrate (dual-judge κ + shift gauntlet + adjudication + receipts).

## Install (when v0.1 lands)

```bash
pip install medimage-model
```

From source:

```bash
pip install git+https://github.com/GOATnote-Inc/medimage-model.git@main
```

## License

Code: Apache License 2.0. Trained weights: NVIDIA Open Model License (commercial-OK) — released per release in `releases/vX.Y/model_card.md`. Training data licenses: see [`docs/LICENSE_MAP.md`](docs/LICENSE_MAP.md). No CC BY-NC-SA contamination.
