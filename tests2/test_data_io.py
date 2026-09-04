"""Tests for data loaders using a mocked ``amocatlas`` reader."""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import xarray as xr

from correlation_trends import data_io


def _install_fake_reader(monkeypatch, **readers) -> None:
    monkeypatch.setitem(
        __import__("sys").modules,
        "amocatlas",
        SimpleNamespace(read=SimpleNamespace(**readers)),
    )


def test_load_amoc_gap_fills_transport_series(monkeypatch) -> None:
    ds = xr.Dataset(
        {
            name: ("TIME", [1.0, np.nan, 3.0])
            for name in ("MOC", "TRANS_FC", "TRANS_EKMAN", "TRANS_UMO")
        },
        coords={"TIME": np.array(["2000-01-01", "2000-01-03", "2000-01-05"], dtype="datetime64[D]")},
    )
    _install_fake_reader(monkeypatch, rapid=lambda: ds)
    time, dt, series = data_io.load_amoc()
    assert time.size == 3
    assert dt == 2.0
    assert np.array_equal(series["MOC"], [1.0, 2.0, 3.0])


def test_load_ts_gridded_unwraps_single_item_list(monkeypatch) -> None:
    ds = xr.Dataset()
    _install_fake_reader(monkeypatch, rapid=lambda **kwargs: [ds])
    assert data_io.load_ts_gridded("cache") is ds


def test_load_moc_sigma0_26n_extracts_time_and_values(monkeypatch) -> None:
    ds = xr.Dataset(
        {"MOC_SIGMA0": ("TIME", [1, 2])},
        coords={"TIME": np.array(["2000-01-01", "2000-01-02"], dtype="datetime64[D]")},
    )
    _install_fake_reader(monkeypatch, rapid=lambda **kwargs: ds)
    time, values = data_io.load_moc_sigma0_26n("cache")
    assert time.size == 2
    assert np.array_equal(values, [1.0, 2.0])


def test_load_47n_accepts_dataset_output(monkeypatch) -> None:
    ds = xr.Dataset(
        {"Trans vol [Sv]": ("TIME", [4, 5])},
        coords={"TIME": np.array(["2000-01-01", "2000-02-01"], dtype="datetime64[D]")},
    )
    _install_fake_reader(monkeypatch, read_47n=lambda: ds)
    _, values = data_io.load_47n()
    assert np.array_equal(values, [4.0, 5.0])
