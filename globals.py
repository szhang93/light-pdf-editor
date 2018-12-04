#!/usr/bin/python3
#IMPORTS
import sys
import atexit
import os
import PyPDF2
import img2pdf
from pdf2image import convert_from_path, convert_from_bytes
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



#Global variables
editMode = True;
selectedTab = 0;
