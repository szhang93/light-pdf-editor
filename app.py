#!/usr/bin/python3

from globals import *
from basicFunctions import *
from pdfDisplay import *
from tools import *
#Many references used from :
#https://pythonspot.com/pyqt5/
#http://zetcode.com/gui/pyqt5/widgets2/


class App(QMainWindow):
    #Creates main window
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        #Geometry info
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        #Hard coded for now.
        self.fullPath = "/home/shini/Documents/projects/pdfEditor/pythonEnv/src"

        #imgList for pdf files is stored in the main App
        self.imgLists = [] #list of image Lists
        self.fileNames = []

        self.initUI()
        self.showMaximized() #fullscreen

    #basic tester
    def testPopup(self):
        QMessageBox.about(self, "message")

    def openFile(self):
        st = self.tabMan.getIdx()+1; #since tab hasn't been created yet

        myPDF = QFileDialog.getOpenFileName(self, "open PDF", self.fullPath, "PDF Files(*.pdf)")
        baseName = os.path.basename(myPDF[0])
        #temporarily stores the opened images
        tempPath = self.fullPath+"/temp/"

        #Converts pdf to series of images.
        images = convert_from_path(myPDF[0])


        pg = 0 #page counter
        tempImgList = [] #list
        #imgList=[] #stores path of list of images
        for image in images:
            image.save(tempPath+baseName+str(pg)+".jpg","JPEG") #saves images to a path
            tempImgList.append(tempPath+baseName+str(pg)+".jpg")
            pg+=1
        self.imgLists.append(tempImgList)
        self.fileNames.append(baseName)
        self.tabMan.addTab(self.imgLists[st])

    def saveFile(self):
        pg = 0;
        st = self.tabMan.getIdx();
        for myPix in self.tabMan.getPdfDisplay(st).pixmaps:
            myPix.save(self.imgLists[st][pg], "JPG")
            pg+=1;

        #https://stackoverflow.com/questions/27327513/create-pdf-from-a-list-of-images
        myPDF = QFileDialog.getSaveFileName(self, "save PDF", self.fullPath, "PDF Files(*.pdf)")
        myPDF = os.path.basename(myPDF[0])
        with open(myPDF,"wb") as f:
            f.write(img2pdf.convert(self.imgLists[st]))



    def displayImg(self,images):
        pixmap = QPixmap()
        for i in range(0, len(images)):
            pixmap.loadFromData(images[i])

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)


    def toggleEditOnOff(self):
        global editMode
        if(editMode):
            editMode = False;
            print("edit mode:", editMode)
        else:
            editMode = True;
            print("edit mode:", editMode)


    def confirmEdit(self):
        tab = self.tabMan.tabList[self.tabMan.getIdx()];
        tab.textBoxConfirmed();

    def cancelEdit(self):
        tab = self.tabMan.tabList[self.tabMan.getIdx()];
        tab.textBoxCanceled();

    def changeFont(self, event):
        #https://stackoverflow.com/questions/6061893/how-do-you-get-the-current-text-contents-of-a-qcombobox
        font = str(self.comboFonts.currentText())
        fontSizeStr = self.fontSize.toPlainText()
        fontSize = 12
        if(int(fontSizeStr)):
            fontSize = int(fontSizeStr)

        for myPdfDisplay in self.tabMan.tabList:
            myPdfDisplay.font = font;
            myPdfDisplay.fontSize = fontSize;
        print("changed to font:", font, "size:", fontSize)

    #USER INTERFACE
    def initUI(self):


        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #menuBar
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('File')
        openFile = fileMenu.addAction("Open")
        saveFile = fileMenu.addAction("Save")
        editMenu = mainMenu.addMenu('Edit')
        editFile = editMenu.addAction("Edit Mode")


        #editFile.triggered.connect(self.toggleEditOnOff)
        #self.pdfDisplay = PdfDisplay(self)
        self.tabMan = TabMan(self)
        self.tools = Tools(self)

        self.toolbar = self.addToolBar("toolbar")
        #http://zetcode.com/gui/pyqt5/menustoolbars/

        add = QAction(QIcon('icons/plus.png'), 'Add', self)
        add.triggered.connect(self.openFile)
        add.setShortcut("Ctrl+O")

        save = QAction(QIcon('icons/bookmark.png'), 'Save', self)
        save.triggered.connect(self.saveFile)
        save.setShortcut("Ctrl+S")

        hand = QAction(QIcon('icons/hand.png'), 'Hand', self)

        edit = QAction(QIcon('icons/pencil.png'), 'Edit', self)
        edit.triggered.connect(self.toggleEditOnOff)

        settings = QAction(QIcon('icons/settings.png'), 'Settings', self)

        confirm = QAction(QIcon('icons/checkmark.png'), 'Confirm', self)
        confirm.triggered.connect(self.confirmEdit)


        cancel = QAction(QIcon('icons/x.png'), 'Cancel', self)
        cancel.triggered.connect(self.cancelEdit)

        self.toolbar.addAction(add)

        self.toolbar.addAction(save)
        self.toolbar.addAction(hand)
        self.toolbar.addAction(edit)
        self.toolbar.addAction(settings)
        self.toolbar.addAction(confirm)
        self.toolbar.addAction(cancel)

        #https://pythonprogramming.net/drop-down-button-window-styles-pyqt-tutorial/
        #https://stackoverflow.com/questions/17152979/i-have-a-pyqt-mainwindow-how-can-i-load-fonts-in-qlistwidget

        allFonts = QFontDatabase().families()
        self.comboFonts = QComboBox(self)
        for myFont in allFonts:
            self.comboFonts.addItem(myFont)
        self.toolbar.addWidget(self.comboFonts)


        #fonts.activated[str].connect(self.changeFont)



        self.fontSize = QTextEdit(self)
        self.toolbar.addWidget(self.fontSize)

        self.fontConfirm = QPushButton("Confirm", None)
        self.toolbar.addWidget(self.fontConfirm)
        self.fontConfirm.mousePressEvent=self.changeFont



        self.layout.addWidget(self.tools)
        self.layout.addWidget(self.tabMan)
        self.setCentralWidget(self.tabMan)

        openFile.triggered.connect(self.openFile)
        #https://stackoverflow.com/questions/940555/pyqt-sending-parameter-to-slot-when-connecting-to-a-signal
        saveFile.triggered.connect(self.saveFile)




        self.show()


    #EXITING PROGRAM
    def exiting(self):
        tempPath = self.fullPath+"/temp/"
        for file in os.listdir(tempPath):
            os.remove(tempPath+file)
