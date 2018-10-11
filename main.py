#!/usr/bin/python3



import sys
import atexit
import os
import PyPDF2
from pdf2image import convert_from_path, convert_from_bytes
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QMessageBox, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QLabel, QScrollArea

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
        self.fullPath = "/home/shini/Documents/pdfEditor/pythonEnv/src"
        self.initUI()
        self.showMaximized()

    def testPopup(self):
        QMessageBox.about(self, "Warning!", "Your computer is infected with Ebola")

    def openFile(self):
        myPDF = QFileDialog.getOpenFileName()
        print(myPDF[0]) #getOpenFileName returns an array
        baseName = os.path.basename(myPDF[0])
        print(baseName)

        tempPath = self.fullPath+"/temp/"

        #Converts pdf to series of images.
        images = convert_from_path(myPDF[0])

        pg = 0 #page counter
        imgList=[] #stores path of list of images
        for image in images:
            image.save(tempPath+baseName+str(pg)+"jpg","JPEG") #saves images to a path
            imgList.append(tempPath+baseName+str(pg)+"jpg")
            pg+=1

        self.pdfDisplay.addPdfTab(imgList)
        #self.displayImg(images)

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
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        self.pdfDisplay = PdfDisplay(self)


        self.setCentralWidget(self.pdfDisplay)

        openFile.triggered.connect(self.openFile)

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








    #https://stackoverflow.com/questions/17002260/how-to-make-a-pyqt-tabbed-interface-with-scroll-bars

    def addPdfTab(self, images):

        pdfWidget = QWidget()
        imageSet = QVBoxLayout(pdfWidget)

        for i in range(0, len(images)):
            label = QLabel(self)
            pixmap = QPixmap(images[i])
            label.setPixmap(pixmap)
            label.setGeometry(0,0,2000,2000)
            imageSet.addWidget(label)

        pdfWidget.layout = imageSet





        #https://www.programcreek.com/python/example/82631/PyQt5.QtWidgets.QScrollArea
        self.pdfScroll = QScrollArea()
        self.pdfScroll.setWidget(pdfWidget)
        self.pdfScroll.setFixedWidth(2000);
        self.pdfScroll.setFixedHeight(1000);
        #pdfScroll.setWidgetResizable(True)

        self.pdfScroll.show();
        #label.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    appExec = app.exec_()
    atexit.register(ex.exiting)
    sys.exit(appExec)
