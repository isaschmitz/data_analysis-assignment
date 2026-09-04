"""Tests for the utility functions in ``amoc_analysis.analysis``."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import xarray as xr

from amoc_analysis import analysis


def test_reformat_and_convert_units() -> None:
    ds = xr.Dataset({"speed": ("TIME", [1.0], {"units": "m/s"})})
    assert analysis.reformat_units_var(ds, "speed") == "m s-1"
    assert analysis.convert_units_var(np.array([2.0]), "m/s", "m s-1")[0] == 2.0
    assert analysis.convert_units_var(np.array([2.0]), "m/s", "unknown")[0] == 2.0


def test_get_default_data_dir_points_to_data_folder() -> None:
    assert analysis.get_default_data_dir() == Path(analysis.__file__).resolve().parent.parent / "data"


def test_apply_defaults_supplies_missing_arguments() -> None:
    calls = {}

    @analysis.apply_defaults("source", ["file.nc"])
    def reader(source, file_list):
        calls.update(source=source, file_list=file_list)
        return "loaded"

    assert reader() == "loaded"
    assert calls == {"source": "source", "file_list": ["file.nc"]}


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://example.com/data.nc", True),
        ("ftp://example.com/data.nc", True),
        ("example.com/data.nc", False),
        ("https://example.com", False),
    ],
)
def test_is_valid_url(url: str, expected: bool) -> None:
    assert analysis._is_valid_url(url) is expected


def test_resolve_file_path_prefers_local_and_cache(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    local_file = source / "data.nc"
    local_file.touch()
    assert analysis.resolve_file_path("data.nc", source, None, tmp_path) == local_file

    cached = tmp_path / "cached.nc"
    cached.touch()
    assert analysis.resolve_file_path("cached.nc", None, None, tmp_path) == cached


def test_resolve_file_path_reports_missing_local_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Local file not found"):
        analysis.resolve_file_path("missing.nc", tmp_path, None, tmp_path)


def test_download_file_uses_existing_cache(tmp_path: Path) -> None:
    existing = tmp_path / "data.nc"
    existing.write_bytes(b"data")
    assert analysis.download_file("https://example.com/data.nc", tmp_path) == str(existing)


def test_safe_update_attrs_preserves_unless_overwriting() -> None:
    ds = xr.Dataset(attrs={"existing": "old"})
    result = analysis.safe_update_attrs(
        ds, {"existing": "new", "added": "value"}, verbose=False
    )
    assert result is ds
    assert ds.attrs == {"existing": "old", "added": "value"}
    analysis.safe_update_attrs(ds, {"existing": "new"}, overwrite=True, verbose=False)
    assert ds.attrs["existing"] == "new"
