"""Spec for the geostrophic-transport helpers, on the real RAPID hydrography.

These tests read ``ts_gridded.nc`` (via amocatlas / the local ``data`` dir) and
require ``gsw``. They are skipped if the data cannot be loaded (e.g. offline with
no cached file).
"""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("gsw")
from correlation_trends.data_io import load_amoc, load_ts_gridded
from correlation_trends.geostrophy import (
    _fill_profiles,
    dynamic_height,
    interior_geostrophic_transport,
    to_teos10,
)


@pytest.fixture(scope="module")
def ts():
    try:
        return load_ts_gridded()
    except Exception as exc:  # pragma: no cover - environment dependent
        pytest.skip(f"ts_gridded unavailable: {exc}")


def test_interior_transport_is_southward_and_finite(ts) -> None:
    trans = interior_geostrophic_transport(ts.isel(TIME=slice(0, 2000)))
    v = trans.values
    assert np.isfinite(v).all()
    assert trans.attrs["units"] == "Sv"
    assert np.nanmean(v) < 0  # interior flow is southward


def test_interior_transport_tracks_trans_umo(ts) -> None:
    n = 2000
    trans = interior_geostrophic_transport(ts.isel(TIME=slice(0, n)))
    _, _, series = load_amoc()
    umo = series["TRANS_UMO"][:n]
    m = np.isfinite(trans.values) & np.isfinite(umo)
    r = np.corrcoef(trans.values[m], umo[m])[0, 1]
    assert r > 0.6  # upper mid-ocean estimate tracks TRANS_UMO well


def test_fill_profiles_interpolates_each_time_column() -> None:
    pressure = np.array([0.0, 100.0, 200.0])
    values = np.array([[1.0, 2.0], [np.nan, 4.0], [5.0, np.nan]])
    filled = _fill_profiles(values, pressure)
    assert np.array_equal(filled[:, 0], [1.0, 3.0, 5.0])
    assert filled[2, 1] == 4.0  # endpoint gaps use the nearest valid value


def test_to_teos10_returns_finite_arrays() -> None:
    sa, ct = to_teos10([20.0, 10.0], [35.0, 35.2], [0.0, 1000.0], -40.0, 26.5)
    assert sa.shape == ct.shape == (2,)
    assert np.isfinite(sa).all()
    assert np.isfinite(ct).all()


def test_dynamic_height_is_zero_at_reference_pressure() -> None:
    pressure = np.array([0.0, 1000.0, 2000.0])
    sa = np.full(pressure.shape, 35.0)
    ct = np.full(pressure.shape, 5.0)
    height = dynamic_height(sa, ct, pressure, p_ref=2000.0)
    assert height[-1] == pytest.approx(0.0, abs=1e-10)
