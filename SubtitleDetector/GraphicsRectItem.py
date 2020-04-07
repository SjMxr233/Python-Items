from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GraphicsRectItem(QGraphicsRectItem):

    handleSpace = -5.0
    handleSize = QPointF(10,10)
    minSize = 25

    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleCursors = {
        handleTopLeft: Qt.SizeFDiagCursor,
        handleTopMiddle: Qt.SizeVerCursor,
        handleTopRight: Qt.SizeBDiagCursor,
        handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor,
        handleBottomLeft: Qt.SizeBDiagCursor,
        handleBottomMiddle: Qt.SizeVerCursor,
        handleBottomRight: Qt.SizeFDiagCursor,
    }

    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.lastmousePos =None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, False)
        self.updateHandlesPos()
    
    def setHH(self,hh,factor):
        self.hh = hh
        self.factor = factor

    def setClip(self,clip):
        self.clip = clip


    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """

        self.handleSelected = self.handleAt(mouseEvent.pos())
        self.mousePressPos = mouseEvent.pos()
        self.lastmousePos = self.mousePressPos
        if self.handleSelected:
            self.mousePressRect = self.boundingRect()

        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            self.Limit(mouseEvent.pos())
        lt,rb = self.getCropBox()
        w =int(rb.x()*self.factor-lt.x()*self.factor)
        h =int(rb.y()*self.factor-lt.y()*self.factor)
        self.clip.setText(str(w)+'X'+str(h))

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.lastmousePos =None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        ox = self.handleSize.x() + self.handleSpace
        oy = self.handleSize.y() + self.handleSpace
        return self.rect().adjusted(-ox, -ox, oy, oy)

    def Limit(self,mousePos):

        toX = mousePos.x() - self.lastmousePos.x()
        toY = mousePos.y() - self.lastmousePos.y()
        diff = QPointF(toX,toY)
        self.lastmousePos = mousePos
        rect = self.rect()

        leftTop = self.handles[self.handleTopLeft].center()
        rightBottom = self.handles[self.handleBottomRight].center()

        if leftTop.x() + toX > 0 and rightBottom.x()+ toX <320:
            rect.setLeft(rect.left() + diff.x())
            rect.setRight(rect.right() + diff.x())

        offsetY = (240-self.hh)/2
        if leftTop.y() + toY > offsetY and rightBottom.y()+ toY <self.hh+offsetY:
            rect.setTop(rect.top() + diff.y())
            rect.setBottom(rect.bottom() + diff.y())

        self.setRect(rect)
        self.updateHandlesPos()






    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        sx = self.handleSize.x()
        sy = self.handleSize.y()
        b = self.boundingRect()
        disX = self.rect().width()/20
        disY = self.rect().height()/20
        self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), sx, sy)
        self.handles[self.handleTopMiddle] = QRectF(b.center().x() - sx *disX/ 2, b.top(), sx*disX, sy)
        self.handles[self.handleTopRight] = QRectF(b.right() - sx, b.top(), sx, sy)
        self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - sy*disY / 2, sx, sy*disY)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - sx, b.center().y() - sy*disY / 2, sx, sy*disY)
        self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - sy, sx, sy)
        self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - sx*disX / 2, b.bottom() - sy, sx*disX, sy)
        self.handles[self.handleBottomRight] = QRectF(b.right() - sx, b.bottom() - sy, sx, sy)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        handleOffsetX = self.handleSize.x() + self.handleSpace
        handleOffsetY = self.handleSize.y() + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)
        offsetY = (240 - self.hh) / 2
        self.prepareGeometryChange()
        if self.handleSelected == self.handleTopLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + handleOffsetX)
            rect.setTop(boundingRect.top() + handleOffsetY)
            if rect.top() < offsetY:
                rect.setTop(offsetY)
            if rect.left() < 0:
                rect.setLeft(0)
            if rect.right() - rect.left() < self.minSize:
                rect.setLeft(rect.right() - self.minSize)
            if rect.bottom() - rect.top() < self.minSize:
                rect.setTop(rect.bottom() - self.minSize)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - handleOffsetX)
            rect.setTop(boundingRect.top() + handleOffsetY)
            if rect.top() < offsetY:
                rect.setTop(offsetY)
            if rect.right() > 320:
                rect.setRight(320)
            if rect.right() - rect.left() < self.minSize:
                rect.setRight(rect.left() + self.minSize)
            if rect.bottom() - rect.top() < self.minSize:
                rect.setTop(rect.bottom() - self.minSize)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + handleOffsetY)
            if rect.top() < offsetY:
                rect.setTop(offsetY)
            if rect.bottom() - rect.top() < self.minSize:
                rect.setTop(rect.bottom() - self.minSize)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + handleOffsetX)
            if rect.left() < 0:
                rect.setLeft(0)
            if rect.right() - rect.left() < self.minSize:
                rect.setLeft(rect.right()-self.minSize)
            self.setRect(rect)


        elif self.handleSelected == self.handleMiddleRight:
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - handleOffsetX)
            if rect.right() > 320:
                rect.setRight(320)
            if rect.width() < self.minSize:
                rect.setWidth(self.minSize)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - handleOffsetY)
            if rect.bottom() > self.hh + offsetY:
                rect.setBottom(self.hh + offsetY)
            if rect.height() < self.minSize:
                rect.setHeight(self.minSize)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + handleOffsetX)
            rect.setBottom(boundingRect.bottom() - handleOffsetY)
            if rect.left() < 0:
                rect.setLeft(0)
            if rect.bottom() > self.hh + offsetY:
                rect.setBottom(self.hh + offsetY)
            if rect.right() - rect.left() < self.minSize:
                rect.setLeft(rect.right() - self.minSize)
            if rect.bottom() - rect.top() < self.minSize:
                rect.setBottom(rect.top() + self.minSize)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - handleOffsetX)
            rect.setBottom(boundingRect.bottom() - handleOffsetY)
            if rect.right() > 320:
                rect.setRight(320)
            if rect.bottom() > self.hh+offsetY:
                rect.setBottom(self.hh +offsetY)
            if rect.width() < self.minSize:
                rect.setWidth(self.minSize)
            if rect.height() < self.minSize:
                rect.setHeight(self.minSize)
            self.setRect(rect)

        self.updateHandlesPos()

    def getCropBox(self):
        leftTop = self.handles[self.handleTopLeft].center()
        rightBottom = self.handles[self.handleBottomRight].center()
        return leftTop,rightBottom

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(255, 255, 255), 2.0, Qt.DashLine))
        painter.drawRect(self.rect())

