"""Generic tools for comparing and regressing time series.

The functions here are intentionally generic so the same analysis can be reused for
RAPID transport series, geostrophic estimates, and any other pair of comparable
observations. For RAPID work the series are usually xarray DataArrays with a
``TIME`` coordinate.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import xarray as xr

from .correlation import cross_correlation
from .trends import fit_trend


def align_series(
    series_a: xr.DataArray | Any,
    series_b: xr.DataArray | Any,
    time_name: str = "TIME",
) -> tuple[xr.DataArray, xr.DataArray]:
    """Align two series on their common time coordinate.

    Parameters
    ----------
    series_a, series_b : xarray.DataArray or array-like
        Two series with a valid time coordinate, or 1D arrays with equivalent
        lengths and a common time axis.
    time_name : str, default "TIME"
        Coordinate name used for xarray Series.

    Returns
    -------
    a_aligned, b_aligned : xarray.DataArray
        Series filtered to the common time points and sorted in time order.
    """
    if isinstance(series_a, xr.DataArray) and isinstance(series_b, xr.DataArray):
        time = np.intersect1d(series_a[time_name].values, series_b[time_name].values)
        a = series_a.sel({time_name: time}).sortby(time_name)
        b = series_b.sel({time_name: time}).sortby(time_name)
        return a, b

    a = np.asarray(series_a, dtype=float)
    b = np.asarray(series_b, dtype=float)
    if a.shape != b.shape:
        raise ValueError("series_a and series_b must have the same shape for array inputs")
    return xr.DataArray(a), xr.DataArray(b)


def compare_series(
    series_a: xr.DataArray | Any,
    series_b: xr.DataArray | Any,
    time_name: str = "TIME",
    *,
    remove_seasonal: bool = False,
) -> dict[str, Any]:
    """Return the key statistical comparison between two series.

    The function is deliberately generic: it can compare any pair of time series
    after aligning them in time and optionally removing the mean annual cycle.

    Returns
    -------
    dict
        Keys include ``time``, ``a``, ``b``, ``pearson_r``, ``lag``, ``lagged_r``,
        ``slope``, ``intercept``, ``trend_line`` and ``covariance``.
    """
    a, b = align_series(series_a, series_b, time_name=time_name)

    if remove_seasonal and hasattr(a, time_name):
        from .seasonal import remove_seasonal_cycle

        a = remove_seasonal_cycle(a)
        b = remove_seasonal_cycle(b)

    a_vals = np.asarray(a.values, dtype=float)
    b_vals = np.asarray(b.values, dtype=float)
    mask = np.isfinite(a_vals) & np.isfinite(b_vals)
    a_vals = a_vals[mask]
    b_vals = b_vals[mask]

    if a_vals.size < 2:
        raise ValueError("The aligned series do not contain enough finite values")

    corr = np.corrcoef(a_vals, b_vals)[0, 1]
    slope, intercept = fit_trend(np.arange(a_vals.size), a_vals)
    slope_y, intercept_y = fit_trend(a_vals, b_vals)

    lags, lag_corr = cross_correlation(a_vals, b_vals)
    peak_idx = int(np.argmax(lag_corr))
    best_lag = int(lags[peak_idx])

    return {
        "time": a[time_name].values[mask] if hasattr(a, time_name) else np.arange(a_vals.size),
        "a": a_vals,
        "b": b_vals,
        "pearson_r": float(corr),
        "lag": best_lag,
        "lagged_r": float(lag_corr[peak_idx]),
        "slope_vs_index": float(slope),
        "intercept_vs_index": float(intercept),
        "slope_y_on_x": float(slope_y),
        "intercept_y_on_x": float(intercept_y),
        "linear_fit": slope_y * a_vals + intercept_y,
        "lags": lags,
        "cross_corr": lag_corr,
    }

import numpy as np
import pandas as pd
import xarray as xr


def infer_resolution(da, time_dim="TIME"):
    """Median timestep of a DataArray's time coordinate, as a pandas Timedelta."""
    times = pd.to_datetime(da[time_dim].values)
    diffs = np.diff(times)
    return pd.Timedelta(np.median(diffs))


def infer_freq_alias(res: pd.Timedelta):
    """Map a Timedelta to a sensible pandas resample rule.

    Falls back to the raw Timedelta (a fixed-width offset) if it doesn't
    look like a standard calendar frequency.
    """
    days = res / pd.Timedelta(days=1)
    if 27 <= days <= 31:
        return "MS"      # monthly (calendar-aware, not a fixed 30D)
    if 6.5 <= days <= 7.5:
        return "1W"
    if 0.9 <= days <= 1.1:
        return "1D"
    if 0.4 <= days <= 0.6:
        return "12h"
    return res            # unrecognised cadence: use as a fixed-width offset


def align_timeseries(x, y, time_dim="TIME", tolerance=None):
    """
    Align two xarray DataArrays of possibly different native resolution.

    - Identifies which of x, y is coarser (larger median timestep).
    - Resamples the finer series down to the coarser series' frequency (mean).
    - Reindexes onto the coarser series' exact timestamps using nearest-
      neighbour matching, so a fixed anchor offset (e.g. resample() landing
      on 00:00 on the 1st when the coarse series sits at 12:00) doesn't
      break the match.
    - Drops any timestep that couldn't be matched within `tolerance`.
    - Asserts the two outputs end up with identical shape and timestamps.

    Parameters
    ----------
    x, y : xarray.DataArray
    time_dim : str
    tolerance : pandas.Timedelta, optional
        Max allowed offset when snapping onto the coarse grid.
        Defaults to half the coarse series' resolution.

    Returns
    -------
    x_aligned, y_aligned : xarray.DataArray, same shape and timestamps.
    """
    res_x = infer_resolution(x, time_dim)
    res_y = infer_resolution(y, time_dim)

    x_is_coarser = res_x >= res_y
    coarse, fine = (x, y) if x_is_coarser else (y, x)
    coarse_res, fine_res = (res_x, res_y) if x_is_coarser else (res_y, res_x)

    if tolerance is None:
        tolerance = coarse_res / 2

    freq = infer_freq_alias(coarse_res)
    fine_resampled = fine.resample({time_dim: freq}).mean()

    fine_aligned = fine_resampled.reindex(
        {time_dim: coarse[time_dim]}, method="nearest", tolerance=tolerance
    )

    merged = xr.merge(
        [coarse.rename("coarse"), fine_aligned.rename("fine")], join="inner"
    ).dropna(dim=time_dim)

    coarse_aligned, fine_aligned = merged["coarse"], merged["fine"]
    x_aligned, y_aligned = (
        (coarse_aligned, fine_aligned) if x_is_coarser else (fine_aligned, coarse_aligned)
    )

    # --- checks ---
    assert x_aligned.shape == y_aligned.shape, (
        f"Alignment failed: shapes differ ({x_aligned.shape} vs {y_aligned.shape})"
    )
    assert np.array_equal(x_aligned[time_dim].values, y_aligned[time_dim].values), (
        "Alignment failed: timestamps don't match after alignment"
    )

    print(
        f"Resampled finer series ({fine_res}) -> {coarse_res} "
        f"(tolerance {tolerance}); aligned shape: {x_aligned.shape}"
    )

    return x_aligned, y_aligned