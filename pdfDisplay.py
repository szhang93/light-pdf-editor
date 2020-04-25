from globals import *
from app import *
from textBox import *
from rect import *
from leftpanel import *

class TabMan(QWidget):
    def __init__(self, parent):
        #https://pythonspot.com/pyqt5-tabs/
        #super(QWidget, self).__init__(parent)
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout(self)

        self.imgLists = parent.imgLists
        self.fileNames = parent.fileNames
        self.tabList = []
        self.tabManager = QTabWidget()
        self.tabManager.setTabsClosable(True)
        self.tabManager.tabCloseRequested.connect(self.closeTab)
        #self.tabManager.resize(parent.width,parent.height)

        self.height = parent.height
        """
        self.leftPanel = LeftPanel(self)
        self.leftPanel.resize(900,parent.height)
        self.leftPanel.show()

        self.layout.addWidget(self.leftPanel)

        self.pdfPages = QWidget(self)
        self.scrollArea2 = QScrollArea(self.pdfPages)
        self.scrollArea2.resize(parent.width,parent.height)
        self.pdfPages.resize(parent.width, parent.height)
        self.pdfPages.layout = QVBoxLayout(self.pdfPages)

        self.pdfPages.layout.addWidget(self.tabManager)

        self.layout.addWidget(self.pdfPages)
        """

        self.layout.addWidget(self.tabManager)

        self.scenes = []
        self.views = []

        self.show()

    def closeTab(self,idx):
        del self.imgLists[idx]
        del self.fileNames[idx]
        del self.tabList[idx]

        self.tabManager.removeTab(idx)


    def addTab(self, images):
        idx = len(self.tabList) #should have same number of scenes
        #self.scenes.append(QGraphicsScene(self.parent))


        self.tabList.append(PdfDisplay(self.parent))
        self.tabList[idx].addPdfTab(images)
        #self.scenes[idx].addWidget(self.tabList[idx])

        #self.views.append(QGraphicsView(self.scenes[idx], self.parent))

        #imgWidth = self.parent.imgWidths[idx]
        #scale to 900
        #ratio = 2000.0/imgWidth
        #print(ratio)

        #self.views[idx].scale(ratio, ratio)

        #self.scenes[idx].setSceneRect(QRectF(0,0,1000,1000))
        #print(self.scenes[idx].sceneRect())
        #self.scenes[idx].setSceneRect(QRectF(0,0,1000,1000))


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
        self.boxFields = []
        self.pageForms = [] #layouts
        self.pages = []
        self.boxFieldNum = 0


        self.font = parent.globalFont
        self.italic = False;
        self.fontSize = parent.globalFontSize



    def textBoxConfirmed(self):


        for textBox in self.boxFields:
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

            option = QTextOption();
            option.QWrapMode = QTextOption.WordWrap;
            painter.drawText(rect, text, option)
            textBox.label.setPixmap(textBox.pixmap)
            #https://stackoverflow.com/questions/5899826/pyqt-how-to-remove-a-widget
            textBox.__del__()
            painter.end()

    def textBoxCanceled(self):
        for textBox in self.boxFields:
            if textBox == None:
                continue
            textBox.__del__()


    #https://programtalk.com/python-examples/PyQt5.QtGui.QMouseEvent/
    def mousePressEventL(self, event, i, label, pixmap):
        global editMode
        print("editMode:",editMode)
        if(editMode==False):
            return


        pos = event.pos()

        #https://pythonspot.com/pyqt5-textbox-example/

        # Create textbox
        #print(textBoxHash+"\n\n")
        self.boxFields.append(TextBox(self, pos, i, self.boxFieldNum, pixmap, label))
        self.boxFieldNum+=1

    def mouseMoveEventL(self, event, i, label, pixmap):
        selected = self.boxFields[self.boxFieldNum-1];

        selected.actionDrag(event, selected.bottomRight)

    def mouseReleaseEventL(self, event, i, label, pixmap):
        selected = self.boxFields[self.boxFieldNum-1];
        selected.actionDragFin(event, selected.bottomRight)
        selected.fresh = False;


    def attachMousePressEvent(self, i):
        self.labels[i].mousePressEvent = lambda event: self.mousePressEventL(event, i, self.labels[i], self.pixmaps[i])
        self.labels[i].mouseMoveEvent = lambda event: self.mouseMoveEventL(event, i, self.labels[i], self.pixmaps[i])
        self.labels[i].mouseReleaseEvent = lambda event: self.mouseReleaseEventL(event, i, self.labels[i], self.pixmaps[i])


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
            #label.resize(500,500)

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
