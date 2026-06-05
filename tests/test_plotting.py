import numpy as np
import pytest
import xarray as xr

from amoc_analysis import plotting


def create_dummy_dataset():
    """Create a dummy dataset for testing plotting functions."""
    time = np.arange("2004-01-01", "2005-01-01", dtype="datetime64[D]")
    transport = np.sin(np.arange(len(time)) * 2 * np.pi / 365) * 5 + 15  # Seasonal signal
    
    return xr.Dataset(
        {
            "moc_mar_hc10": (
                ["TIME"],
                transport,
                {
                    "units": "Sv",
                    "long_name": "Meridional Overturning Circulation",
                    "comment": "MOC at 26.5N, 1000m depth"
                }
            )
        },
        coords={"TIME": time},
    )


def test_plot_monthly_transport():
    """Test the plot_monthly_transport function."""
    ds = create_dummy_dataset()
    
    fig, ax = plotting.plot_monthly_transport(ds)
    
    # Check that a figure and axis are returned
    assert fig is not None
    assert ax is not None
    
    # Check that the plot has the expected number of lines (original + monthly avg)
    lines = ax.get_lines()
    assert len(lines) >= 2  # At least original and monthly average
    
    # Check that axis labels are set
    assert ax.get_ylabel() != ""
    assert ax.get_xlabel() != ""
    
    # Check that legend exists
    legend = ax.get_legend()
    assert legend is not None


def test_plot_time_series():
    """Test the basic plot_time_series function."""
    ds = create_dummy_dataset()
    
    fig, ax = plotting.plot_time_series(ds, "moc_mar_hc10")
    
    # Check that a figure and axis are returned
    assert fig is not None
    assert ax is not None
    
    # Check that the plot has data
    lines = ax.get_lines()
    assert len(lines) >= 1
    
    # Check that axis labels are set
    assert ax.get_ylabel() != ""
    assert ax.get_xlabel() == "Time"


def test_plot_time_series_custom_labels():
    """Test plot_time_series with custom labels."""
    ds = create_dummy_dataset()
    
    custom_title = "Custom Title"
    custom_ylabel = "Custom Y-Label"
    
    fig, ax = plotting.plot_time_series(
        ds, "moc_mar_hc10", 
        title=custom_title,
        ylabel=custom_ylabel,
        color="red"
    )
    
    # Check custom labels are applied
    assert ax.get_title() == custom_title
    assert ax.get_ylabel() == custom_ylabel
    
    # Check custom color is applied
    line = ax.get_lines()[0]
    assert line.get_color() == "red"


def test_show_variables_with_dataset():
    """Test show_variables function with an xarray Dataset."""
    ds = create_dummy_dataset()
    
    result = plotting.show_variables(ds)
    
    # Check that result is a styled DataFrame
    assert hasattr(result, 'data')  # Styler objects have a 'data' attribute
    
    # The underlying DataFrame should contain information about our variable
    df = result.data
    assert "moc_mar_hc10" in df.index


def test_show_attributes_with_dataset():
    """Test show_attributes function with an xarray Dataset."""
    # Create a dataset with some attributes
    ds = create_dummy_dataset()
    ds.attrs["title"] = "Test Dataset"
    ds.attrs["institution"] = "Test University"
    
    result = plotting.show_attributes(ds)
    
    # Check that result is a DataFrame
    assert hasattr(result, 'columns')
    assert "Attribute" in result.columns
    assert "Value" in result.columns
    
    # Check that our attributes are in the result
    attributes = result["Attribute"].tolist()
    assert "title" in attributes
    assert "institution" in attributes