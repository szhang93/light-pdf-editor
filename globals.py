#!/usr/bin/python3
#IMPORTS
import sys
import atexit
import os
import PyPDF2
import img2pdf
from pdf2image import convert_from_path, convert_from_bytes
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QMessageBox, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QLabel, QScrollArea, QLineEdit, QMessageBox



#Global variables
editMode = True;
selectedTab = 0;
