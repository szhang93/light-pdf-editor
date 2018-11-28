#!/usr/bin/python3

# Main entrance

import sys
import atexit
import os
from app import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    appExec = app.exec_()
    atexit.register(ex.exiting)
    sys.exit(appExec)
