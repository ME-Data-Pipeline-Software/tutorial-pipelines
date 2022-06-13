import numpy as np
from pydantic import BaseModel, Extra
import xarray as xr
from numpy.typing import NDArray
from tsdat import QualityChecker, QualityHandler


class PolyInterpHandler(QualityHandler):
    """----------------------------------------------------------------------------
    Fills in missing data with a cubic polynomial spline
    ----------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        """If your QualityChecker should take any additional arguments from the
        quality configuration file, then those should be specified here.
        """

    parameters: Parameters = Parameters()
    """Extra parameters that can be set via the quality configuration file. If you opt
    to not use any configuration parameters then please remove the code above."""

    def run(
        self, dataset: xr.Dataset, variable_name: str, failures: NDArray[np.bool8]
    ) -> xr.Dataset:

        if failures.any():
            dataset[variable_name] = dataset[variable_name].interpolate_na(
                dim="time", method="cubic", keep_attrs=True
            )

        return dataset
