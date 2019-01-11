#!/usr/bin/python3

from globals import *



class BoxField(QObject):

    # i is page num
    def __init__ (self, parent, pos, i, BoxNum, pixmap, label):
        super().__init__()
        self.parent = parent
        #coordinate positions
        #https://stackoverflow.com/questions/48716193/how-to-change-qlineedit-spacing-between-text-and-its-edge
        fontHeight = QFontMetrics(QFont(parent.font)).height()
        self.sizeX = 0
        self.sizeY = 0

        self.label = label
        self.pixmap = pixmap
        self.index = BoxNum
        self.topLeftPos = QPoint(pos.x()-10, pos.y()-10)
        self.topRightPos = QPoint(pos.x()+self.sizeX, pos.y()-10)
        self.bottomLeftPos = QPoint(pos.x()-10, pos.y()+self.sizeY)
        self.bottomRightPos = QPoint(pos.x()+self.sizeX, pos.y()+self.sizeY)

        self.topLeft = self.createDot(self.topLeftPos, parent.pages[i])
        self.topRight = self.createDot(self.topRightPos,parent.pages[i]);
        self.bottomLeft = self.createDot(self.bottomLeftPos,parent.pages[i]);
        self.bottomRight = self.createDot(self.bottomRightPos,parent.pages[i]);

        self.addListeners(self.topLeft)
        self.addListeners(self.topRight)
        self.addListeners(self.bottomLeft)
        self.addListeners(self.bottomRight)

        self.initialPosition = pos
        self.movingPosition = pos

        self.boxField = QRect(pos, QSize(100, 100))
        self.boxField.moveCenter(pos)
        self.boxField.setSize(QSize(100,100))

        #https://www.programcreek.com/python/example/99581/PyQt5.QtCore.QRect
        self.painter = QPainter(pixmap)
        self.color = QColor(100,100,100)
        self.painter.fillRect(self.boxField,QBrush(self.color))



        #cancel = QAction(QIcon('icons/x.png'), 'Cancel', self)
        self.cancel = QPushButton(QIcon('icons/x.png'),"",parent.pages[i])
        self.cancel.move(QPoint(self.topRightPos.x(), self.topRightPos.y())) #64 is pixel height
        self.cancel.show()
        #self.cancel.keyPressEvent = self.__del__
        self.cancel.mousePressEvent = lambda event: self.__del__()
        #create text field with default coordinates

        #create draggable dots with default coordinates

        #define action listener.

    def createDot(self, pos, parent):
        label = QLabel(parent)
        label.move(pos)
        label.resize(10,10)
        label.setStyleSheet("background: rgba(0,0,0,100%)")
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
        #pos = QCursor.pos()
        self.movingPosition = self.movingPosition + event.pos()
        obj.move(self.movingPosition)

        #if dragging corners

    def actionDragFin(self, event, obj):
        #pos = QCursor.pos()
        pos = self.movingPosition + event.pos()
        obj.move(pos)
        offsetX = pos.x() - self.initialPosition.x()
        offsetY = pos.y() - self.initialPosition.y()
        if(obj is self.topLeft):
            self.topLeftPos = pos
            self.topRightPos = QPoint(self.topRightPos.x(), self.topRightPos.y()+offsetY)
            self.bottomLeftPos = QPoint(self.bottomLeftPos.x()+offsetX, self.bottomLeftPos.y())
            self.topRight.move(self.topRightPos)
            self.bottomLeft.move(self.bottomLeftPos)
            self.boxField.moveCenter(QPoint(self.topLeftPos.x()+10, self.topLeftPos.y()+10))
            self.sizeX = self.sizeX - offsetX
            self.sizeY = self.sizeY - offsetY
            self.boxField.setSize(QSize(self.sizeX,self.sizeY))

        elif(obj is self.topRight):
            self.topRightPos = pos
            self.bottomRightPos = QPoint(self.bottomRightPos.x()+offsetX, self.bottomRightPos.y())
            self.topLeftPos = QPoint(self.topLeftPos.x(), self.topLeftPos.y()+offsetY)
            self.bottomRight.move(self.bottomRightPos)
            self.topLeft.move(self.topLeftPos)
            self.boxField.moveCenter(QPoint(self.topLeftPos.x()+10, self.topLeftPos.y()+10))
            self.sizeX = self.sizeX + offsetX
            self.sizeY = self.sizeY - offsetY
            self.boxField.setSize(QSize(self.sizeX,self.sizeY))

        elif(obj is self.bottomLeft):
            self.bottomLeftPos = pos
            self.bottomRightPos = QPoint(self.bottomRightPos.x(), self.bottomRightPos.y()+offsetY)
            self.topLeftPos = QPoint(self.topLeftPos.x()+offsetX, self.topLeftPos.y())
            self.bottomRight.move(self.bottomRightPos)
            self.topLeft.move(self.topLeftPos)
            self.boxField.moveCenter(QPoint(self.topLeftPos.x()+10, self.topLeftPos.y()+10))
            self.sizeX = self.sizeX - offsetX
            self.sizeY = self.sizeY + offsetY
            self.boxField.setSize(QSize(self.sizeX,self.sizeY))

        elif(obj is self.bottomRight):
            self.bottomRightPos = pos
            self.topRightPos = QPoint(self.topRightPos.x()+offsetX, self.topRightPos.y())
            self.bottomLeftPos = QPoint(self.bottomLeftPos.x(), self.bottomLeftPos.y()+offsetY)
            self.topRight.move(self.topRightPos)
            self.bottomLeft.move(self.bottomLeftPos)
            self.sizeX = self.sizeX + offsetX
            self.sizeY = self.sizeY + offsetY
            self.boxField.setSize(QSize(self.sizeX,self.sizeY))


        else:
            print("actionDragFin Error")
        obj.show()
        self.cancel.move(QPoint(self.topRightPos.x(), self.topRightPos.y()))


    def saveInitialPosition(self, event, obj):
        #Correct position is Box position + event pos
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
        self.movingPosition = self.initialPosition

    def __del__(self):
        print("deleted\n")
        self.topLeft.deleteLater()
        self.topRight.deleteLater()
        self.bottomLeft.deleteLater()
        self.bottomRight.deleteLater()
        del self.boxField
        self.cancel.deleteLater()
        self.parent.boxFields[self.index] = None
