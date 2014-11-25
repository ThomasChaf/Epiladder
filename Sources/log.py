# ******************************************************************************
#                                                                              *
#                                    LOG PY                                    *
#                                                                              *
#              Display informations when verbose mode is activated             *
#                                                                              *
#  Created by Thomas Chafiol  -  thomaschaf@gmail.com  -  03  /  07  /  2013   *
# ******************************************************************************

class Log:
    NO_GPA          = "No GPA founded"
    NO_MOYENNE      = "No Moyenne founded"
    REQUEST_FAIL    = "Request failed"

    def __init__(self, verbose):
        self.verbose = verbose

    def write(self, string):
        if self.verbose == False:
            return
        print("\033[32m[INFO]", "\033[0m", string)

    def error(self, string):
        print("\033[31m[ERROR]", "\033[0m", string)
