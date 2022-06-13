import xarray as xr
from typing import Any, Optional
from pydantic import BaseModel, Extra
from tsdat.io.base import DataConverter
from tsdat.utils import assign_data
from tsdat.config.dataset import DatasetConfig


class Kt10Converter(DataConverter):
    """---------------------------------------------------------------------------------
    Converts NCEI windspeed data format from 0.1 knots to m/s
    Expects "kt/10" as input and "m/s" as output units
    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        """If your CustomConverter should take any additional arguments from the
        retriever configuration file, then those should be specified here.
        """

        units: Optional[str] = None

    parameters: Parameters = Parameters()
    """Extra parameters that can be set via the retrieval configuration file. If you opt
    to not use any configuration parameters then please remove the code above."""

    def convert(
        self,
        dataset: xr.Dataset,
        dataset_config: DatasetConfig,
        variable_name: str,
        **kwargs: Any,
    ) -> xr.Dataset:

        input_units = self.parameters.units
        output_units = dataset_config[variable_name].attrs.units

        if "kt/10" in input_units and "m/s" in output_units:
            pass
        else:
            return dataset

        data = dataset[variable_name].data / 10 * 0.514444

        dataset = assign_data(dataset, data, variable_name)
        dataset[variable_name].attrs["units"] = output_units

        return dataset
