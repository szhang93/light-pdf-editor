from globals import *
from app import *
from textBox import *

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
        #self.layout.addWidget(self.tabList[idx])
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
        self.textBoxes = []
        self.pageForms = [] #layouts
        self.pages = []
        self.textBoxNum = 0


        self.font = "Arial";
        self.italic = False;
        self.fontSize = 12;



    def textBoxConfirmed(self):


        for textBox in self.textBoxes:
            if textBox == None:
                continue
            x = textBox.topLeftPos.x()
            y = textBox.topLeftPos.y()
            width = textBox.textEdit.frameGeometry().width()
            height = textBox.textEdit.frameGeometry().height()
            text = textBox.textEdit.toPlainText()

            rect = QRectF(x, y, width, height);
            painter = QPainter(textBox.pixmap)
            painter.begin(self)
            painter.setFont(QFont(textBox.font, textBox.fontSize))
            #painter.drawText(pos.x(), pos.y()+self.fontSize, text)

            painter.drawText(rect, text, option = QTextOption())
            textBox.label.setPixmap(textBox.pixmap)
            #https://stackoverflow.com/questions/5899826/pyqt-how-to-remove-a-widget
            textBox.__del__()
            painter.end()

    def textBoxCanceled(self):
        for textBox in self.textBoxes:
            if textBox == None:
                continue
            textBox.__del__()


    #https://programtalk.com/python-examples/PyQt5.QtGui.QMouseEvent/
    def mousePressEventL(self, event, i, label, pixmap):
        global editMode
        if(not editMode):
            return

        pos = event.pos()

        #https://pythonspot.com/pyqt5-textbox-example/

        # Create textbox
        #print(textBoxHash+"\n\n")
        self.textBoxes.append(TextBox(self, pos, i, self.textBoxNum, pixmap, label))
        self.textBoxNum+=1




    def attachMousePressEvent(self, i):
        self.labels[i].mousePressEvent = lambda event: self.mousePressEventL(event, i, self.labels[i], self.pixmaps[i])

    #https://stackoverflow.com/questions/17002260/how-to-make-a-pyqt-tabbed-interface-with-scroll-bars
    def addPdfTab(self, images):

        pdfWidget = QWidget()
        imageSet = QVBoxLayout(pdfWidget)
        self.images = images


        for i in range(0, len(images)):
            page = QWidget()
            pageLayout = QVBoxLayout(page)
            self.pageForms.append(pageLayout)
            self.pages.append(page)

            label = QLabel(self)
            pixmap = QPixmap(images[i])

            #https://stackoverflow.com/questions/3504522/pyqt-get-pixel-position-and-value-when-mouse-click-on-the-image

            label.setGeometry(0,0,10,10)
            label.setPixmap(pixmap)
            label.hasScaledContents();
            label.resize(500,500)

            self.pageForms[i].addWidget(label)

            self.pixmaps.append(pixmap)
            self.labels.append(label)
            imageSet.addWidget(page) #stacked layout one

        for i in range(0, len(self.labels)):
            self.attachMousePressEvent(i);




        pdfWidget.layout = imageSet

        self.pdfScroll = QScrollArea()
        self.pdfScroll.setWidget(pdfWidget)
        self.pdfScroll.setWidgetResizable(True)
        #self.pdfScroll.setFixedWidth(2000)
        #self.pdfScroll.setFixedHeight(1000)
        self.layout.addWidget(self.pdfScroll)

        self.pdfScroll.show();
