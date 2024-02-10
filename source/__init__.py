"""
This code compiles HPML (Hosker's Poetical Markup Language) into LaTeX.
"""

# Local imports.
from .hpml_compiler import HPMLCompiler
from .utils import get_package_code

# Local constants.
PACKAGE_CODE = get_package_code()
