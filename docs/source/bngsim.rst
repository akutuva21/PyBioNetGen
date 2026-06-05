.. _bngsim:

############################################
Optional in-process simulation with BNGsim
############################################

PyBioNetGen can optionally use `BNGsim <https://github.com/RuleWorld/bngsim>`_ as an
**in-process** simulation engine. This is entirely opt-in:

* If ``bngsim`` is **not** installed, every simulation routes through the existing
  subprocess ``BNG2.pl`` / ``run_network`` / NFsim path exactly as before.
  **With BNGsim absent, behavior is unchanged.**
* If ``bngsim`` **is** installed (and recent enough), the simulation step runs
  in-process, without spawning a Perl subprocess.

BNGsim is **never an install dependency** of PyBioNetGen. It is gated at runtime by a
single ``BNGSIM_AVAILABLE`` flag, so installing it can only add capabilities — it can
never change the default path.

What it enables
===============

These capabilities are active **only when BNGsim is installed**:

* In-process **ODE, SSA, and NFsim** simulation (no Perl subprocess for the
  simulation step).
* **Multi-format input** with auto-detection — ``.bngl``, ``.net``, SBML (``.xml``),
  and Antimony (``.ant``) — plus an explicit override (``--format`` / ``format=``).
* Codegen (compiled C right-hand side) for accelerated ODE simulation, with
  automatic fallback to the interpreted RHS where codegen is unsafe.
* Threaded parameter scanning and steady-state solving.
* New ``run`` CLI flags: ``--method``, ``--format``, ``--timeout``, ``--no-bngsim``.
* New ``bionetgen.run(...)`` keyword arguments: ``simulator=`` (default ``"auto"``),
  ``method=``, ``format=``, ``t_span=``, ``n_points=``, ``timeout=``.

Installing BNGsim
=================

BNGsim is a compiled extension and is not yet published on PyPI, so the extra

.. code-block:: shell

    pip install bionetgen[bngsim]

will not resolve until BNGsim is on PyPI. The extra is declared (floor
``bngsim>=0.9.10``) so it works automatically once that happens.

In the meantime, install a prebuilt wheel from the release assets:

* **macOS / Python 3.12 wheels (arm64 + x86_64):**
  https://github.com/wshlavacek/PyBioNetGen/releases/tag/bngsim-wheels-0.9.10

.. code-block:: shell

    pip install bionetgen
    pip install <path-or-url-to-the-bngsim-wheel>.whl

For other platforms or Python versions, build BNGsim from source (it uses
scikit-build-core).

PyBioNetGen requires **BNGsim 0.9.10 or newer** (``MINIMUM_BNGSIM_VERSION = "0.9.10"``).
An older BNGsim is treated as if it were absent — PyBioNetGen falls back to the
legacy subprocess path and reports the version that was found.

Checking whether it is active
=============================

.. code-block:: python

    import bionetgen
    print(bionetgen.BNGSIM_AVAILABLE)   # True only if a recent BNGsim is importable

Forcing the legacy path
=======================

To force the subprocess path even when BNGsim is installed — for example to compare
results or to reproduce the default behavior — set the ``BIONETGEN_NO_BNGSIM``
environment variable:

.. code-block:: shell

    BIONETGEN_NO_BNGSIM=1 bionetgen run -i mymodel.bngl -o output_folder

The same kill-switch applies to library use; with it set, ``BNGSIM_AVAILABLE`` is
``False`` and every simulation uses the legacy engine. The ``run`` subcommand also
accepts a per-invocation ``--no-bngsim`` flag for the same effect.
