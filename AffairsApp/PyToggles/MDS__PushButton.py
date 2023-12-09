from PyQt6 import QtCore
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, QSize, QEasingCurve, QMargins, QPoint

class MDS__PushButton(QPushButton):
    def __init__(self, 
                 text='No text',
                 width=150,
                 height=100,
                 radius=10.,
                 bgColor="#191970",
                 textColor="snow",
                 hoverColor="", 
                 animationStyle = QEasingCurve.Type.OutExpo,
                 parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setMinimumSize(width, height)

        self.radius = radius
        self.buttonRect = QRect(0, 0, width, height)
        self.setGeometry(self.buttonRect)

        self.__bgColor = bgColor;
        self.__textColor = textColor
        self.__hoverColor = hoverColor
        self.__currentColor = bgColor

    def enterEvent(self, event):
        self.__currentColor = self.__hoverColor
        self.update()

        QPushButton.enterEvent(self, event)
    
    def leaveEvent(self, event) -> None:
        self.__currentColor = self.__bgColor
        self.update()

        QPushButton.leaveEvent(self, event)
        
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)

        p.setBrush(QColor(self.__currentColor))
        
        p.drawRoundedRect(self.buttonRect, self.radius, self.radius)

        pen = QPen(QColor(self.__textColor))
        p.setPen(pen)
        p.drawText(self.buttonRect, Qt.AlignmentFlag.AlignCenter, self.text())

        p.end();
