"""Checks for the worked I/O helpers (these pass out of the box)."""

from __future__ import annotations

import numpy as np

from spectra_filtering.data_io import fill_gaps
from spectra_filtering.filters import nyquist_frequency


def test_nyquist_of_twelve_hour_grid() -> None:
    """A 12-hour (0.5-day) grid has a Nyquist frequency of 1 cycle per day."""
    assert nyquist_frequency(0.5) == 1.0


def test_fill_gaps_removes_interior_nans() -> None:
    """Linear interpolation fills interior gaps and recovers a straight line."""
    x = np.array([0.0, np.nan, 2.0, np.nan, 4.0])
    filled = fill_gaps(x)
    assert np.all(np.isfinite(filled))
    np.testing.assert_allclose(filled, [0.0, 1.0, 2.0, 3.0, 4.0])


def test_fill_gaps_is_noncopy_safe() -> None:
    """The input array is not mutated in place."""
    x = np.array([1.0, np.nan, 3.0])
    _ = fill_gaps(x)
    assert np.isnan(x[1])
