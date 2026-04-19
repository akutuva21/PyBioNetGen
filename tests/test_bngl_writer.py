from bionetgen.atomizer.writer.bnglWriter import evaluatePiecewiseFunction

def test_evaluatePiecewiseFunction():
    # evaluatePiecewiseFunction currently just returns None
    assert evaluatePiecewiseFunction(None) is None
    assert evaluatePiecewiseFunction("some function string") is None
    assert evaluatePiecewiseFunction({"key": "value"}) is None
    assert evaluatePiecewiseFunction(123) is None
