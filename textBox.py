#!/usr/bin/python3

from globals import *


defX = 300
defY = 300
class TextBox(QObject):

    def __init__ (self, parent, pos, i):
        super().__init__()

        self.parent = parent
        #coordinate positions

        self.topLeftPos = pos
        self.topRightPos = QPoint(pos.x()+defX, pos.y())
        self.bottomLeftPos = QPoint(pos.x(), pos.y()+defY)
        self.bottomRightPos = QPoint(pos.x()+defX, pos.y()+defY)

        self.topLeft = self.createDot(pos, parent.pages[i])
        self.topRight = self.createDot(QPoint(pos.x()+defX, pos.y()),parent.pages[i]);
        self.bottomLeft = self.createDot(QPoint(pos.x(), pos.y()+defY),parent.pages[i]);
        self.bottomRight = self.createDot(QPoint(pos.x()+defX, pos.y()+defY),parent.pages[i]);

        self.addListeners(self.topLeft)
        self.addListeners(self.topRight)
        self.addListeners(self.bottomLeft)
        self.addListeners(self.bottomRight)

        self.initialPosition = pos

        self.textEdit = QTextEdit(parent.pages[i])
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        self.textEdit.setLineWrapMode(1);

        self.textEdit.setCurrentFont(QFont(parent.font,parent.fontSize))
        #self.pageForms[i].addWidget(self.textEdit);
        self.textEdit.move(pos)
        self.textEdit.resize(defX, defY)
        self.textEdit.setStyleSheet("background: rgba(0,0,0,0%)")

        self.textEdit.show()
        #create text field with default coordinates

        #create draggable dots with default coordinates

        #define action listener.
    def createDot(self, pos, parent):
        label = QLabel(parent)
        label.move(pos)
        label.resize(10,10)
        label.setStyleSheet("background: rgba(100,0,0,100%)")
        label.show()
        #https://stackoverflow.com/questions/11172420/moving-object-with-mouse


        return label

    def addListeners(self, obj):
        obj.mousePressEvent = lambda event: self.saveInitialPosition(event, obj)
        obj.mouseReleaseEvent = lambda event: self.actionDragFin(event, obj)
        obj.mouseMoveEvent = lambda event: self.actionDrag(event, obj);

    def actionMove(self, event, obj):
        return 0


        #if clicked inside box coordinates

    def actionDrag(self, event, obj):
        pos = QCursor.pos()
        obj.move(pos)
        #if dragging corners

    def actionDragFin(self, event, obj):
        pos = QCursor.pos()
        obj.move(pos)
        offsetX = pos.x() - self.initialPosition.x()
        offsetY = pos.y() - self.initialPosition.y()
        if(obj is self.topLeft):
            self.topLeftPos = pos
            self.topRightPos = QPoint(self.topRightPos.x(), self.topRightPos.y()+offsetY)
            self.bottomLeftPos = QPoint(self.bottomLeftPos.x()+offsetX, self.bottomLeftPos.y())
            self.topRight.move(self.topRightPos)
            self.bottomLeft.move(self.bottomLeftPos)

        elif(obj is self.topRight):
            return 0
        elif(obj is self.bottomLeft):
            self.bottomLeftPos = pos
            self.bottomRightPos = QPoint(self.bottomRightPos.x(), self.bottomRightPos.y()+offsetY)
            self.topLeftPos = QPoint(self.topLeftPos.x()+offsetX, self.topLeftPos.y())
            self.bottomRight.move(self.bottomRightPos)
            self.topLeft.move(self.topLeftPos)
        elif(obj is self.bottomRight):
            return 0
        else:
            print("actionDragFin Error")
        obj.show()

    def saveInitialPosition(self, event, obj):
        if(obj is self.topLeft):
            self.initialPosition = self.topLeftPos
        elif(obj is self.topRight):
            self.initialPosition = self.topRightPos
        elif(obj is self.bottomLeft):
            self.initialPosition = self.bottomLeftPos
        elif(obj is self.bottomRight):
            self.initialPosition = self.bottomRightPos
        else:
            print("saveInitialPosition Error")

    def __del__(self):
        self.topLeft.deleteLater()
        self.topRight.deleteLater()
        self.bottomLeft.deleteLater()
        self.bottomRight.deleteLater()
        self.textEdit.deleteLater()
