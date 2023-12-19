"""
This code defines a class which compiles HPML into LaTeX.
"""

# Standard imports.
from dataclasses import dataclass
from pathlib import Path

# Local imports.
from .preprocessor import Preprocessor
from .utils import TEX_EXTENSION, get_lexicon

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
    temp: str = None
    lines: list[str] = None
    path_to_output_file: str = None
    output_string: str = None

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

    def compile(self):
        """ Build the output string from the input. """
        self.preprocess()
        self.build_output()

    def preprocess(self):
        """ Run the input through a preprocessor object. """
        preprocessor = Preprocessor(self.input_string, self.mods)
        self.temp = preprocessor.preprocess()

    def build_output(self):
        """ Ronseal. """
        self.lines = self.temp.split("\n")
        self.purge_whitespace()
        self.process_choruses()
        self.process_minichoruses()
        self.add_endings()
        self.process_syntactics()
        self.process_semantics()
        self.output_string = "\n".join(self.lines)

    def purge_whitespace(self):
        """ Ronseal. """
        for index, line in enumerate(self.lines):
            # Remove whitespace from line ends.
            while line.endswith(" "):
                line = line[:len(line)-1]
            self.lines[index] = line
        # Remove any trailing blank lines.
        while self.lines[len(self.lines)-1] == "":
            self.lines = self.lines[0:-1]

    def process_choruses(self):
        """ Handles choruses and inscriptions. """
        for index, line in enumerate(self.lines):
            if ("###CHORUS" in line) or ("###INSCRIPTION" in line):
                for line_num in range(index+1, len(self.lines)):
                    current_line = self.lines[line_num]
                    previous_line = self.lines[line_num-1]
                    if index == len(self.lines)-1:
                        self.lines[line_num] = current_line+"}"
                    elif current_line == "":
                        self.lines[line_num-1] = previous_line+"}"
                        break
                self.lines[index] = "{\\itshape "

    def process_minichoruses(self):
        """ Handles mini-choruses and mini-inscriptions. """
        for index, line in enumerate(self.lines):
            if ("##MINICHORUS" in line) or ("##MINIINSCRIPTION" in line):
                line = line.replace("##MINICHORUS ", "\\vin \\textit{")
                line = line.replace("##MINIINSCRIPTION ", "\\textit{")
                line = line+"}"
                self.lines[index] = line

    def add_endings(self):
        """ Adds "\\", "\\*" or "\\!" to each line, as appropriate. """
        if self.is_prose_poem:
            return
        for index, line in enumerate(self.lines):
            if (
                (line == "") or
                (line == "{\\itshape ") or
                (index == len(self.lines)-1)
               ):
                pass
            elif (index != len(self.lines)-1) and (self.lines[index+1] == ""):
                line = line+"\\\\!"
                self.lines[index] = line
            elif index in (0, len(self.lines)-2):
                line = line+"\\\\*"
                self.lines[index] = line
            elif self.lines[index-1] == "":
                line = line+"\\\\*"
                self.lines[index] = line
            elif (index < len(self.lines)-2) and (self.lines[index+2] == ""):
                line = line+"\\\\*"
                self.lines[index] = line
            else:
                line = line+"\\\\"
                self.lines[index] = line

    def process_syntactics(self):
        """ Translate those clusters for which clear equivalents exist. """
        for hpml_code, latex_code in EQUIVALENTS.items():
            self.replace_across_all_lines(hpml_code, latex_code)

    def replace_across_all_lines(self, old, new):
        """ Replace every instance of old with new across all lines. """
        for index, line in enumerate(self.lines):
            self.lines[index] = line.replace(old, new)

    def process_semantics(self):
        """ Ronseal. """
        self.process_places()
        self.process_persons()
        self.process_publications()
        self.process_foreign_strings()
        self.process_fractions()
        self.process_ampersands()
        self.process_stress()
        self.process_flagverses()
        self.process_subscript()
        self.process_whitespace()

    def process_places(self):
        """ Ronseal. """
        self.replace_across_all_lines("#PLACE{", "\\textsc{")

    def process_persons(self):
        """ Ronseal. """
        self.replace_across_all_lines("#PERSON{", "\\textit{")

    def process_publications(self):
        """ Ronseal. """
        self.replace_across_all_lines("#PUBLICATION{", "{\\hoskeroe ")

    def process_foreign_strings(self):
        """ Ronseal. """
        self.replace_across_all_lines("#FOREIGN{", "{\\hoskeroe ")

    def process_fractions(self):
        """ Ronseal. """
        for hpml_code, sub_dict in FRACTIONS.items():
            latex_code = sub_dict["latex"]
            self.replace_across_all_lines(hpml_code, latex_code)

    def process_ampersands(self):
        """ Ronseal. """
        self.replace_across_all_lines("#ADD", "\\&")

    def process_stress(self):
        """ Handles stressed syllables. """
        self.replace_across_all_lines("#STRESS{", "\\'{")

    def process_flagverses(self):
        """ Adds mini-titles to particular verses. """
        self.replace_across_all_lines(
            "##FLAGVERSE{",
            "\\flagverse{\\footnotesize "
        )

    def process_subscript(self):
        """ Ronseal. """
        self.replace_across_all_lines("#SUB{", "\\textsubscript{")

    def process_whitespace(self):
        """ Ronseal. """
        self.replace_across_all_lines("#WHITESPACE{", "\\textcolor{white}{")

    def save_to_file(self):
        """ Save the output string to a file. """
        if not self.path_to_output_file:
            raise HPMLCompilerException("No save file path specified.")
        with open(self.path_to_output_file, "w") as output_file:
            output_file.write(self.output_string)

################################
# HELPER CLASSES AND FUNCTIONS #
################################

class HPMLCompilerException(Exception):
    """ A custom exception. """
