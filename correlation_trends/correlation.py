"""Autocorrelation, decorrelation timescale, and cross-correlation.

Worked helpers: :func:`autocorr`, :func:`integral_timescale`, :func:`effective_dof`.
Student stub: :func:`cross_correlation`.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import signal


def autocorr(x: ArrayLike, biased: bool = True) -> NDArray[np.float64]:
    """One-sided sample autocorrelation ``R(tau)`` with ``R(0) = 1``.

    Parameters
    ----------
    x : array_like
        Input series. Non-finite values are dropped before estimation.
    biased : bool, default True
        If True, normalise each lag by ``N`` (the biased estimator: a triangular
        ``(N - tau)/N`` taper, low variance, positive-definite). If False,
        normalise by ``N - tau`` (unbiased in the mean, but the variance grows
        without bound as ``tau -> N``).

    Returns
    -------
    numpy.ndarray
        ``R(tau)`` for lags ``0, 1, ..., N-1``.

    Notes
    -----
    The biased and unbiased estimates agree at small lag (many pairs) and diverge
    at large lag; the biased tail is damped toward zero while the unbiased tail
    fans out. See the lecture figure comparing white noise, AR(1), and a sinusoid.
    """
    x = np.asarray(x, dtype=np.float64)
    x = x[np.isfinite(x)]          # drop non-finite values, as documented

    d = x - x.mean()
    n, var = d.size, d.var()
    R = np.correlate(d, d, "full")[n - 1:]  # lags 0...n-1
    if biased:
        return R / (n * var)
    return R / ((n - np.arange(n)) * var)

def integral_timescale(x: ArrayLike, dt: float, biased: bool = True) -> float:
    """Integral (decorrelation) timescale ``T*`` by trapezoid to the first zero.

    ``T* = int_0^inf R(tau) dtau``, estimated as the trapezoidal sum of the
    autocorrelation truncated at its first zero crossing. Truncating there keeps
    essentially all the real area while discarding the noisy large-lag tail; for
    the biased estimator this is close to the full integral (the tail is damped).

    Parameters
    ----------
    x : array_like
        Input series.
    dt : float
        Sample spacing, in the time units you want ``T*`` expressed in.
    biased : bool, default True
        Estimator passed to :func:`autocorr`. Biased is recommended.

    Returns
    -------
    float
        The one-sided integral timescale ``T*`` (same units as ``dt``).
    """
    R = autocorr(x, biased=biased)
    tau = 0.0
    i = 0
    while i + 1 < len(R) and R[i] >= 0:
        tau += dt * (R[i] + R[i + 1]) / 2
        i += 1
    return float(tau)

def integral_timescale_i(x: ArrayLike, dt: float, biased: bool = True) -> float:
    """Integral (decorrelation) timescale ``T*`` by trapezoid to the first zero.

    ``T* = int_0^inf R(tau) dtau``, estimated as the trapezoidal sum of the
    autocorrelation truncated at its first zero crossing. Truncating there keeps
    essentially all the real area while discarding the noisy large-lag tail; for
    the biased estimator this is close to the full integral (the tail is damped).

    Parameters
    ----------
    x : array_like
        Input series.
    dt : float
        Sample spacing, in the time units you want ``T*`` expressed in.
    biased : bool, default True
        Estimator passed to :func:`autocorr`. Biased is recommended.

    Returns
    -------
    float
        The one-sided integral timescale ``T*`` (same units as ``dt``).
    """
    R = autocorr(x, biased=biased)
    tau = 0.0
    i = 0
    while i + 1 < len(R) and R[i] >= 0:
        tau += dt * (R[i] + R[i + 1]) / 2
        i += 1
    return i

def effective_dof(x: ArrayLike, dt: float, biased: bool = True) -> float:
    """Effective (equivalent) degrees of freedom ``EDOF`` for a series.

    Following Emery & Thomson, the raw degrees of freedom are
    ``DOF = record / T*`` and the *equivalent* degrees of freedom are
    ``EDOF = DOF / 2 = record / (2 T*)``. Use ``EDOF`` — not ``DOF`` — for error
    bars, confidence intervals, and significance tests: the factor of two comes
    from the two-sided variance sum ``1 + 2 sum rho_k``.

    Parameters
    ----------
    x : array_like
        Input series.
    dt : float
        Sample spacing.
    biased : bool, default True
        Estimator passed through to :func:`integral_timescale`.

    Returns
    -------
    float
        ``EDOF = record / (2 T*)``, where ``record = N * dt``.
    """
    #x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    d = x - x.mean()
    n, var = d.size, d.var()
    R = autocorr(x, biased=biased)
    if x.size == 0:
        return 0.0
    tstar = integral_timescale(x, dt, biased=biased)
    i = integral_timescale_i(x, dt, biased=biased)
    n_eff = n / (1+2*R[1:i].sum())
    record = x.size * dt
    return (record / (2 * tstar))

def effective_dof_new(x: ArrayLike, dt: float, biased: bool = True) -> float:
    """Effective (equivalent) degrees of freedom ``EDOF`` for a series.

    Following Emery & Thomson, the raw degrees of freedom are
    ``DOF = record / T*`` and the *equivalent* degrees of freedom are
    ``EDOF = DOF / 2 = record / (2 T*)``. Use ``EDOF`` — not ``DOF`` — for error
    bars, confidence intervals, and significance tests: the factor of two comes
    from the two-sided variance sum ``1 + 2 sum rho_k``.

    Parameters
    ----------
    x : array_like
        Input series.
    dt : float
        Sample spacing.
    biased : bool, default True
        Estimator passed through to :func:`integral_timescale`.

    Returns
    -------
    float
        ``EDOF = record / (2 T*)``, where ``record = N * dt``.
    """
    #x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    d = x - x.mean()
    n, var = d.size, d.var()
    R = autocorr(x, biased=biased)
    if x.size == 0:
        return 0.0
    tstar = integral_timescale(x, dt, biased=biased)
    i = integral_timescale_i(x, dt, biased=biased)
    n_eff = n / (1+2*R[1:i].sum())
    record = x.size * dt
    return n_eff



def cross_correlation(
    x: ArrayLike, y: ArrayLike
) -> tuple[NDArray[np.int_], NDArray[np.float64]]:
    """Normalised cross-correlation of two series, with the lag axis.

    Both series are standardised (subtract mean, divide by standard deviation)
    and correlated at every integer lag.

    Parameters
    ----------
    x, y : array_like
        Two series of equal length.

    Returns
    -------
    lags : numpy.ndarray
        Integer lags, from ``-(N-1)`` to ``N-1``.
    r : numpy.ndarray
        Cross-correlation at each lag; ``r`` peaks at the lag that best aligns
        the two series.

    Notes
    -----
    Sign convention: the peak sits at the lag by which ``y`` is shifted relative
    to ``x``. If ``y`` lags ``x`` by ``k`` samples (``x`` leads) the peak is at
    ``-k``; so a **negative** peak lag means ``x`` leads ``y``, a positive one
    means ``y`` leads ``x``.
    """
    x = (x - np.mean(x)) / np.std(x)
    y = (y - np.mean(y)) / np.std(y)
    c = signal.correlate(x, y, "full") /len(x)
    lags = signal.correlation_lags(len(x), len(y), "full")
    lag = lags[c.argmax()]
    print(f"Peak cross-correlation at lag {lag}, if negative: x leads y")
    return lags, c

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def align_at_lag(x, y, lag):
    """Return (x_aligned, y_aligned) so that x[n] pairs with y[n - lag]."""
    n = len(x)
    if lag >= 0:
        return x[lag:], y[:n - lag]
    else:
        return x[:n + lag], y[-lag:]

def plot_cc_panel(ax_line, ax_scatter, x, y, title, x_name, y_name):
    lags, c = cross_correlation(x, y)
    peak_idx = np.argmax(c)
    peak_lag, peak_r = lags[peak_idx], c[peak_idx]

    # --- cross-correlation curve ---
    ax_line.plot(lags, c, color="steelblue", lw=1.2)
    ax_line.axvline(peak_lag, color="crimson", ls="--", lw=1)
    ax_line.axhline(0, color="grey", lw=0.6)
    ax_line.plot(peak_lag, peak_r, "o", color="crimson")
    ax_line.annotate(f"lag={peak_lag}, r={peak_r:.2f}",
                      xy=(peak_lag, peak_r), xytext=(6, 6),
                      textcoords="offset points", color="crimson", fontsize=9)
    ax_line.set_title(title)
    ax_line.set_xlabel("Lag (months)")
    ax_line.set_ylabel("Cross-correlation")

    # --- scatter at peak lag ---
    xa, ya = align_at_lag(np.asarray(x), np.asarray(y), peak_lag)
    slope, intercept, r_val, p_val, se = stats.linregress(xa, ya)
    ax_scatter.scatter(xa, ya, s=12, alpha=0.6, color="steelblue")
    xs = np.linspace(xa.min(), xa.max(), 100)
    ax_scatter.plot(xs, slope * xs + intercept, color="crimson", lw=1.5)
    ax_scatter.set_title(f"Aligned at lag={peak_lag} (r={r_val:.2f}, p={p_val:.1e})")
    ax_scatter.set_xlabel(x_name)
    ax_scatter.set_ylabel(f"{y_name} (lag {peak_lag})")

    return peak_lag, peak_r
