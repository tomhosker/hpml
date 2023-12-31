"""
This code defines a class which compiles HPML into LaTeX.
"""

# Standard imports.
from dataclasses import dataclass
from pathlib import Path

# Local imports.
from .centerer import Centerer
from .preprocessor import Preprocessor
from .utils import (
    TEX_EXTENSION,
    BEGIN_VERSE,
    BEGIN_VERSE_CENTERED,
    END_VERSE,
    PRE_SETTOWIDTH,
    POST_SETTOWIDTH,
    get_lexicon,
    trim_whitespace,
    trim_blank_lines
)

# Local constants.
LEXICON = get_lexicon()
EQUIVALENTS = LEXICON["equivalents"]
FRACTIONS = LEXICON["fractions"]

##############
# MAIN CLASS #
##############

@dataclass
class HPMLCompiler:
    """ The class in question. """
    path_to_input_file: str = None
    input_string: str = None
    is_prose_poem: bool = False
    mods: list[str] = None
    path_to_output_file: str = None
    output_string: str = None
    enclose: bool = True
    manual_settowidth_string: str = None
    auto_center: bool = True
    # Non-public.
    _temp: str = None
    _lines: list[str] = None

    def __post_init__(self):
        if self.path_to_input_file and self.input_string:
            raise HPMLCompilerException(
                "You must Specify either an input file or an input string, "+
                "but NOT BOTH."
            )
        if not self.path_to_input_file and not self.input_string:
            raise HPMLCompilerException(
                "You must specify either an input file or an input string."
            )
        if not self.input_string:
            with open(self.path_to_input_file, "r") as input_file:
                self.input_string = input_file.read()
        if self.path_to_input_file and not self.path_to_output_file:
            self.path_to_output_file = \
                Path(self.path_to_input_file).with_suffix(TEX_EXTENSION)

    def compile(self) -> str:
        """ Build the output string from the input. """
        self._preprocess()
        self._process()
        if self.path_to_output_file:
            return self.path_to_output_file
        return self.output_string

    def _preprocess(self):
        """ Run the input through a preprocessor object. """
        preprocessor = Preprocessor(self.input_string, self.mods)
        self._temp = preprocessor.preprocess()

    def _process(self):
        """ Ronseal. """
        self._lines = self._temp.split("\n")
        self._purge_whitespace()
        self._process_choruses()
        self._process_minichoruses()
        self._add_endings()
        self._process_syntactics()
        self._process_semantics()
        if self.enclose:
            self._enclose_output()
        self.output_string = "\n".join(self._lines)

    def _purge_whitespace(self):
        """ Ronseal. """
        for index, line in enumerate(self._lines):
            self._lines[index] = trim_whitespace(line)
        self._lines = trim_blank_lines(self._lines)

    def _process_choruses(self):
        """ Handles choruses and inscriptions. """
        for index, line in enumerate(self._lines):
            if ("###CHORUS" in line) or ("###INSCRIPTION" in line):
                for line_num in range(index+1, len(self._lines)):
                    current_line = self._lines[line_num]
                    previous_line = self._lines[line_num-1]
                    if index == len(self._lines)-1:
                        self._lines[line_num] = current_line+"}"
                    elif current_line == "":
                        self._lines[line_num-1] = previous_line+"}"
                        break
                self._lines[index] = "{\\itshape "

    def _process_minichoruses(self):
        """ Handles mini-choruses and mini-inscriptions. """
        for index, line in enumerate(self._lines):
            if ("##MINICHORUS" in line) or ("##MINIINSCRIPTION" in line):
                line = line.replace("##MINICHORUS ", "\\vin \\textit{")
                line = line.replace("##MINIINSCRIPTION ", "\\textit{")
                line = line+"}"
                self._lines[index] = line

    def _add_endings(self):
        """ Adds "\\", "\\*" or "\\!" to each line, as appropriate. """
        if self.is_prose_poem:
            return
        for index, line in enumerate(self._lines):
            if (
                (line == "") or
                (line == "{\\itshape ") or
                (index == len(self._lines)-1)
               ):
                pass
            elif (index != len(self._lines)-1) and (self._lines[index+1] == ""):
                line = line+"\\\\!"
                self._lines[index] = line
            elif index in (0, len(self._lines)-2):
                line = line+"\\\\*"
                self._lines[index] = line
            elif self._lines[index-1] == "":
                line = line+"\\\\*"
                self._lines[index] = line
            elif (index < len(self._lines)-2) and (self._lines[index+2] == ""):
                line = line+"\\\\*"
                self._lines[index] = line
            else:
                line = line+"\\\\"
                self._lines[index] = line

    def _process_syntactics(self):
        """ Translate those clusters for which clear equivalents exist. """
        for hpml_code, eq_dict in EQUIVALENTS.items():
            self._replace_across_all_lines(hpml_code, eq_dict["latex"])

    def _replace_across_all_lines(self, old, new):
        """ Replace every instance of old with new across all lines. """
        for index, line in enumerate(self._lines):
            self._lines[index] = line.replace(old, new)

    def _process_semantics(self):
        """ Ronseal. """
        self._process_tabs()
        self._process_margin_notes()
        self._process_places()
        self._process_persons()
        self._process_publications()
        self._process_foreign_strings()
        self._process_fractions()
        self._process_ampersands()
        self._process_stress()
        self._process_flagverses()
        self._process_subscript()
        self._process_whitespace()

    def _process_tabs(self):
        """ Ronseal. """
        self._replace_across_all_lines("##TAB", "\\vin")

    def _process_margin_notes(self):
        """ Ronseal. """
        self._replace_across_all_lines(
            "##MARGINNOTE{",
            "\\marginnote{\\footnotesize "
        )

    def _process_places(self):
        """ Ronseal. """
        self._replace_across_all_lines("#PLACE{", "\\textsc{")

    def _process_persons(self):
        """ Ronseal. """
        self._replace_across_all_lines("#PERSON{", "\\textit{")

    def _process_publications(self):
        """ Ronseal. """
        self._replace_across_all_lines("#PUBLICATION{", "{\\hoskeroe ")

    def _process_foreign_strings(self):
        """ Ronseal. """
        self._replace_across_all_lines("#FOREIGN{", "{\\hoskeroe ")

    def _process_fractions(self):
        """ Ronseal. """
        for hpml_code, sub_dict in FRACTIONS.items():
            latex_code = sub_dict["latex"]
            self._replace_across_all_lines(hpml_code, latex_code)

    def _process_ampersands(self):
        """ Ronseal. """
        self._replace_across_all_lines("#ADD", "\\&")

    def _process_stress(self):
        """ Handles stressed syllables. """
        self._replace_across_all_lines("#STRESS{", "\\'{")

    def _process_flagverses(self):
        """ Adds mini-titles to particular verses. """
        self._replace_across_all_lines(
            "##FLAGVERSE{",
            "\\flagverse{\\footnotesize "
        )

    def _process_subscript(self):
        """ Ronseal. """
        self._replace_across_all_lines("#SUB{", "\\textsubscript{")

    def _process_whitespace(self):
        """ Ronseal. """
        self._replace_across_all_lines("#WHITESPACE{", "\\textcolor{white}{")

    def _enclose_output(self):
        """ Enclose the input in a poem environment. """
        if self.manual_settowidth_string or self.auto_center:
            local_begin_verse = BEGIN_VERSE_CENTERED
        else:
            local_begin_verse = BEGIN_VERSE
        self._lines = [local_begin_verse]+self._lines+[END_VERSE]
        if self.manual_settowidth_string or self.auto_center:
            self._center_output()

    def _center_output(self):
        """ Add a string to center this poem on the page. """
        if self.manual_settowidth_string:
            settowidth_string = self.manual_settowidth
        else:
            settowidth_string = get_settowidth_string(self.input_string)
        settowidth_line = PRE_SETTOWIDTH+settowidth_string+POST_SETTOWIDTH
        self._lines = [settowidth_line]+self._lines

    def save_to_file(self) -> str:
        """ Save the output string to a file. """
        if not self.path_to_output_file:
            raise HPMLCompilerException("No save file path specified.")
        with open(self.path_to_output_file, "w") as output_file:
            output_file.write(self.output_string)
        return self.path_to_output_file

################################
# HELPER CLASSES AND FUNCTIONS #
################################

class HPMLCompilerException(Exception):
    """ A custom exception. """

def get_settowidth_string(input_string):
    """ Get an automatically-generated settowidth string for a given poem in
    HPML code. """
    centerer = Centerer(input_string)
    return centerer.get_settowidth_string()
