import os
import logging
from tempfile import TemporaryDirectory
from bionetgen.main import BioNetGen
from bionetgen.core.tools import BNGCLI

app = BioNetGen()
app.setup()
conf = app.config["bionetgen"]

logger = logging.getLogger(__name__)


def run(inp, out=None, suppress=False, timeout=None):
    """
    Convenience function to run BNG2.pl as a library

    Usage: run(path_to_input_file, output_folder)

    Arguments
    ---------
    path_to_input_file : str
        this has to point to a BNGL file
    output_folder : str
        (optional) this points to a folder to put the results
        into. If it doesn't exist, it will be created.
    """
    # if out is None we make a temp directory
    cur_dir = os.getcwd()
    if out is None:
        import tempfile
        import shutil

        out_dir = tempfile.mkdtemp(prefix="bngrun_")
        try:
            # instantiate a CLI object with the info
            cli = BNGCLI(
                inp, out_dir, conf["bngpath"], suppress=suppress, timeout=timeout
            )
            cli.run()
        except Exception as e:
            logger.error("Couldn't run the simulation, see error")
            if hasattr(e, "stdout") and e.stdout is not None:
                logger.error(f"STDOUT:\n{e.stdout}")
            if hasattr(e, "stderr") and e.stderr is not None:
                logger.error(f"STDERR:\n{e.stderr}")
            raise e
        finally:
            os.chdir(cur_dir)
            try:
                shutil.rmtree(out_dir)
            except:
                pass
    else:
        try:
            # instantiate a CLI object with the info
            cli = BNGCLI(inp, out, conf["bngpath"], suppress=suppress, timeout=timeout)
            cli.run()
        except Exception as e:
            logger.error("Couldn't run the simulation, see error")
            if hasattr(e, "stdout") and e.stdout is not None:
                logger.error(f"STDOUT:\n{e.stdout}")
            if hasattr(e, "stderr") and e.stderr is not None:
                logger.error(f"STDERR:\n{e.stderr}")
            raise e
        finally:
            os.chdir(cur_dir)
    return cli.result
