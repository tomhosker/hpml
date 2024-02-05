"""
This code defines the functions which test the HPMLCOMPILER class.
"""

# Standard imports.
from pathlib import Path

# Source imports.
from source.hpml_compiler import HPMLCompiler

# Local constants.
PATH_OBJ_TO_DATA = Path(__file__).parent/"data"

####################
# HELPER FUNCTIONS #
####################

def compile_hpml_from_path(path_to_hpml):
    """ Ronseal. """
    compiler = HPMLCompiler(path_to_input_file=path_to_hpml)
    compiler.compile()
    compiler.save_to_file()

def assert_tex_equals(path_to_actual, path_to_expected):
    """ Assert that the contents of two .tex files are the same. """
    with open(path_to_actual, "r") as actual_file:
        actual = actual_file.read()
    with open(path_to_expected, "r") as expected_file:
        expected = expected_file.read()
    while expected.endswith("\n"):
        expected = expected[0:-1]
    assert actual == expected

###########
# TESTING #
###########

def test_hpml_compiler():
    """ Test that the compiler runs and produces the right output. """
    path_to_hpml = str(PATH_OBJ_TO_DATA/"ode_on_a_grecian_urn.hpml")
    path_to_actual = Path(path_to_hpml).with_suffix(".tex")
    path_to_expected = str(PATH_OBJ_TO_DATA/"ode_on_a_grecian_urn_expected.tex")
    compile_hpml_from_path(path_to_hpml)
    assert_tex_equals(path_to_actual, path_to_expected)
    # Clean.
    Path(path_to_actual).unlink()

def test_manual_centering():
    """ Test that, when manual centering is indicated in the HPML code, it is
    handled correctly. """
    hpml_fn = "ode_on_a_grecian_urn_manual_centering.hpml"
    expected_fn = "ode_on_a_grecian_urn_manual_centering_expected.tex"
    path_to_hpml = str(PATH_OBJ_TO_DATA/hpml_fn)
    path_to_actual = Path(path_to_hpml).with_suffix(".tex")
    path_to_expected = str(PATH_OBJ_TO_DATA/expected_fn)
    compile_hpml_from_path(path_to_hpml)
    assert_tex_equals(path_to_actual, path_to_expected)
    # Clean.
    Path(path_to_actual).unlink()
