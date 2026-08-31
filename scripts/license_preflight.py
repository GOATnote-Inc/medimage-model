#!/usr/bin/env python3
"""License preflight gate.

Walks a manifest directory and refuses to proceed if any dataset is licensed
under a non-commercial or research-only term. The substrate of the entire
commercial-OK promise of `medimage-model` rests on this gate.

Allowed licenses (SPDX identifiers, case-insensitive):
  - CC0-1.0
  - CC-BY-4.0          (commercial OK with attribution)
  - CC-BY-3.0
  - CC-BY-SA-4.0       (share-alike but still commercial-OK)
  - CC-BY-SA-3.0
  - Apache-2.0
  - MIT
  - BSD-3-Clause
  - BSD-2-Clause
  - NVIDIA-Open-Model-License (NVIDIA-blessed commercial use)

Refused (any of these flips exit 2):
  - CC-BY-NC-*         (NC = non-commercial)
  - CC-BY-ND-*         (ND = no derivatives; incompatible with training)
  - "research-only"
  - "PhysioNet-Credentialed" (gated commercial)
  - any custom license whose 'commercial_use' field is false

Usage:
    python scripts/license_preflight.py <manifest_dir>

Manifest schema (JSON, one dataset per file):
{
  "dataset_id": "openneuro:ds000247",
  "name": "...",
  "modality": "MRI",
  "anatomy": "brain",
  "size_volumes": 100,
  "license": {
    "spdx": "CC0-1.0",
    "commercial_use": true,
    "share_alike": false,
    "redistribute": true,
    "url": "https://creativecommons.org/publicdomain/zero/1.0/"
  },
  "source_url": "https://openneuro.org/datasets/ds000247",
  "manifest_version": 1
}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_SPDX = {
    "CC0-1.0",
    "CC-BY-4.0",
    "CC-BY-3.0",
    "CC-BY-SA-4.0",
    "CC-BY-SA-3.0",
    "Apache-2.0",
    "MIT",
    "BSD-3-Clause",
    "BSD-2-Clause",
    "NVIDIA-Open-Model-License",
}

FORBIDDEN_SUBSTRINGS = (
    "CC-BY-NC",
    "CC-BY-ND",
    "research-only",
    "research_only",
    "PhysioNet-Credentialed",
)


def _classify(license_obj: dict) -> tuple[bool, str]:
    spdx = str(license_obj.get("spdx", "")).strip()
    if not spdx:
        return False, "missing 'spdx' field"

    for bad in FORBIDDEN_SUBSTRINGS:
        if bad.lower() in spdx.lower():
            return False, f"forbidden license token: {spdx!r}"

    if spdx not in ALLOWED_SPDX:
        return False, f"unrecognised SPDX identifier: {spdx!r} (not on allowlist)"

    if license_obj.get("commercial_use") is False:
        return False, "license declares commercial_use=false"

    return True, spdx


def _check_one(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return [f"{path}: invalid JSON ({e})"]

    if "license" not in data:
        return [f"{path}: missing 'license' object"]

    ok, detail = _classify(data["license"])
    if not ok:
        errors.append(f"{path}: REJECTED — {detail}")
    else:
        dataset_id = data.get("dataset_id", "<unknown>")
        print(f"OK  {dataset_id:40s} license={detail}")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: license_preflight.py <manifest_dir>", file=sys.stderr)
        return 64
    root = Path(argv[1])
    if not root.exists():
        # Fail closed: a missing directory means nothing was checked. A path
        # typo must never green the gate that the commercial-OK promise rests on.
        print(f"FAILED: manifest dir does not exist: {root}", file=sys.stderr)
        return 2

    manifests = sorted(root.glob("*.json"))
    if not manifests:
        # Fail closed for the same reason: zero manifests checked is not a pass.
        print(f"FAILED: no manifests found under {root}", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    for path in manifests:
        all_errors.extend(_check_one(path))

    if all_errors:
        print("", file=sys.stderr)
        for e in all_errors:
            print(e, file=sys.stderr)
        print(f"\nFAILED: {len(all_errors)} manifest(s) rejected", file=sys.stderr)
        return 2

    print(f"\nOK: {len(manifests)} manifest(s) cleared license preflight")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
