"""Tests for time-series alignment and comparison helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from correlation_trends.timeseries import (
    align_series,
    align_timeseries,
    compare_series,
    infer_freq_alias,
    infer_resolution,
)


def _series(start: str, periods: int, freq: str, values=None) -> xr.DataArray:
    time = pd.date_range(start, periods=periods, freq=freq)
    if values is None:
        values = np.arange(periods, dtype=float)
    return xr.DataArray(values, coords={"TIME": time}, dims="TIME")


def test_align_series_intersects_and_sorts_time() -> None:
    a = _series("2000-01-01", 3, "D", [1, 2, 3]).sortby("TIME", ascending=False)
    b = _series("2000-01-02", 3, "D", [10, 20, 30])
    aligned_a, aligned_b = align_series(a, b)
    assert aligned_a.TIME.values.tolist() == aligned_b.TIME.values.tolist()
    assert aligned_a.values.tolist() == [2, 3]
    assert aligned_b.values.tolist() == [10, 20]


def test_align_series_rejects_different_array_shapes() -> None:
    with pytest.raises(ValueError, match="same shape"):
        align_series([1, 2], [1, 2, 3])


def test_compare_series_reports_perfect_relationship() -> None:
    a = _series("2000-01-01", 10, "D")
    b = 2 * a + 1
    result = compare_series(a, b)
    assert result["pearson_r"] == pytest.approx(1.0)
    assert result["slope_y_on_x"] == pytest.approx(2.0)
    assert np.allclose(result["linear_fit"], b.values)


def test_infer_resolution_and_frequency_aliases() -> None:
    da = _series("2000-01-01", 4, "D")
    assert infer_resolution(da) == pd.Timedelta(days=1)
    assert infer_freq_alias(pd.Timedelta(days=30)) == "MS"
    assert infer_freq_alias(pd.Timedelta(days=7)) == "1W"
    assert infer_freq_alias(pd.Timedelta(days=1)) == "1D"
    assert infer_freq_alias(pd.Timedelta(hours=12)) == "12h"
    assert infer_freq_alias(pd.Timedelta(hours=3)) == pd.Timedelta(hours=3)


def test_align_timeseries_resamples_finer_series() -> None:
    coarse = _series("2000-01-01", 4, "D", [0, 1, 2, 3])
    fine = _series(
        "2000-01-01",
        8,
        "12h",
        [0, 0, 1, 1, 2, 2, 3, 3],
    )
    aligned_coarse, aligned_fine = align_timeseries(coarse, fine)
    assert np.array_equal(aligned_coarse.TIME.values, aligned_fine.TIME.values)
    assert np.allclose(aligned_coarse, aligned_fine)
