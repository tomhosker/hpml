"""
This code defines a class which carries out the preprocessing stage of compiling
HPML into LaTeX.
"""

# Standard imports.
import warnings

# Local imports.
from .utils import (
    SUPPRESS_NON_STANDARD_MOD_NAME,
    SUPPRESS_NON_STANDARD_MODS,
    ALL_MODS,
    get_lexicon
)

# Local constants.
FRACTIONS = get_lexicon()["fractions"]

##############
# MAIN CLASS #
##############

class Preprocessor:
    """ The class in question. """
    def __init__(self, hpml, raw_mods):
        if not raw_mods:
            raw_mods = ()
        self.hpml = hpml
        self.mods = build_mods(raw_mods)

    def preprocess(self):
        """ Ronseal. """
        for mod in self.mods:
            mod_method = getattr(self, mod)
            mod_method()
        return self.hpml

    def replace_substring(self, old, new):
        """ Replace a given substring with another. """
        self.hpml = self.hpml.replace(old, new)

    def suppress_person_font(self):
        """ Implement the mod. """
        self.replace_substring("#PERSON", "")

    def suppress_place_font(self):
        """ Implement the mod. """
        self.replace_substring("#PLACE", "")

    def suppress_publication_font(self):
        """ Implement the mod. """
        self.replace_substring("#PUBLICATION", "#ITAL")

    def suppress_foreign_font(self):
        """ Implement the mod. """
        self.replace_substring("#FOREIGN", "#ITAL")

    def suppress_ship_font(self):
        """ Implement the mod. """
        self.replace_substring("#SHIP", "#ITAL")

    def suppress_ampersands(self):
        """ Implement the mod. """
        self.replace_substring("#ADD", "and")

    def suppress_fractions(self):
        """ Implement the mod. """
        for fraction, sub_dict in FRACTIONS.items():
            self.replace_substring(fraction, sub_dict["words"])

    def em_dashes(self):
        """ Implement the mod. """
        self.replace_substring(" -- ", " --- ")

####################
# HELPER FUNCTIONS #
####################

def build_mods(raw_mods):
    """ Build a SET of mods from a list of raw mods. """
    result = set()
    for raw_mod in raw_mods:
        if raw_mod == SUPPRESS_NON_STANDARD_MOD_NAME:
            result = result.union(SUPPRESS_NON_STANDARD_MODS)
        elif raw_mod in ALL_MODS:
            result.add(raw_mod)
        else:
            warnings.warn("Unrecognised preprocessor mod: "+str(raw_mod))
    return result
