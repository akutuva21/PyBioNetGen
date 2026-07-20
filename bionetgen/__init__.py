from .core.defaults import defaults
from .core.tools.bngsim_bridge import BNGSIM_AVAILABLE, BNGSIM_VERSION
from .modelapi import bngmodel
from .modelapi.runner import run
from .simulator.simulators import sim_getter

# sympy is an expensive dependency to import. We delay importing the
# SympyOdes helpers until they are actually accessed.

__all__ = [
    "defaults",
    "BNGSIM_AVAILABLE",
    "BNGSIM_VERSION",
    "bngmodel",
    "run",
    "sim_getter",
    "SympyOdes",
    "export_sympy_odes",
]


def __getattr__(name):
    if name == "__version__":
        import importlib.metadata

        try:
            return importlib.metadata.version("bionetgen")
        except importlib.metadata.PackageNotFoundError:
            from .core.version import get_version

            return get_version()

    if name in {"SympyOdes", "export_sympy_odes"}:
        from .modelapi import sympy_odes

        return getattr(sympy_odes, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
