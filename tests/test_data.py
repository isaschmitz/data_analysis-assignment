import pytest
import xarray as xr

from amoc_analysis import data


def test_load_sample_dataset_rapid():
    ds = data.load_sample_dataset("rapid")
    assert isinstance(ds, xr.Dataset), "Expected an xarray.Dataset"
    assert "TIME" in ds or "time" in ds, "Dataset should have a TIME or time coordinate"
    time_dim = "TIME" if "TIME" in ds.dims else "time"
    assert time_dim in ds.dims, "Dataset should have a TIME or time dimension"
    assert ds.sizes[time_dim] > 0, f"{time_dim} dimension should not be empty"
    assert "moc_mar_hc10" in ds, "Expected variable moc_mar_hc10 in RAPID dataset"


def test_load_sample_dataset_invalid_array():
    with pytest.raises(
        ValueError,
        match="Sample dataset for array 'invalid' is not defined",
    ):
        data.load_sample_dataset("invalid")


def test_load_dataset_invalid_array():
    with pytest.raises(ValueError, match="Unknown array name: invalid"):
        data.load_dataset("invalid")


@pytest.mark.parametrize(
    "array_name, expected_var",
    [
        ("rapid", "moc_mar_hc10"),
    ],
)
def test_load_dataset(array_name, expected_var):
    datasets = data.load_dataset(array_name)
    assert isinstance(datasets, list), f"{array_name} should return a list of datasets"
    assert len(datasets) > 0, f"{array_name} dataset list should not be empty"

    for ds in datasets:
        assert isinstance(
            ds,
            xr.Dataset,
        ), f"Each dataset for {array_name} should be an xarray.Dataset"
        assert (
            "TIME" in ds or "time" in ds
        ), f"{array_name} dataset should have TIME or time coordinate"
        assert (
            expected_var in ds
        ), f"{array_name} dataset should contain variable {expected_var}"
        assert (
            "source_file" in ds.attrs
        ), f"{array_name} dataset should include 'source_file' metadata"
        assert (
            "project" in ds.attrs
        ), f"{array_name} dataset should include 'project' metadata"


def test_save_dataset_creates_file(tmp_path):
    # Create a dummy dataset
    ds = xr.Dataset(
        {
            "mock_variable": (
                ["x"],
                [1.0, 2.0, 3.0],
                {"units": "Sv", "comment": "Mock transport"},
            )
        },
        coords={"x": [0, 1, 2]},
    )
    outfile = tmp_path / "test.nc"

    success = data.save_dataset(
        ds, output_file=outfile, delete_existing=True, prompt_user=False
    )
    assert success
    assert outfile.exists()


def test_save_dataset_skips_when_file_exists_and_no_delete(tmp_path):
    # Create a dummy dataset
    ds = xr.Dataset(
        {
            "mock_variable": (
                ["x"],
                [1.0, 2.0, 3.0],
                {"units": "Sv", "comment": "Mock transport"},
            )
        },
        coords={"x": [0, 1, 2]},
    )
    outfile = tmp_path / "test_exists.nc"

    # First save
    data.save_dataset(ds, output_file=outfile, delete_existing=False, prompt_user=False)

    # Try again without delete or prompt
    success = data.save_dataset(
        ds, output_file=outfile, delete_existing=False, prompt_user=False
    )

    assert not success
    assert outfile.exists()