import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_custom_pipeline_tutorial_pipeline():
    config_path = Path("pipelines/custom_pipeline_tutorial/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = (
        "pipelines/custom_pipeline_tutorial/test/data/input/custom.sample_data.csv"
    )
    expected_file = "pipelines/custom_pipeline_tutorial/test/data/expected/arctic.custom_pipeline_tutorial.b1.20150112.000000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
