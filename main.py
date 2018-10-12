#!/usr/bin/python3

import sys
import atexit
import os
from mainUI import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    appExec = app.exec_()
    atexit.register(ex.exiting)
    sys.exit(appExec)
