# Architecture

Planned architecture for a brain-MR multimodal reasoning model with a clean commercial-use-friendly license chain. None of the layers below exist in this repository yet except the data layer's license preflight gate; this document is the design target, not a description of shipped code.

```
┌────────────────────────────────────────────────────────────┐
│  FHIR DiagnosticReport draft + structured Observations      │
├────────────────────────────────────────────────────────────┤
│  Text decoder: Nemotron-3-Nano-30B-A3B + LoRA (Mamba-2/MoE) │
├────────────────────────────────────────────────────────────┤
│  Image encoder: MAISI-v2 latents (NVIDIA Open Model License)│
│                 + MedImageInsight (MIT-class) baseline      │
├────────────────────────────────────────────────────────────┤
│  Data layer: permissive-only manifests + synthetic-tagged   │
│  samples (NV-Generate-MR-Brain). License preflight gate.    │
├────────────────────────────────────────────────────────────┤
│  Eval: medimage-eval substrate (dual-judge κ, shift, adj.) │
└────────────────────────────────────────────────────────────┘
```

## Training stages
1. **Contrastive image-text pretraining** — align MAISI-v2 latents with report-sentence embeddings.
2. **Supervised report generation** — image → `{findings, impression, comparison, recommendations}`.
3. **GRPO with verifiable rewards** — critical-finding penalties dominate the gradient when missed.

## Why a parallel commercial-OK track
See `docs/LICENSE_MAP.md`. The research-track sibling repo `medimage-model-research` is architecturally identical but ingests MR-RATE / CT-RATE and therefore inherits CC BY-NC-SA on weights. Both repos publish through the same `medimage-eval` substrate so results are directly comparable.
