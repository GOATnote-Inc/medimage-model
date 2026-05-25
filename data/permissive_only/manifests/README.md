# permissive_only/manifests

Each JSON file in this directory describes one dataset entering training. `scripts/license_preflight.py` runs against this directory in CI and **refuses to merge** if any manifest carries a non-commercial or research-only license.

See `docs/LICENSE_MAP.md` for the allowed SPDX identifiers. The first PR populates this directory with the OpenNeuro CC0 seed datasets.
