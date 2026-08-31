# CLAUDE.md — medimage-model operating charter

## Mission
Ship a fully-open, commercial-use-friendly brain-MR multimodal reasoning model. No CC BY-NC-SA contamination anywhere in the data pipeline.

## Non-negotiables

1. **License preflight at ingest.** Every dataset must pass `scripts/license_preflight.py` before being added to `data/permissive_only/`. The preflight refuses any CC BY-NC, CC BY-NC-SA, CC BY-NC-ND, or research-only license.
2. **No `.env` reads.** Judge API keys come from the environment; verify presence with length-only checks, never print values.
3. **Judge pre-flight before any multi-hour eval/train.** Silent judge auth failures poison every reward signal.
4. **No `git add -A`.** Stage by name; data/cache/, checkpoints/, wandb/, eval_outputs/ are artifact-class.
5. **Synthetic data on a leash.** Synthetic samples carry a manifest tag; per-stratum synthetic fraction never exceeds the configured cap without explicit sign-off.
6. **Receipts on every release.** `releases/vX.Y/attestation.json` carries: code commit, data manifest hash, eval results hash, judge versions, seed. Append-only.

## Continuation contract
- Start: read `STATUS.md`.
- End: update `STATUS.md`.

## Cross-repo dependencies
- `medimage-eval` — eval substrate (Apache 2.0).
- `medimage-corpus` — dataset catalog (registry; we consume the manifest, not the data).
- `receipts` (eventually) — attestation ledger.

Sibling research track (do not confuse): `medimage-model-research` uses MR-RATE + CT-RATE and inherits CC BY-NC-SA on weights. This repo does NOT.
