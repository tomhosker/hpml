"""
This code defines some utility functions used across the package.
"""

# Standard imports.
import json
import re
import shutil
import warnings
from enum import Enum
from pathlib import Path

# Local constants.
PATH_OBJ_TO_DATA = Path(__file__).parent/"data"
PATH_TO_LEXICON = str((PATH_OBJ_TO_DATA/"lexicon.json").resolve())
PATH_OBJ_TO_GTKSOURCEVIEW = Path("/usr")/"share"/"gtksourceview-4"
PATH_TO_HPML_LANG_SRC = str((PATH_OBJ_TO_DATA/"hpml.lang").resolve())
PATH_OBJ_TO_HPML_LANG_DST = \
    PATH_OBJ_TO_GTKSOURCEVIEW/"language-specs"/"hpml.lang"
PATH_TO_HPML_LANG_DST = str(PATH_OBJ_TO_HPML_LANG_DST.resolve())
HPML_EXTENSION = ".hpml"
TEX_EXTENSION = ".tex"
BEGIN_VERSE = "\\begin{verse}"
BEGIN_VERSE_CENTERED = BEGIN_VERSE+"[\\versewidth]"
END_VERSE = "\\end{verse}"
PRE_SETTOWIDTH = "\\settowidth{\\versewidth}{"
POST_SETTOWIDTH = "}"

#########
# ENUMS #
#########

SUPPRESS_NON_STANDARD = "suppress_non_standard"

class SuppressNonStandardMods(Enum):
    """ Lists the mods which, individually, suppress any non-standard printing
    conventions. """
    SUPPRESS_PERSON_FONT = "suppress_person_font"
    SUPPRESS_PLACE_FONT = "suppress_place_font"
    SUPPRESS_PUBLICATION_FONT = "suppress_publication_font"
    SUPPRESS_FOREIGN_FONT = "suppress_foreign_font"
    SUPPRESS_SHIP_FONT = "suppress_ship_font"
    SUPPRESS_FRACTIONS = "suppress_fractions"
    SUPPRESS_AMPERSANDS = "suppress_ampersands"

class OtherMods(Enum):
    """ Lists the mods which do not suppress any non-standard printing
    conventions. """
    EM_DASHES = "em_dashes"

# Sets of values are sometimes useful.
SUPPRESS_NON_STANDARD_MODS_AS_SET = {
    item.value for item in SuppressNonStandardMods
}
OTHER_MODS_AS_SET = {item.value for item in OtherMods}

#############
# FUNCTIONS #
#############

def is_suppress_non_standard_mod(mod_name):
    """ Determine whether the enum contains this value. """
    if mod_name in SUPPRESS_NON_STANDARD_MODS_AS_SET:
        return True
    return False

def is_other_mod(mod_name):
    """ Determine whether the enum contains this value. """
    if mod_name in OTHER_MODS_AS_SET:
        return True
    return False

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

def trim_whitespace(line):
    """ Remove (1) whitespace from the front, (2) and from the back, and (3)
    any double, triple, etc spaces. """
    line = re.sub("^ *", "", line)
    line = re.sub(" *$", "", line)
    while "  " in line:
        line = line.replace("  ", " ")
    return line

def trim_blank_lines(lines):
    """ Trim any leading or trailing blank lines, and any double, triple, etc
    blank lines, from a list of lines. """
    result = []
    last_index = len(lines)-1
    prev = None
    for index, line in enumerate(lines):
        if (
            (line != "") or
            ((prev is not None) and (prev != "") and (index != last_index))
        ):
            result.append(line)
        prev = line
    return result
