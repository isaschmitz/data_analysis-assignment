"""Linear trends and their significance for autocorrelated series.

Worked helper: :func:`fit_trend`. Student stub: :func:`trend_with_significance`.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
from numpy.typing import ArrayLike
from scipy import stats

from .correlation import effective_dof_new, autocorr, integral_timescale


class TrendResult(NamedTuple):
    """Result of :func:`trend_with_significance`.

    Attributes
    ----------
    slope, intercept : float
        Least-squares fit coefficients (``x ~ slope * t + intercept``).
    se : float
        Naive OLS standard error of the slope (assumes independent residuals).
    se_eff : float
        Standard error inflated for autocorrelation, ``se * sqrt(N / N_eff)``.
    p_naive, p_eff : float
        Two-sided p-values for ``slope = 0`` using ``se`` (with ``N - 2`` d.o.f.)
        and ``se_eff`` (with ``N_eff - 2`` d.o.f.) respectively.
    n_eff : float
        Effective sample size ``N / (1 + 2 sum rho_k)`` from the residuals.
    t_naive, t_eff : float
        Slope in units of its standard error (``slope / se`` and ``slope / se_eff``)
        -- how many sigma the slope sits from zero. Significant at 95% needs
        ``|t| > ~1.96``.
    """

    slope: float
    intercept: float
    se: float
    se_eff: float
    p_naive: float
    p_eff: float
    n_eff: float
    t_naive: float
    t_eff: float


def fit_trend(t: ArrayLike, x: ArrayLike) -> tuple[float, float]:
    """Least-squares straight-line fit.

    Parameters
    ----------
    t : array_like
        Predictor (e.g. time).
    x : array_like
        Response series.

    Returns
    -------
    slope, intercept : float
        Coefficients of ``x ~ slope * t + intercept``.
    """
    slope, intercept = np.polyfit(np.asarray(t, float), np.asarray(x, float), 1)

    return float(slope), float(intercept)


def trend_with_significance(t: ArrayLike, x: ArrayLike, dt: float) -> TrendResult:
    """Slope, its standard error, ``slope/SE``, and autocorrelation-aware p-values.

    The naive standard error assumes independent residuals. For a red-noise
    series that is optimistic: neighbouring residuals are correlated, so the
    record carries fewer independent samples than ``N``. The honest version
    replaces ``N`` by the effective sample size ``N_eff`` derived from the
    two-sided integral timescale of the residuals, inflating the SE by
    ``sqrt(N / N_eff)``.

    Parameters
    ----------
    t : array_like
        Predictor (time), same units implied by ``dt``.
    x : array_like
        Response series.
    dt : float
        Sample spacing (present for interface symmetry; ``N_eff`` here is a
        sample count and does not depend on ``dt``).

    Returns
    -------
    TrendResult
        Slope, intercept, naive and effective SE, p-values, ``N_eff``, and the
        ``slope/SE`` ratios ``t_naive`` and ``t_eff``.
    """
    t = np.asarray(t, dtype=float)
    x = np.asarray(x, dtype=float)
    if x.size != t.size:
        raise ValueError("t and x must have the same length")
    if x.size < 3:
        raise ValueError("Need at least three samples for a trend fit")

    slope, intercept = fit_trend(t, x)
    trend = slope * t + intercept
    resid = x - trend

    N = x.size
    Sxx = np.sum((t - t.mean()) ** 2)
    se = np.sqrt(np.sum(resid**2) / (N - 2) / Sxx)  # OLS slope SE

    n_eff = effective_dof_new(resid, dt)
    # if n_eff <= 0:
    #     n_eff = 1.0
    se_eff = se * np.sqrt(N / n_eff)

    t_naive = slope / se
    t_eff = slope / se_eff
    p_naive = 2 * stats.t.sf(abs(t_naive), N - 2)
    p_eff = 2 * stats.t.sf(abs(t_eff), max(n_eff - 2, 1))

    return TrendResult(
        slope=float(slope),
        intercept=float(intercept),
        se=float(se),
        se_eff=float(se_eff),
        p_naive=float(p_naive),
        p_eff=float(p_eff),
        n_eff=float(n_eff),
        t_naive=float(t_naive),
        t_eff=float(t_eff),
    )
