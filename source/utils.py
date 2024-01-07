"""
This code defines some utility functions used across the package.
"""

# Standard imports.
import json
import shutil
import warnings
from pathlib import Path

# Local constants.
PATH_OBJ_TO_DATA = Path(__file__).parent/"data"
PATH_TO_LEXICON = str((PATH_OBJ_TO_DATA/"lexicon.json").resolve())
PATH_OBJ_TO_GTKSOURCEVIEW = Path("/usr")/"share"/"gtksourceview-4"
PATH_TO_HPML_LANG_SRC = str((PATH_OBJ_TO_DATA/"hpml.lang").resolve())
PATH_OBJ_TO_HPML_LANG_DST = \
    PATH_OBJ_TO_GTKSOURCEVIEW/"language-specs"/"hpml.lang"
PATH_TO_HPML_LANG_DST = str(PATH_OBJ_TO_HPML_LANG_DST.resolve())
SUPPRESS_NON_STANDARD_MOD_NAME = "suppress_non_standard"
SUPPRESS_NON_STANDARD_MODS = {
    "suppress_person_font",
    "suppress_place_font",
    "suppress_publication_font",
    "suppress_foreign_font",
    "suppress_ship_font",
    "suppress_fractions",
    "suppress_ampersands"
}
OTHER_MODS = {
    "em_dashes",
}
ALL_MODS = SUPPRESS_NON_STANDARD_MODS.union(OTHER_MODS)
HPML_EXTENSION = ".hpml"
TEX_EXTENSION = ".tex"
BEGIN_VERSE = "\\begin{verse}"
END_VERSE = "\\end{verse}"
PRE_SETTOWIDTH = "\\settowidth{\\versewidth}{"
POST_SETTOWIDTH = "}"

#############
# FUNCTIONS #
#############

def get_lexicon():
    """ Return a dictionary of the HTML lexicon. """
    with open(PATH_TO_LEXICON, "r") as lexicon_file:
        lexicon_str = lexicon_file.read()
    result = json.loads(lexicon_str)
    return result

def install_hpml_lang():
    """ Install the HPML language features in Gedit. """
    if not PATH_OBJ_TO_HPML_LANG_DST.exists():
        if PATH_OBJ_TO_GTKSOURCEVIEW.exists():
            shutil.copy(PATH_TO_HPML_LANG_SRC, PATH_TO_HPML_LANG_DST)
        else:
            path_to_gtksourceview = str(PATH_OBJ_TO_GTKSOURCEVIEW.resolve())
            warnings.warn(
                "The folder "+path_to_gtksourceview+" does not exist on this "+
                "machine. Therefore, it has not been possible to install the "+
                "HPML language features into Gedit."
            )
