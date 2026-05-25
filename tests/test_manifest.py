"""Manifest schema + loader tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from medimage_model.data.manifest import (
    DatasetManifest,
    load_manifest,
    load_manifest_dir,
)

FIXTURES = Path(__file__).parent / "fixtures" / "license_preflight"
SEED_MANIFESTS = Path(__file__).parents[1] / "data" / "permissive_only" / "manifests"


def test_seed_manifests_validate():
    """Every JSON in data/permissive_only/manifests must pass the schema."""
    manifests = load_manifest_dir(SEED_MANIFESTS)
    assert manifests, "no seed manifests on disk"
    for m in manifests:
        assert m.license.commercial_use is True
        assert ":" in m.dataset_id


def test_good_fixture_loads():
    m = load_manifest(FIXTURES / "good.json")
    assert m.dataset_id == "test:good"
    assert m.license.spdx == "CC0-1.0"
    assert m.license.commercial_use is True


def test_bad_nc_fixture_rejected():
    with pytest.raises(ValidationError) as ei:
        load_manifest(FIXTURES / "bad_nc.json")
    msg = str(ei.value)
    assert "CC-BY-NC" in msg or "commercial_use" in msg


def test_schema_rejects_missing_colon_in_id():
    raw = {
        "dataset_id": "noprefix",
        "name": "n",
        "modality": "MRI",
        "anatomy": "brain",
        "size_volumes": 1,
        "license": {
            "spdx": "CC0-1.0",
            "commercial_use": True,
            "share_alike": False,
            "redistribute": True,
            "url": "https://example.invalid",
        },
        "source_url": "https://example.invalid",
        "manifest_version": 1,
    }
    with pytest.raises(ValidationError):
        DatasetManifest.model_validate(raw)


def test_schema_rejects_unknown_spdx():
    raw = {
        "dataset_id": "test:bad-spdx",
        "name": "n",
        "modality": "MRI",
        "anatomy": "brain",
        "size_volumes": 1,
        "license": {
            "spdx": "Proprietary-1.0",
            "commercial_use": True,
            "share_alike": False,
            "redistribute": True,
            "url": "https://example.invalid",
        },
        "source_url": "https://example.invalid",
        "manifest_version": 1,
    }
    with pytest.raises(ValidationError) as ei:
        DatasetManifest.model_validate(raw)
    assert "Proprietary-1.0" in str(ei.value)


def test_schema_rejects_zero_volumes():
    raw = {
        "dataset_id": "test:empty",
        "name": "n",
        "modality": "MRI",
        "anatomy": "brain",
        "size_volumes": 0,
        "license": {
            "spdx": "CC0-1.0",
            "commercial_use": True,
            "share_alike": False,
            "redistribute": True,
            "url": "https://example.invalid",
        },
        "source_url": "https://example.invalid",
        "manifest_version": 1,
    }
    with pytest.raises(ValidationError):
        DatasetManifest.model_validate(raw)
