import pytest
from unittest.mock import patch
from bionetgen.modelapi.sympy_odes import _safe_rmtree, _extract_nv_assignments, _extract_odes_from_cvode_mex


def test_extract_nv_assignments():
    # Empty body
    assert _extract_nv_assignments("", "expr") == {}

    # No matches
    assert _extract_nv_assignments("int main() {}", "expr") == {}

    # Valid assignments using standard array indexing syntax
    body = """
    NV_Ith_S(expressions, 0) = 2.0 * k1;
    NV_Ith_S(expressions, 1) = k2 * s1;
    NV_Ith_S(other_var, 0) = 1.0;
    """

    res = _extract_nv_assignments(body, "expressions")
    assert len(res) == 2
    assert res[0] == "2.0 * k1"
    assert res[1] == "k2 * s1"

    # Ensure it only extracts the requested variable
    res_other = _extract_nv_assignments(body, "other_var")
    assert len(res_other) == 1
    assert res_other[0] == "1.0"


def test_safe_rmtree_oserror(tmp_path):
    d = tmp_path / "test_dir"
    d.mkdir()
    (d / "file.txt").write_text("hello")
    with patch("os.lstat") as mock_lstat:
        mock_lstat.side_effect = OSError("Mock OS Error")
        try:
            _safe_rmtree(str(d))
        except Exception as e:
            pytest.fail(f"_safe_rmtree raised an exception unexpectedly: {e}")


import pytest
from bionetgen.modelapi.sympy_odes import extract_odes_from_mexfile


def test_extract_odes_standard_mex(tmp_path):
    mex_c = tmp_path / "model_mex.c"
    mex_c.write_text("""
    const char *species[] = {"S1", "S2"};
    const char *param[] = {"k1", "k2"};

    NV_Ith_S(ydot,0) = -params[0] * NV_Ith_S(y,0);
    NV_Ith_S(ydot,1) = params[0] * NV_Ith_S(y,0) - param[1] * p[1];
    """)
    result = extract_odes_from_mexfile(str(mex_c))

    assert len(result.odes) == 2
    assert str(result.odes[0]) == "-S1*k1"
    assert str(result.odes[1]) == "S1*k1 - k2**2"


def test_extract_odes_cvode(tmp_path):
    mex_c = tmp_path / "model_mex_cvode.c"
    mex_c.write_text("""
    #define __N_SPECIES__ 2
    #define __N_PARAMETERS__ 2

    void calc_expressions(realtype t) {
        NV_Ith_S(expressions,0) = parameters[0] * 2;
}

    void calc_observables(realtype t) {
        NV_Ith_S(observables,0) = NV_Ith_S(species,0) + NV_Ith_S(species,1);
}

    void calc_ratelaws(realtype t) {
        NV_Ith_S(ratelaws,0) = NV_Ith_S(expressions,0) * NV_Ith_S(species,0);
}

    void calc_species_deriv(realtype t) {
        NV_Ith_S(Dspecies,0) = -NV_Ith_S(ratelaws,0);
        NV_Ith_S(Dspecies,1) = NV_Ith_S(ratelaws,0);
}
    """)
    result = extract_odes_from_mexfile(str(mex_c))

    assert len(result.odes) == 2
    assert str(result.odes[0]) == "-2*p0*s0"
    assert str(result.odes[1]) == "2*p0*s0"


def test_extract_odes_no_odes(tmp_path):
    mex_c = tmp_path / "model_empty.c"
    mex_c.write_text("int main() { return 0; }")
    with pytest.raises(ValueError, match="No ODE assignments found in mex output."):
        extract_odes_from_mexfile(str(mex_c))


def test_extract_odes_cvode_no_odes(tmp_path):
    mex_c = tmp_path / "model_cvode_empty.c"
    mex_c.write_text("""
    void calc_species_deriv(realtype t) {
}
    NV_Ith_S(Dspecies,0) // Just to trigger cvode path
    """)
    with pytest.raises(ValueError, match="No ODE assignments found in mex output."):
        extract_odes_from_mexfile(str(mex_c))


