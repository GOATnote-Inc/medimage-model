"""Hermetic smoke tests."""

from __future__ import annotations

import medimage_model


def test_version_string():
    assert isinstance(medimage_model.__version__, str)
    assert medimage_model.__version__.count(".") >= 2


def test_subpackages_importable():
    from medimage_model import data, eval, models, receipts, safety, serving, training

    for mod in (data, eval, models, receipts, safety, serving, training):
        assert mod is not None
