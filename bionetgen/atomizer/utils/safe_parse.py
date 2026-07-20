import ast


def safe_parse(val, max_depth=100):
    """
    Safely parse a string containing a Python literal expression.
    Prevents recursion/stack overflow attacks by checking nesting depth
    before calling ast.literal_eval.
    """
    if not isinstance(val, str):
        return val

    depth = 0
    max_depth_seen = 0
    for char in val:
        if char in "[({":
            depth += 1
            if depth > max_depth_seen:
                max_depth_seen = depth
            if depth > max_depth:
                raise ValueError("String is too deeply nested to be safely parsed")
        elif char in "])}":
            depth -= 1

    return ast.literal_eval(val)
