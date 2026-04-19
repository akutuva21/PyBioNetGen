1. Modify `add_empty_block` and `add_block` in `bionetgen/network/network.py` and `bionetgen/modelapi/model.py` to handle the AttributeError when `getattr` fails to find a valid block adder method.
2. If `getattr` raises an `AttributeError` with a message like "'Network' object has no attribute...", catch the exception and raise a `BNGModelError` with a message indicating the block is not supported. For example: `raise BNGModelError(self, message=f"Block type {bname} is not supported.")` for `bionetgen/network/network.py` and `raise BNGModelError(self.model_path, message=f"Block type {bname} is not supported.")` for `bionetgen/modelapi/model.py`.
3. Complete pre commit steps to ensure proper testing, verification, review, and reflection are done.
4. Run testing script to make sure the exceptions are properly caught.
5. Submit the task.
