"""
This code defines the functions which test the PREPROCESSOR class.
"""

# Source imports.
from source.preprocessor import Preprocessor

###########
# TESTING #
###########

def test_no_mods():
    """ Test the Preprocessor class. """
    before = "This #PERSON{Person} is a douchebag."
    mods = []
    preprocessor = Preprocessor(before, mods)
    after = preprocessor.preprocess()
    assert "#PERSON" in after

def test_suppress_place_and_foreign_fonts():
    """ Test that suppression of the special place and foreign fonts is
    happening. """
    before = "This #PLACE{Place} feels #FOREIGN{foreign}."
    mods = ["suppress_place_font", "suppress_foreign_font"]
    preprocessor = Preprocessor(before, mods)
    after = preprocessor.preprocess()
    assert "#PLACE" not in after
    assert "#FOREIGN" not in after

def test_suppress_fractions():
    """ Test that suppression of fractions is taking place. """
    before = "What's a #HALF plus a #THIRD plus a #QUARTER?"
    mods = ["suppress_fractions"]
    preprocessor = Preprocessor(before, mods)
    after = preprocessor.preprocess()
    assert "#HALF" not in after
    assert "#THIRD" not in after
    assert "#QUARTER" not in after

def test_m_dashes_and_suppress_ampersands():
    """ Test that suppression of fractions is taking place. """
    before = "Fear God -- #ADD take your own part."
    mods = ["suppress_ampersands", "em_dashes"]
    preprocessor = Preprocessor(before, mods)
    after = preprocessor.preprocess()
    assert "#ADD" not in after
    assert " -- " not in after