def test_extract_odes_unsupported_rate_law(tmp_path):
    mex_c = tmp_path / "model_cvode_err.c"
    mex_c.write_text("""
    #define __N_SPECIES__ 1
    #define __N_PARAMETERS__ 0
    void calc_ratelaws(realtype t) {
        NV_Ith_S(ratelaws,0) = /* not yet supported by writeMexfile */;
}
    void calc_species_deriv(realtype t) {
        NV_Ith_S(Dspecies,0) = NV_Ith_S(ratelaws,0);
}
    """)
    with pytest.raises(NotImplementedError, match="not yet supported by writeMexfile"):
        extract_odes_from_mexfile(str(mex_c))


from bionetgen.modelapi.sympy_odes import _extract_function_body


def test_extract_function_body_normal():
    text = "void myfunc() {\n  body text;\n}\n"
    assert _extract_function_body(text, "myfunc") == "\n  body text;\n"


def test_extract_function_body_missing_brace():
    text = "void myfunc() {\n  body text;\n"
    assert _extract_function_body(text, "myfunc") == ""


def test_extract_function_body_nested_braces():
    text = "void myfunc() {\n  if (1) { body; }\n}\n"
    assert _extract_function_body(text, "myfunc") == "\n  if (1) { body; }\n"


def test_extract_function_body_not_found():
    text = "void otherfunc() {\n  body text;\n}\n"
    assert _extract_function_body(text, "myfunc") == ""

def test_extract_odes_from_cvode_mex_direct():
    mex_c_text = """
    #define __N_SPECIES__ 2
    #define __N_PARAMETERS__ 2

    void calc_expressions(realtype t) {
        NV_Ith_S(expressions,0) = parameters[0] * 2;
}

    void calc_observables(realtype t) {
        NV_Ith_S(observables,0) = NV_Ith_S(species,0) + NV_Ith_S(species,1);
}

    void calc_ratelaws(realtype t) {
        NV_Ith_S(ratelaws,0) = NV_Ith_S(expressions,0) * NV_Ith_S(species,0);
}

    void calc_species_deriv(realtype t) {
        NV_Ith_S(Dspecies,0) = -NV_Ith_S(ratelaws,0);
        NV_Ith_S(Dspecies,1) = NV_Ith_S(ratelaws,0);
}
    """
    result = _extract_odes_from_cvode_mex(mex_c_text, "dummy_path.c")

    assert len(result.odes) == 2
    assert str(result.odes[0]) == "-2*p0*s0"
    assert str(result.odes[1]) == "2*p0*s0"
    assert len(result.species) == 2
    assert len(result.params) == 2

def test_extract_odes_from_cvode_mex_inference():
    # Omits __N_SPECIES__ and __N_PARAMETERS__ defines to test the inference fallback
    mex_c_text = """
    void calc_expressions(realtype t) {
        NV_Ith_S(expressions,0) = parameters[0] * 2;
}

    void calc_observables(realtype t) {
        NV_Ith_S(observables,0) = NV_Ith_S(species,0) + NV_Ith_S(species,1);
}

    void calc_ratelaws(realtype t) {
        NV_Ith_S(ratelaws,0) = NV_Ith_S(expressions,0) * NV_Ith_S(species,0);
}

    void calc_species_deriv(realtype t) {
        NV_Ith_S(Dspecies,0) = -NV_Ith_S(ratelaws,0);
        NV_Ith_S(Dspecies,1) = NV_Ith_S(ratelaws,0);
}
    """
    result = _extract_odes_from_cvode_mex(mex_c_text, "dummy_path.c")

    assert len(result.odes) == 2
    assert str(result.odes[0]) == "-2*p0*s0"
    assert str(result.odes[1]) == "2*p0*s0"
    assert len(result.species) == 2
    assert len(result.params) == 1
