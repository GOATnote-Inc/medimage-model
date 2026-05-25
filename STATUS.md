# STATUS

## Active task
**Bootstrap v0.1 scaffold.** Land the permissive-data manifest schema + license preflight gate + a green CI baseline. No training yet.

## Exit criteria for current pickup
- `make lint` green
- `make test` green (hermetic)
- `scripts/license_preflight.py` refuses a fixture CC BY-NC-SA manifest and accepts a fixture CC0 manifest
- `data/permissive_only/manifests/openneuro_seed.json` lists the seed OpenNeuro datasets with license=`CC0-1.0`

## Verify command
```
make lint && make test
```

## Next-up after pickup
1. Wire `medimage-eval` substrate as a real dependency.
2. Add UCSF-BMSR + BraTS-permissive manifests.
3. Stand up the data loader against the manifest schema.
4. First contrastive-pretraining smoke run on the local seed.

## Known blockers
None.

## Last updated
2026-05-25 — initial scaffold
