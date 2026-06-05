"""Loading and gap-filling for the RAPID 26N AMOC transport series.

These routines are *worked* — loading and interpolation are mechanical and not the
point of the lecture, so students start from a clean array.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import xarray as xr


def load_moc(
    path: str | Path,
    var: str = "moc_mar_hc10",
) -> tuple[np.ndarray, np.ndarray, float]:
    """Load an AMOC transport series and its sampling interval.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the RAPID ``moc_transports.nc`` file.
    var : str, optional
        Variable name to extract. Default ``"moc_mar_hc10"`` (overturning
        transport, Sv).

    Returns
    -------
    time : numpy.ndarray, dtype ``datetime64[ns]``, shape (N,)
        Time coordinate.
    values : numpy.ndarray, dtype float64, shape (N,)
        Transport in Sv, with gaps still present as ``NaN``.
    dt_days : float
        Median sample spacing in days (0.5 for the 12-hour grid).

    Notes
    -----
    The series carries a small number of ``NaN`` gaps; call :func:`fill_gaps`
    before spectral estimation.
    """
    ds = xr.open_dataset(path)
    da = ds[var]
    time = da["time"].values
    values = da.values.astype("float64")
    dt_days = float(np.median(np.diff(time)) / np.timedelta64(1, "D"))
    return time, values, dt_days


def fill_gaps(values: np.ndarray, method: str = "linear") -> np.ndarray:
    """Fill ``NaN`` gaps in an evenly sampled series by interpolation.

    Parameters
    ----------
    values : numpy.ndarray, shape (N,)
        Series with ``NaN`` at missing samples.
    method : {"linear"}, optional
        Interpolation method. Only linear is implemented (the settled choice for
        this lecture).

    Returns
    -------
    filled : numpy.ndarray, shape (N,)
        Copy of ``values`` with interior gaps linearly interpolated.

    Notes
    -----
    Interpolating across gaps is itself a mild low-pass operation — worth a remark
    in class. Leading/trailing ``NaN`` (none in this dataset) would be left as-is.
    """
    if method != "linear":
        raise ValueError(f"unsupported method: {method!r}")
    filled = np.asarray(values, dtype="float64").copy()
    good = np.isfinite(filled)
    idx = np.arange(filled.size)
    filled[~good] = np.interp(idx[~good], idx[good], filled[good])
    return filled
