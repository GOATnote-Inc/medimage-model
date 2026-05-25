"""End-to-end test that scripts/license_preflight.py rejects an NC manifest.

We invoke the preflight as a subprocess against the test fixtures directory
so this is exactly what CI runs.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = REPO_ROOT / "scripts" / "license_preflight.py"


def _run(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(PREFLIGHT), str(target)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_preflight_accepts_good_only_dir(tmp_path: Path):
    good_src = REPO_ROOT / "tests" / "fixtures" / "license_preflight" / "good.json"
    target = tmp_path / "manifests"
    target.mkdir()
    (target / "good.json").write_text(good_src.read_text())

    result = _run(target)
    assert result.returncode == 0, result.stderr
    assert "cleared license preflight" in result.stdout


def test_preflight_rejects_nc_manifest(tmp_path: Path):
    bad_src = REPO_ROOT / "tests" / "fixtures" / "license_preflight" / "bad_nc.json"
    target = tmp_path / "manifests"
    target.mkdir()
    (target / "bad_nc.json").write_text(bad_src.read_text())

    result = _run(target)
    assert result.returncode == 2, result.stdout
    assert "REJECTED" in result.stderr


def test_preflight_handles_missing_dir():
    result = _run(REPO_ROOT / "does-not-exist")
    assert result.returncode == 0
    assert "treating as empty" in result.stdout


def test_preflight_accepts_real_seed_manifests():
    """The actual seed manifests in this repo must pass."""
    target = REPO_ROOT / "data" / "permissive_only" / "manifests"
    result = _run(target)
    assert result.returncode == 0, result.stderr
