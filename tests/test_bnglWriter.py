from bionetgen.atomizer.writer.bnglWriter import evaluatePiecewiseFunction


def test_evaluatePiecewiseFunction():
    """
    evaluatePiecewiseFunction explicitly returns None at the moment.
    """
    assert evaluatePiecewiseFunction("some function") is None
    assert evaluatePiecewiseFunction(None) is None
