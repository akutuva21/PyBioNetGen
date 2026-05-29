import re

def fix_types(arg_value, arg_type):
    if arg_type == "dict":
        if isinstance(arg_value, str) and arg_value.startswith("{") and arg_value.endswith("}"):
            return True
        return isinstance(arg_value, dict)
    elif arg_type == "list":
        if isinstance(arg_value, str) and arg_value.startswith("[") and arg_value.endswith("]"):
            return True
        return isinstance(arg_value, list)
    return False

print(fix_types("{'R'=>5,'L'=>5}", "dict"))
