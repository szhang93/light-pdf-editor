#!/usr/bin/python3

from globals import *
from pdfDisplay import *

#Many references used from :
#https://pythonspot.com/pyqt5/
#http://zetcode.com/gui/pyqt5/widgets2/


class App(QMainWindow):



    #Creates main window
    def __init__(self):
        super().__init__()
        #https://stackoverflow.com/questions/14506787/reading-pyqt-stylesheet-from-external-qss-file
        style="style.stylesheet"
        with open(style,"r") as fh:
            self.setStyleSheet(fh.read())


        self.layout = QVBoxLayout()
        #Geometry info
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 1000

        self.globalFont = ("Arial")

        self.globalFontSize = 12

        #Hard coded for now.
        self.fullPath = "/home/shini/Documents/projects/pdfEditor/pythonEnv/src"

        #imgList for pdf files is stored in the main App
        self.imgLists = [] #list of image Lists
        self.fileNames = []
        self.imgWidths = []

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

    def changeFont(self, event, keyPressed):
        if keyPressed:
            if event.key() != Qt.Key_Return:
                print("Not enter")
                #https://stackoverflow.com/questions/18575635/pyqt-pyside-keypressevent-default-behaviour
                #super(QTextEdit, self.fontSize).keyPressEvent(event)
                if(event.key()==Qt.Key_Backspace):
                    print("backspace")
                    self.fontSize.setText(self.fontSize.toPlainText()[:-1])
                elif (event.key()>=48) and (event.key()<=57):
                    self.fontSize.setText(self.fontSize.toPlainText()+chr(event.key()))
                else:
                    print("not allowed")
                return

        #https://stackoverflow.com/questions/6061893/how-do-you-get-the-current-text-contents-of-a-qcombobox
        self.globalFont = str(self.comboFonts.currentText())
        fontSizeStr = self.fontSize.toPlainText()
        self.globalFontSize = 12
        if(int(fontSizeStr)):
            self.globalFontSize = int(fontSizeStr)


        print("changed to font:", self.globalFont, "size:", self.globalFontSize)


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

        #https://stackoverflow.com/questions/13779752/how-to-set-the-default-item-of-a-qcombobox
        # self.comboFonts.setCurrentIndex(allFonts.index('Arial'))


        #fonts.activated[str].connect(self.changeFont)



        self.fontSize = QTextEdit(self)
        self.fontSize.setText("12")

        self.fontSize.setFixedSize(50,20)
        self.fontSize.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        self.toolbar.addWidget(self.fontSize)

        self.fontConfirm = QPushButton("Confirm", None)
        self.toolbar.addWidget(self.fontConfirm)
        self.fontSize.keyPressEvent=lambda event: self.changeFont(event, True)
        self.fontConfirm.mousePressEvent=lambda event: self.changeFont(event, False)




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
