from globals import *
from app import *

class TabMan(QWidget):
    def __init__(self, parent):
        #https://pythonspot.com/pyqt5-tabs/
        #super(QWidget, self).__init__(parent)
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)

        self.imgLists = parent.imgLists
        self.fileNames = parent.fileNames
        self.tabList = []
        self.tabManager = QTabWidget()
        self.tabManager.resize(300,200)
        self.layout.addWidget(self.tabManager)

        self.show()

    def addTab(self, images):
        idx = len(self.tabList)
        self.tabList.append(PdfDisplay(self.parent))
        self.tabList[idx].addPdfTab(images)
        self.tabManager.addTab(self.tabList[idx], self.fileNames[idx])

    def getPdfDisplay(self, idx):
        return self.tabList[idx]

    def getIdx(self):
        return self.tabManager.currentIndex()

class PdfDisplay(QWidget):

    def __init__(self, parent):
        #super(QWidget, self).__init__(parent)
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.images = []
        self.pixmaps = []
        self.labels = []
        self.textBoxes = {}
        self.textBoxConfirms = {}
        self.textBoxDeclines = {}

    def removeTextBox(self, textBoxHash):
        #https://stackoverflow.com/questions/5899826/pyqt-how-to-remove-a-widget
        self.textBoxes[textBoxHash].deleteLater()
        self.textBoxConfirms[textBoxHash].deleteLater()
        self.textBoxDeclines[textBoxHash].deleteLater()
        self.textBoxes[textBoxHash] = None
        self.textBoxConfirms[textBoxHash] = None
        self.textBoxDeclines[textBoxHash] = None

    def textBoxConfirmed(self,i, pos, pixmap, label, text):
        painter = QPainter(pixmap)
        painter.setFont(QFont('Arial', 50))
        painter.drawText(pos, text)
        label.setPixmap(pixmap)
        textBoxHash = "("+str(pos.x()) + "," +str(pos.y())+ ")"+  "_" + str(i)
        self.removeTextBox(textBoxHash)


    def textBoxDeclined(self, i, pos):
        textBoxHash = "("+str(pos.x()) + "," +str(pos.y())+ ")"+  "_" + str(i)
        self.removeTextBox(textBoxHash)
    #https://programtalk.com/python-examples/PyQt5.QtGui.QMouseEvent/
    def mousePressEventL(self, event, i, label, pixmap):
        global editMode
        if(not editMode):
            return

        pos = event.pos()

        #https://pythonspot.com/pyqt5-textbox-example/

        # Create textbox
        textBoxHash = "("+str(pos.x()) + "," +str(pos.y())+ ")"+  "_" + str(i)
        #print(textBoxHash+"\n\n")
        self.textBoxes[textBoxHash] = QLineEdit(self)
        self.textBoxes[textBoxHash].move(pos)
        self.textBoxes[textBoxHash].resize(280,40)

        # Create a button in the window
        self.textBoxConfirms[textBoxHash] = QPushButton('Confirm', self)
        self.textBoxConfirms[textBoxHash].move(pos.x(), pos.y()+40)
        self.textBoxDeclines[textBoxHash] = QPushButton('No', self)
        self.textBoxDeclines[textBoxHash].move(pos.x(), pos.y()+80)

        self.textBoxes[textBoxHash].show()
        self.textBoxConfirms[textBoxHash].show()
        self.textBoxDeclines[textBoxHash].show()

        # connect button to function on_click
        self.textBoxConfirms[textBoxHash].clicked.connect(lambda :self.textBoxConfirmed(i, pos, pixmap, label, self.textBoxes[textBoxHash].text()))
        self.textBoxDeclines[textBoxHash].clicked.connect(lambda :self.textBoxDeclined(i, pos))



    def attachMousePressEvent(self, i):
        self.labels[i].mousePressEvent = lambda event: self.mousePressEventL(event, i, self.labels[i], self.pixmaps[i])

    #https://stackoverflow.com/questions/17002260/how-to-make-a-pyqt-tabbed-interface-with-scroll-bars
    def addPdfTab(self, images):

        pdfWidget = QWidget()
        imageSet = QVBoxLayout(pdfWidget)
        self.images = images


        for i in range(0, len(images)):
            label = QLabel(self)
            pixmap = QPixmap(images[i])

            #https://stackoverflow.com/questions/3504522/pyqt-get-pixel-position-and-value-when-mouse-click-on-the-image

            label.setGeometry(0,0,10,10)
            label.setPixmap(pixmap)
            self.pixmaps.append(pixmap)
            self.labels.append(label)
            imageSet.addWidget(label)

        for i in range(0, len(self.labels)):
            self.attachMousePressEvent(i);




        pdfWidget.layout = imageSet

        self.pdfScroll = QScrollArea()
        self.pdfScroll.setWidget(pdfWidget)
        self.pdfScroll.setFixedWidth(2000)
        self.pdfScroll.setFixedHeight(1000)
        self.layout.addWidget(self.pdfScroll)

        self.pdfScroll.show();