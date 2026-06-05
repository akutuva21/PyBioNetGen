# NOTE Anything that needs to go into the library
# side needs to not be in the core section, it
# leads to circular imports
from .result import BNGResult
from .plot import BNGPlotter
from .info import BNGInfo
from .cli import BNGCLI
from .visualize import BNGVisualize
from .gdiff import BNGGdiff
from .bngsim_bridge import (
    BNGSIM_AVAILABLE,
    BNGSIM_HAS_NFSIM,
    BNGSIM_VERSION,
    detect_input_format,
    run_bngl_with_bngsim,
    run_bngl_with_bngsim_backend_hook,
    run_nfsim,
    run_with_bngsim,
)
from .bngsim_backend_helper import (
    execute_backend_payload as execute_bngsim_backend_payload,
)
