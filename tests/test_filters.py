"""Spec for the Butterworth response (a student stub in the assignment version)."""

from __future__ import annotations

import numpy as np
import pytest

from spectra_filtering.filters import butterworth_squared_response

F_CUT = 0.1  # cycles per day (10-day cutoff)


def test_half_power_at_cutoff_single_pass() -> None:
    """Single-pass |H|**2 equals 0.5 at the cutoff frequency."""
    h2 = butterworth_squared_response(np.array([F_CUT]), F_CUT, order=5, zero_phase=False)
    assert h2[0] == pytest.approx(0.5)


def test_response_is_monotonic_and_bounded() -> None:
    """The response decreases monotonically with frequency and stays in [0, 1]."""
    freq = np.linspace(0.0, 1.0, 200)
    h2 = butterworth_squared_response(freq, F_CUT, order=5, zero_phase=True)
    assert np.all((h2 >= 0.0) & (h2 <= 1.0 + 1e-12))
    assert np.all(np.diff(h2) <= 1e-12)


def test_zero_phase_is_steeper_than_single_pass() -> None:
    """Zero-phase (filtfilt) attenuates more in the stopband than a single pass."""
    f = np.array([5.0 * F_CUT])
    single = butterworth_squared_response(f, F_CUT, order=5, zero_phase=False)
    zero = butterworth_squared_response(f, F_CUT, order=5, zero_phase=True)
    assert zero[0] < single[0]
