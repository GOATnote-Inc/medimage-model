"""Dataset manifest schema + loader.

Every dataset entering training is described by a JSON manifest under
`data/permissive_only/manifests/`. The schema enforced here is the same
contract that `scripts/license_preflight.py` checks at CI time, so a manifest
that loads cleanly through `load_manifest_dir(...)` is guaranteed to pass
preflight.

The schema is intentionally narrow. It captures what we need for licensing,
provenance, and per-sample tracking — not BIDS metadata, not study-level
demographics, not site-by-site scanner mix. Those live in the dataset itself
or in `medimage-corpus`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# SPDX identifiers + project-specific markers that pass commercial-OK preflight.
ALLOWED_SPDX = frozenset(
    {
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
)

# Substrings that always disqualify a manifest, regardless of other fields.
FORBIDDEN_SUBSTRINGS = (
    "CC-BY-NC",
    "CC-BY-ND",
    "research-only",
    "research_only",
    "PhysioNet-Credentialed",
)


Modality = Literal["MRI", "CT", "X-ray", "Ultrasound", "Pathology", "Dermatology"]
Anatomy = Literal["brain", "chest", "abdomen", "spine", "knee", "skin", "whole-body"]


class DatasetLicense(BaseModel):
    """License block for a single dataset manifest."""

    spdx: str = Field(..., description="SPDX identifier or NVIDIA-Open-Model-License")
    commercial_use: bool = Field(..., description="True if commercial use is allowed")
    share_alike: bool = Field(..., description="True if derivatives must be similarly licensed")
    redistribute: bool = Field(..., description="True if the dataset itself can be redistributed")
    url: str = Field(..., description="Canonical URL of the full license text")

    @field_validator("spdx")
    @classmethod
    def _check_spdx(cls, v: str) -> str:
        v = v.strip()
        for bad in FORBIDDEN_SUBSTRINGS:
            if bad.lower() in v.lower():
                raise ValueError(f"forbidden license token {bad!r} in spdx={v!r}")
        if v not in ALLOWED_SPDX:
            raise ValueError(f"unrecognised SPDX identifier: {v!r} (not on allowlist)")
        return v

    @field_validator("commercial_use")
    @classmethod
    def _commercial_must_be_true(cls, v: bool) -> bool:
        if not v:
            raise ValueError(
                "commercial_use must be true for this repo (use medimage-model-research "
                "for non-commercial corpora)"
            )
        return v


class DatasetManifest(BaseModel):
    """A single dataset manifest, validated at load time."""

    dataset_id: str = Field(..., description="Stable identifier, e.g. 'openneuro:ds000247'")
    name: str = Field(..., description="Human-readable name")
    modality: Modality
    anatomy: Anatomy
    size_volumes: int = Field(..., ge=1, description="Number of imaging volumes")
    license: DatasetLicense
    source_url: str = Field(..., description="Canonical URL of the dataset")
    manifest_version: int = Field(1, description="Schema version for this manifest")
    notes: str = Field("", description="Free-text provenance notes")

    @field_validator("dataset_id")
    @classmethod
    def _dataset_id_format(cls, v: str) -> str:
        if ":" not in v:
            raise ValueError(
                "dataset_id must be in '<source>:<id>' form, e.g. 'openneuro:ds000247'"
            )
        return v


def load_manifest(path: Path) -> DatasetManifest:
    """Load and validate a single manifest file."""
    raw = json.loads(path.read_text())
    return DatasetManifest.model_validate(raw)


def load_manifest_dir(directory: Path) -> list[DatasetManifest]:
    """Load and validate all JSON manifests under `directory`.

    Skips non-JSON files. Raises ValidationError on the first invalid manifest
    so CI gates fail loudly.
    """
    paths = sorted(p for p in directory.glob("*.json"))
    return [load_manifest(p) for p in paths]
