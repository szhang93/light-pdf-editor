#!/usr/bin/python3

import sys
import atexit
import os
import PyPDF2
import img2pdf
from pdf2image import convert_from_path, convert_from_bytes
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QMessageBox, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QLabel, QScrollArea

from basicFunctions import *
#Many references used from :
#https://pythonspot.com/pyqt5/
#http://zetcode.com/gui/pyqt5/widgets2/
class App(QMainWindow):

    #Creates main window


    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.fullPath = "/home/shini/Documents/projects/pdfEditor/pythonEnv/src"


        self.imgList = [] #list of images
        self.initUI()
        self.showMaximized()

    def testPopup(self):
        QMessageBox.about(self, "message")

    def openFile(self):
        myPDF = QFileDialog.getOpenFileName(self, "open PDF", self.fullPath, "PDF Files(*.pdf)")
        print(myPDF[0]) #getOpenFileName returns an array
        baseName = os.path.basename(myPDF[0])
        print(baseName)

        tempPath = self.fullPath+"/temp/"

        #Converts pdf to series of images.
        images = convert_from_path(myPDF[0])

        pg = 0 #page counter
        #imgList=[] #stores path of list of images
        for image in images:
            image.save(tempPath+baseName+str(pg)+".jpg","JPEG") #saves images to a path
            self.imgList.append(tempPath+baseName+str(pg)+".jpg")
            pg+=1

        self.pdfDisplay.addPdfTab(self.imgList)
        #self.displayImg(images)

    def saveFile(self):
        #https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
        myPDF = QFileDialog.getSaveFileName(self, "save PDF", self.fullPath, "PDF Files(*.pdf)")
        myPDF = os.path.basename(myPDF[0])
        print("list of images to pdf:\n",self.imgList)
        with open(myPDF,"wb") as f:
            f.write(img2pdf.convert(self.imgList))



    def displayImg(self,images):
        print(images)
        pixmap = QPixmap()
        for i in range(0, len(images)):
            pixmap.loadFromData(images[i])

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

    #USER INTERFACE
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('File')
        openFile = fileMenu.addAction("Open")
        saveFile = fileMenu.addAction("Save")
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        self.pdfDisplay = PdfDisplay(self)
        self.setCentralWidget(self.pdfDisplay)

        openFile.triggered.connect(self.openFile)
        #https://stackoverflow.com/questions/940555/pyqt-sending-parameter-to-slot-when-connecting-to-a-signal
        saveFile.triggered.connect(self.saveFile)

        self.show()

    #EXITING PROGRAM
    def exiting(self):
        tempPath = self.fullPath+"/temp/"
        for file in os.listdir(tempPath):
            os.remove(tempPath+file)


class PdfDisplay(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.images = []
        self.pixmaps = []
        self.labels = []


    #https://programtalk.com/python-examples/PyQt5.QtGui.QMouseEvent/
    def mousePressEvent(self, event, label, pixmap):
        print(self.labels[0])
        print(self.labels[1])
        print(self.labels[2])
        print(label)
        print(event)
        pos = event.pos()
        print(pos)
        painter = QPainter(pixmap)
        painter.setFont(QFont('Arial', 50))
        painter.drawText(pos, "hello world")
        label.setPixmap(pixmap)


    #https://stackoverflow.com/questions/17002260/how-to-make-a-pyqt-tabbed-interface-with-scroll-bars
    def addPdfTab(self, images):

        pdfWidget = QWidget()
        imageSet = QVBoxLayout(pdfWidget)
        self.images = images


        for i in range(0, len(images)):
            label = QLabel(self)
            pixmap = QPixmap(images[i])

            #https://stackoverflow.com/questions/3504522/pyqt-get-pixel-position-and-value-when-mouse-click-on-the-image
            #addTextWithPix = lambda x : addText(pixmap)
            #addTextWithPix = lambda


            label.setGeometry(0,0,10,10)
            label.setPixmap(pixmap)
            self.pixmaps.append(pixmap)
            self.labels.append(label)
            imageSet.addWidget(label)

        self.labels[0].mousePressEvent = lambda event: self.mousePressEvent(event, self.labels[0], self.pixmaps[0])
        self.labels[1].mousePressEvent = lambda event: self.mousePressEvent(event, self.labels[1], self.pixmaps[1])
        self.labels[2].mousePressEvent = lambda event: self.mousePressEvent(event, self.labels[2], self.pixmaps[2])
        #for i in range(0, len(self.labels)):
            #self.labels[i].mousePressEvent = lambda event: self.mousePressEvent(event, self.labels[i], self.pixmaps[i])
            #self.labels[i].setScaledContents(True)



        pdfWidget.layout = imageSet
        #https://www.programcreek.com/python/example/82631/PyQt5.QtWidgets.QScrollArea
        self.pdfScroll = QScrollArea()
        self.pdfScroll.setWidget(pdfWidget)
        self.pdfScroll.setFixedWidth(2000)
        self.pdfScroll.setFixedHeight(1000)
        self.layout.addWidget(self.pdfScroll)
        #pdfScroll.setWidgetResizable(True)

        self.pdfScroll.show();
        #label.show()
