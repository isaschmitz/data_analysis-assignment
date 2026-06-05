"""Spec for the Assignment 1 analysis helpers (student stubs in the assignment)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from spectra_filtering.analysis import (
    summary_stats,
    seasonal_cycle,
    decorrelation_timescale,
)


def test_summary_stats_handles_gaps() -> None:
    data = np.array([1.0, 2.0, 3.0, 4.0, np.nan])
    s = summary_stats(data)
    assert s["n"] == 5
    assert s["n_missing"] == 1
    assert s["mean"] == pytest.approx(2.5)
    assert s["median"] == pytest.approx(2.5)
    assert s["range"] == pytest.approx(3.0)


def test_seasonal_cycle_recovers_annual_signal() -> None:
    t = pd.date_range("2000-01-01", "2009-12-31", freq="D")
    # warm in northern summer (peaks ~July), cold in January
    sig = -np.cos(2 * np.pi * t.dayofyear.values / 365.25)
    clim = seasonal_cycle(t.values, sig, by="month")
    assert set(clim.index) == set(range(1, 13))
    assert {"mean", "median"} <= set(clim.columns)
    assert clim.loc[7, "mean"] > clim.loc[1, "mean"]  # July warmer than January


def test_decorrelation_white_vs_correlated() -> None:
    rng = np.random.default_rng(0)
    dt = 1.0
    n = 20000

    white = rng.standard_normal(n)
    tau_w, ndof_w = decorrelation_timescale(white, dt)

    # AR(1), strongly autocorrelated
    r = 0.95
    ar = np.zeros(n)
    for i in range(1, n):
        ar[i] = r * ar[i - 1] + rng.standard_normal()
    tau_a, ndof_a = decorrelation_timescale(ar, dt)

    assert tau_w < 5 * dt                  # white: short integral scale
    assert ndof_w > 0.3 * n                # white: many independent samples
    assert tau_a > tau_w                   # correlated: longer scale
    assert ndof_a < ndof_w                 # correlated: fewer d.o.f.
