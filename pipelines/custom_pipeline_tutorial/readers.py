from typing import Any, Dict, Union
from pydantic import BaseModel, Extra
import pandas as pd
import xarray as xr
from tsdat import DataReader


class NCEIReader(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that can be used to read data from a specific format.

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.
    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        """If your CustomDataReader should take any additional arguments from the
        retriever configuration file, then those should be specified here."""

        read_csv_kwargs: Dict[str, Any] = {}
        from_dataframe_kwargs: Dict[str, Any] = {}

    parameters: Parameters = Parameters()
    """Extra parameters that can be set via the retrieval configuration file. If you opt
    to not use any configuration parameters then please remove the code above."""

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        # Read csv file with pandas
        df = pd.read_csv(input_key, **self.parameters.read_csv_kwargs)

        # Return an xarray dataset
        return xr.Dataset.from_dataframe(df, **self.parameters.from_dataframe_kwargs)
