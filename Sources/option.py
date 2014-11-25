# ******************************************************************************
#                                                                              *
#                                  OPTION PY                                   *
#                                                                              *
# Retrieve options passed through the arguments (ex: --verbose = verbose mode) *
#                                                                              *
# ******************************************************************************

import sys

class Option:
    VERBOSE = "--verbose"

    def __init__(self):
        self.output = 1
        self.options = {}
        self.options[Option.VERBOSE] = False

    def help(self):
        print("\t\t\tEpiladder\n")
        print("Options:\n")
        print("\t--help Display some explications")
        print("\t--verbose Verbose mode")
        print("\t--file=filename File which will used to save results\n")

    def parse(self, arg):
        for a in arg:
            if a in self.options:
                self.options[a] = True
            elif a.startswith("--file"):
                self.output = open(a[7:], 'w')
            elif a == '--help':
                self.help()
                sys.exit()

    def write(self, string):
        if self.output != 1:
            self.output.write(string)
        else:
            print(string)

    def isVerboseMode(self):
        return (self.options[Option.VERBOSE])
