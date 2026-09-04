"""Spec for the correlation helpers and the ``cross_correlation`` stub."""

from __future__ import annotations

import numpy as np
import pytest
import matplotlib.pyplot as plt
import correlation_trends.correlation as correlation_module

from correlation_trends.correlation import (
    autocorr,
    integral_timescale,
    integral_timescale_i,
    effective_dof,
    effective_dof_new,
    cross_correlation,
    align_at_lag,
    plot_cc_panel,
)


def _ar1(n: int, r: float, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    a = np.zeros(n)
    a[0] = rng.standard_normal()
    for i in range(1, n):
        a[i] = r * a[i - 1] + rng.standard_normal()
    return a


def test_autocorr_zero_lag_is_one() -> None:
    x = _ar1(2000, 0.6)
    assert autocorr(x)[0] == pytest.approx(1.0)


def test_autocorr_biased_tail_smaller_than_unbiased() -> None:
    x = np.random.default_rng(1).standard_normal(500)
    rb = autocorr(x, biased=True)
    ru = autocorr(x, biased=False)
    # at large lag the unbiased estimate fans out; the biased one is damped
    assert np.abs(rb[-50:]).mean() < np.abs(ru[-50:]).mean()


def test_integral_timescale_orders_white_vs_red() -> None:
    dt = 1.0
    white = np.random.default_rng(2).standard_normal(20000)
    red = _ar1(20000, 0.9, seed=3)
    tau_w = integral_timescale(white, dt)
    tau_r = integral_timescale(red, dt)
    assert tau_w < 5 * dt  # white: short scale
    assert tau_r > tau_w  # correlated: longer scale


def test_effective_dof_is_half_dof_and_smaller_for_red() -> None:
    dt = 1.0
    n = 20000
    white = np.random.default_rng(4).standard_normal(n)
    red = _ar1(n, 0.9, seed=5)
    # EDOF = record / (2 T*) = DOF / 2
    tstar = integral_timescale(white, dt)
    assert effective_dof(white, dt) == pytest.approx((n * dt) / (2 * tstar))
    assert effective_dof(red, dt) < effective_dof(white, dt)


def test_effective_dof_new_returns_sample_effective_dof() -> None:
    x = np.random.default_rng(7).standard_normal(1000)
    assert effective_dof_new(x, 1.0) == pytest.approx(
        effective_dof(x, 1.0), rel=0.1
    )


def test_integral_timescale_i_returns_zero_crossing_index(monkeypatch) -> None:
    monkeypatch.setattr(
        correlation_module, "autocorr", lambda x, biased=True: np.array([1.0, 0.5, -0.2])
    )
    x = np.ones(4)
    assert integral_timescale_i(x, 1.0) == 2


def test_cross_correlation_recovers_known_lag() -> None:
    rng = np.random.default_rng(6)
    n = 4000
    x = rng.standard_normal(n)
    shift = 12
    y = np.roll(x, shift)  # y lags x by `shift` (x leads y)
    lags, r = cross_correlation(x, y)
    assert len(lags) == 2 * n - 1
    # x leads y => peak at negative lag (see sign convention in the docstring)
    assert lags[np.argmax(r)] == -shift
    assert r.max() == pytest.approx(1.0, abs=0.02)


def test_align_at_lag_pairs_shifted_values() -> None:
    x = np.arange(5)
    y = np.arange(5) + 10
    xa, ya = align_at_lag(x, y, 2)
    assert np.array_equal(xa, [2, 3, 4])
    assert np.array_equal(ya, [10, 11, 12])

    xa, ya = align_at_lag(x, y, -2)
    assert np.array_equal(xa, [0, 1, 2])
    assert np.array_equal(ya, [12, 13, 14])


def test_plot_cc_panel_draws_both_panels() -> None:
    x = np.arange(20.0)
    y = np.roll(x, 2)
    fig, (ax_line, ax_scatter) = plt.subplots(1, 2)
    try:
        lag, peak = plot_cc_panel(
            ax_line, ax_scatter, x, y, "Comparison", "x", "y"
        )
        assert lag == -2
        assert peak > 0.7
        assert ax_line.get_title() == "Comparison"
        assert ax_scatter.collections
    finally:
        plt.close(fig)
