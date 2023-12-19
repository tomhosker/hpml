"""
This code defines the functions which test the HPMLCOMPILER class.
"""

# Standard imports.
from pathlib import Path

# Source imports.
from source.hpml_compiler import HPMLCompiler

###########
# TESTING #
###########

def test_hpml_compiler():
    """ Test that the compiler runs and produces the right output. """
    path_obj_to_data = Path(__file__).parent/"data"
    path_to_hpml = str(path_obj_to_data/"ode_on_a_grecian_urn.hpml")
    compiler = HPMLCompiler(path_to_input_file=path_to_hpml)
    compiler.compile()
    compiler.save_to_file()
    path_to_actual = Path(path_to_hpml).with_suffix(".tex")
    with open(path_to_actual, "r") as actual_file:
        actual = actual_file.read()
    path_to_expected = str(path_obj_to_data/"ode_on_a_grecian_urn_expected.tex")
    with open(path_to_expected, "r") as expected_file:
        expected = expected_file.read()
    assert actual == expected
    # Clean.
    Path(path_to_actual).unlink()
