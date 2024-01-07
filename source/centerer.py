"""
This code defines a class which generates a LaTeX string which CENTERS a given
poem on a page.
"""

##############
# MAIN CLASS #
##############

class Centerer:
    """ The class in question. """
    def __init__(self, input_string):
        self.input_string = input_string
        self.lines = input_string.split("\n")

    def purge_hpml_from_lines(self):
        """ Purge any HPML code from each line. """
        for index, line in enumerate(self.lines):
            self.lines[index] = purge_hpml_from_line(line)

    def get_second_longest_line(self):
        """ Ronseal. """
        result = self.lines[0]
        for line in self.lines:
            if len(line) > len(result):
                result = line
        return result

    def get_settowidth_string(self):
        """ Get the second longest PURGED line. """
        self.purge_hpml_from_lines()
        return self.get_second_longest_line()

####################
# HELPER FUNCTIONS #
####################

def purge_hpml_from_line(line):
    """ Purge any HPML code from a given line. """
    result = ""
    in_command = False
    for letter in line:
        if in_command:
            if letter == " ":
                in_command = False
                result += letter
            elif letter == "{":
                in_command = False
        elif letter == "#":
            in_command = True
        elif letter == "}":
            pass
        else:
            result += letter
    return result
