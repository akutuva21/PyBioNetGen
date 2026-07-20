import pytest
from unittest.mock import patch
from bionetgen.modelapi.sympy_odes import (
    _safe_rmtree,
    _extract_nv_assignments,
    _extract_define_int,
    _extract_odes_from_cvode_mex,
    _replace_parameters_brackets,
)


def test_replace_parameters_brackets():
    # Normal in-bounds replacements
    expr = "parameters[0] * parameters[1] + parameters[2]"
    param_names = ["k1", "k2", "k3"]
    assert _replace_parameters_brackets(expr, param_names) == "k1 * k2 + k3"

    # Out-of-bounds replacements
    expr = "parameters[0] + parameters[10]"
    param_names = ["k1"]
    assert _replace_parameters_brackets(expr, param_names) == "k1 + p10"

    # Varying whitespace
    expr = "parameters  [ 0 ] * parameters[1  ]"
    param_names = ["k1", "k2"]
    assert _replace_parameters_brackets(expr, param_names) == "k1 * k2"

    # No matches
    expr = "no parameters here"
    param_names = ["k1"]
    assert _replace_parameters_brackets(expr, param_names) == "no parameters here"

    # Empty parameter list
    expr = "parameters[0] + parameters[1]"
    param_names = []
    assert _replace_parameters_brackets(expr, param_names) == "p0 + p1"


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


def test_extract_function_body_newlines():
    text = """void myfunc()
{
  body text;
}
"""
    assert _extract_function_body(text, "myfunc") == "\n  body text;\n"


def test_extract_function_body_parameters():
    text = """void myfunc(int a, double b) {
  body param;
}
"""
    assert _extract_function_body(text, "myfunc") == "\n  body param;\n"


def test_extract_function_body_multiple_funcs():
    text = """void otherfunc() {
  other;
}
void myfunc() {
  target;
}
"""
    assert _extract_function_body(text, "myfunc") == "\n  target;\n"


def test_extract_define_int():
    assert _extract_define_int("#define MY_VAR 42", "MY_VAR") == 42
    assert _extract_define_int("  #define   MY_VAR   42  ", "MY_VAR") == 42
    assert _extract_define_int("\t#define\tMY_VAR\t42\t", "MY_VAR") == 42
    text = """
    #define OTHER 1
    #define MY_VAR 42
    #define ANOTHER 2
    """
    assert _extract_define_int(text, "MY_VAR") == 42
    assert _extract_define_int("#define OTHER 1", "MY_VAR") is None
    assert _extract_define_int("#define MY_VAR abc", "MY_VAR") is None
    assert _extract_define_int("#define MY_VAR 42.5", "MY_VAR") is None


def test_replace_indexed_symbols_repl_param():
    from bionetgen.modelapi.sympy_odes import _replace_indexed_symbols

    expr = "NV_Ith_S(y, 0) + y[1] + params[0] + param[1] + p[2] + p[3]"
    species = ["S1"]
    params = ["k1", "k2", "k3"]
    res = _replace_indexed_symbols(expr, species, params)
    assert res == "S1 + s1 + k1 + k2 + k3 + p3"


from bionetgen.modelapi.sympy_odes import _replace_indexed_symbols


def test_replace_indexed_symbols():
    # Test valid species and parameter indices
    expr = "NV_Ith_S(y,0) + y[1] + params[0] * param[1] - p[2]"
    res = _replace_indexed_symbols(expr, ["S1", "S2"], ["k1", "k2", "k3"])
    assert res == "S1 + S2 + k1 * k2 - k3"

    # Test species index out of bounds
    expr_out_of_bounds_species = "NV_Ith_S(y,2)"
    res = _replace_indexed_symbols(expr_out_of_bounds_species, ["S1", "S2"], [])
    assert res == "s2"

    # Test parameter index out of bounds
    expr_out_of_bounds_param = "param[2]"
    res = _replace_indexed_symbols(expr_out_of_bounds_param, [], ["k1", "k2"])
    assert res == "p2"

    expr_out_of_bounds_params = "params[2]"
    res = _replace_indexed_symbols(expr_out_of_bounds_params, [], ["k1", "k2"])
    assert res == "p2"

    expr_out_of_bounds_p = "p[2]"
    res = _replace_indexed_symbols(expr_out_of_bounds_p, [], ["k1", "k2"])
    assert res == "p2"


import sympy as sp
from bionetgen.modelapi.sympy_odes import _replace_nv_ith_s


def test_replace_nv_ith_s():
    species_symbol_names = ["A", "B", "C"]
    expr_syms = [sp.Symbol("E1"), sp.Symbol("E2")]
    obs_syms = [sp.Symbol("O1")]
    rate_syms = [sp.Symbol("R1"), sp.Symbol("R2"), sp.Symbol("R3")]

    # Test "species" branch (in bounds and out of bounds)
    expr1 = "NV_Ith_S(species, 1) + NV_Ith_S(species, 5)"
    res1 = _replace_nv_ith_s(
        expr1, species_symbol_names, expr_syms, obs_syms, rate_syms
    )
    assert res1 == "B + s5"

    # Test "expressions" branch
    expr2 = "NV_Ith_S(expressions, 0) + NV_Ith_S(expressions, 10)"
    res2 = _replace_nv_ith_s(
        expr2, species_symbol_names, expr_syms, obs_syms, rate_syms
    )
    assert res2 == "E1 + e10"

    # Test "observables" branch
    expr3 = "NV_Ith_S(observables, 0) + NV_Ith_S(observables, 5)"
    res3 = _replace_nv_ith_s(
        expr3, species_symbol_names, expr_syms, obs_syms, rate_syms
    )
    assert res3 == "O1 + o5"

    # Test "ratelaws" branch
    expr4 = "NV_Ith_S(ratelaws, 2) + NV_Ith_S(ratelaws, 10)"
    res4 = _replace_nv_ith_s(
        expr4, species_symbol_names, expr_syms, obs_syms, rate_syms
    )
    assert res4 == "R3 + r10"

    # Test "Dspecies" branch
    expr5 = "NV_Ith_S(Dspecies, 1)"
    res5 = _replace_nv_ith_s(
        expr5, species_symbol_names, expr_syms, obs_syms, rate_syms
    )
    assert res5 == "ds1"

    # Test unknown variable branch
    expr6 = "NV_Ith_S(unknown, 2)"
    res6 = _replace_nv_ith_s(
        expr6, species_symbol_names, expr_syms, obs_syms, rate_syms
    )
    assert res6 == "NV_Ith_S(unknown, 2)"


def test_replace_indexed_symbols():
    from bionetgen.modelapi.sympy_odes import _replace_indexed_symbols

    species_names = ["S1", "S2"]
    param_names = ["k1", "k2"]

    # Test species replacements
    expr1 = "NV_Ith_S(y, 0) + NV_Ith_S(y, 1)"
    assert _replace_indexed_symbols(expr1, species_names, param_names) == "S1 + S2"

    expr2 = "y[0] + y[1]"
    assert _replace_indexed_symbols(expr2, species_names, param_names) == "S1 + S2"

    # Test out of bounds species
    expr3 = "y[2]"
    assert _replace_indexed_symbols(expr3, species_names, param_names) == "s2"

    # Test param replacements
    expr4 = "params[0] + param[1]"
    assert _replace_indexed_symbols(expr4, species_names, param_names) == "k1 + k2"

    expr5 = "p[0]"
    assert _replace_indexed_symbols(expr5, species_names, param_names) == "k1"

    # Test out of bounds param
    expr6 = "p[2]"
    assert _replace_indexed_symbols(expr6, species_names, param_names) == "p2"
