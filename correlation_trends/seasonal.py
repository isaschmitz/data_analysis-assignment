"""Remove the seasonal (annual) cycle with xarray ``groupby`` (worked helper).

The seasonal cycle is a large, deterministic signal. If two series share it, their
cross-correlation peaks near +/-12 months and their trends can be biased -- so it
is usually removed before correlation or trend analysis. The idiom is a
month-of-year ``groupby``: build the monthly climatology, then subtract it.
"""

from __future__ import annotations

import xarray as xr


def seasonal_climatology(da: xr.DataArray, group: str = "TIME.month") -> xr.DataArray:
    """Monthly climatology: the mean annual cycle.

    Parameters
    ----------
    da : xarray.DataArray
        Series with a datetime ``TIME`` coordinate.
    group : str, default "TIME.month"
        Grouping key. ``"TIME.month"`` gives a 12-value climatology; use
        ``"TIME.dayofyear"`` for a daily climatology.

    Returns
    -------
    xarray.DataArray
        The group-mean (e.g. 12 monthly means), indexed by the group label.
    """
    return da.groupby(group).mean()


def remove_seasonal_cycle(da: xr.DataArray, group: str = "TIME.month") -> xr.DataArray:
    """Return the series with its mean annual cycle removed, **mean preserved**.

    Subtract the monthly climatology (which removes the seasonal *departures* and
    the overall mean) and then add the overall mean back, so the deseasonalised
    series sits at the same level as the original -- only the seasonal wiggle is
    gone, not the mean.

    Parameters
    ----------
    da : xarray.DataArray
        Series with a datetime ``TIME`` coordinate.
    group : str, default "TIME.month"
        Grouping key passed to :func:`seasonal_climatology`.

    Returns
    -------
    xarray.DataArray
        ``da`` with the seasonal cycle removed, on the original ``TIME`` axis,
        retaining the original overall mean.

    Examples
    --------
    >>> clim = da.groupby("TIME.month").mean()
    >>> deseasonalised = da.groupby("TIME.month") - clim + da.mean()
    """
    clim = seasonal_climatology(da, group)
    deseason = da.groupby(group) - clim + da.mean()
    
    return deseason

import numpy as np
import xarray as xr


def deseasonalize(da, time_dim="TIME", min_years=2):
    """
    Remove the mean seasonal cycle from a time series.

    Computes the climatological mean for each calendar month (Jan..Dec)
    across all years present, then subtracts it from every timestep of
    that month.

    Parameters
    ----------
    da : xarray.DataArray
        Must have a datetime coordinate along `time_dim`. Works best on
        monthly-resolution data; for finer-resolution data, resample to
        monthly first (e.g. with `align_timeseries` / `.resample()`) so
        each calendar month bin is a single physically meaningful value
        rather than a mix of many sub-monthly samples per month.
    time_dim : str
    min_years : int
        Warn if fewer than this many years of data are available, since
        the climatology gets noisy/unrepresentative with very few years.

    Returns
    -------
    da_deseason : xarray.DataArray
        Same shape as `da`, with the seasonal cycle removed. Also carries
        a new coordinate `{time_dim}.month` dropped again at the end (kept
        internal), and an attribute recording how it was computed.
    climatology : xarray.DataArray
        The 12-point (Jan..Dec) climatological mean, for inspection/plotting.
    """
    times = da[time_dim].to_index()
    n_years = times.year.max() - times.year.min() + 1
    if n_years < min_years:
        print(
            f"Warning: only {n_years} year(s) of data spans '{time_dim}'; "
            f"climatology may be noisy/unrepresentative with so few years."
        )

    # Check for gaps: how many obs per calendar month vs. expected
    counts = da.groupby(f"{time_dim}.month").count(time_dim)
    if counts.min().item() < 2:
        months_low = counts.where(counts < 2, drop=True).month.values
        print(
            f"Warning: calendar month(s) {list(months_low)} have <2 "
            f"observations to average over — their climatology is based "
            f"on a single year and won't represent a true mean cycle."
        )

    climatology = da.groupby(f"{time_dim}.month").mean(time_dim)
    da_deseason = da.groupby(f"{time_dim}.month") - climatology + da.mean(time_dim)
    da_deseason = da_deseason.drop_vars("month", errors="ignore")
    da_deseason.attrs["deseasonalized"] = (
        f"Monthly climatology (mean per calendar month over "
        f"{times.year.min()}-{times.year.max()}) subtracted."
    )

    return da_deseason, climatology
