# Plan to Improve CLI Error Reporting in `bionetgen/modelapi/runner.py`

## Understanding the Issue
The current code in `bionetgen/modelapi/runner.py` catches an exception during execution of `BNGCLI.run()`, prints a generic message "Couldn't run the simulation, see error", and then re-raises the exception. The user explicitly stated: "Can be improved easily by extracting the stderr/stdout from the CLI execution object or logging the exception detail."

Looking at `BNGCLI` in `bionetgen/core/tools/cli.py`, if an error occurs running the command, it raises a `BNGRunError` (from `bionetgen.core.exc`). A `BNGRunError` instance has properties `stdout` and `stderr`.
Even for generic exceptions, it's more informative to log them rather than just `print()`.

We will modify `bionetgen/modelapi/runner.py` to check if `e` has `stdout` or `stderr` and log them, or use the app logger to print the error.
Actually, the app object is imported and available in `runner.py`:
```python
app = BioNetGen()
app.setup()
```
We can use `app.log.error()` to log the error details, including checking for `hasattr(e, "stdout")` and `hasattr(e, "stderr")` and logging them.

## Planned Changes
1. *Modify `bionetgen/modelapi/runner.py` exception handling*
   - Change both `except Exception as e:` blocks in `run()`.
   - Use `app.log.error(f"Couldn't run the simulation: {e}")` instead of `print(...)`.
   - Check if `hasattr(e, "stdout")` and it's not None, and log it: `app.log.error(f"stdout: {e.stdout}")`.
   - Check if `hasattr(e, "stderr")` and it's not None, and log it: `app.log.error(f"stderr: {e.stderr}")`.
   - Keep the `raise e` at the end to not break any higher-level catching.

2. *Verify Changes*
   - Run the tests in `tests/test_runner.py` to ensure the exceptions are still raised correctly.
   - Run our `test_fail.py` script to see if the stdout/stderr are now appropriately logged by the app.

3. *Pre-commit steps*
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

4. *Submit*
   - Submit the branch.
