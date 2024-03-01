import pathlib as pt
import pytest
import shutil

import duallog_v2.dual_logger as dl

EXAMPLE_CONFIG_PATH = "example_config.ini"

@pytest.fixture(scope="function", params=[None, EXAMPLE_CONFIG_PATH])
def dual_logger(request):
    if request.param is None:
        return dl.DualLogger(logs_dir="mylogs")
    else:
        return dl.DualLogger(logs_dir="mylogs", config_file=request.param)
    
    # yield
    # shutil.rmtree("mylogs")

