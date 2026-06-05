"""Spec for the estimators students implement.

In the student version these functions raise ``NotImplementedError`` and these
tests fail until they are filled in. Against the solution they all pass.
"""

from __future__ import annotations

import numpy as np
import pytest

from spectra_filtering.spectra import (
    frequency_axis,
    raw_periodogram,
    welch_psd,
    parseval_ratio,
)
from spectra_filtering.leakage import synthetic_tone

DT = 0.5  # days (12-hour grid)


def test_frequency_axis_spans_zero_to_nyquist() -> None:
    """The one-sided axis runs from 0 to the Nyquist frequency (worked helper)."""
    freq = frequency_axis(1000, DT)
    assert freq[0] == 0.0
    assert freq[-1] == pytest.approx(1.0)  # Nyquist for 0.5-day grid


def test_periodogram_satisfies_parseval() -> None:
    """Integrated PSD should equal the series variance to a few percent."""
    rng = np.random.default_rng(0)
    x = rng.standard_normal(4096)
    freq, psd = raw_periodogram(x, DT, detrend=True, window="boxcar")
    assert parseval_ratio(x, freq, psd) == pytest.approx(1.0, rel=0.1)


def test_welch_reduces_variance_relative_to_periodogram() -> None:
    """Welch averaging should produce a far smoother spectrum than the periodogram."""
    rng = np.random.default_rng(1)
    x = rng.standard_normal(8192)
    _, pgram = raw_periodogram(x, DT)
    _, welch = welch_psd(x, DT, segment_length=512, overlap=0.5)
    # crude smoothness proxy: relative scatter of neighbouring bins
    scatter = lambda p: np.std(np.diff(p)) / np.mean(p)
    assert scatter(welch) < scatter(pgram)


def test_tapering_reduces_leakage_for_off_bin_tone() -> None:
    """A Hann taper should lower the spectral floor away from an off-bin tone."""
    n = 2048
    # off-bin frequency: between two FFT bins to provoke leakage
    f0 = (10.5) / (n * DT)
    x = synthetic_tone(f0, n, DT)
    freq, psd_box = raw_periodogram(x, DT, window="boxcar")
    _, psd_hann = raw_periodogram(x, DT, window="hann")
    peak = np.argmax(psd_box)
    far = (freq > freq[peak] * 3)  # well away from the tone
    assert np.median(psd_hann[far]) < np.median(psd_box[far])
