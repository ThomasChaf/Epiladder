#!/usr/bin/env python3
# ******************************************************************************
#                                                                              *
#                                   MAIN PY                                    *
#                                                                              *
#  Created by Thomas Chafiol  -  thomaschaf@gmail.com  -  03  /  07  /  2013   *
# ******************************************************************************

import sys
from epilader import Epilader

if __name__ == "__main__":
    epilader = Epilader(sys.argv)
    epilader.set_cookies()
    epilader.launch()
    epilader.sort()
    epilader.display()
    del epilader
