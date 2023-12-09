from PyQt6 import QtGui
from PyQt6.QtWidgets import QLineEdit, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QRect, pyqtSlot, QMargins

class MDS__LineEdit(QLineEdit):
    def __init__(self,
                 width = 300,
                 height = 50,
                 backgroundColor = "#272727",
                 focusColor = "#272727",
                 textColor = "snow",
                 mode = "normal",
                 radius = 30,
                 parent = None):
        super().__init__(parent)
        self.setMinimumSize(width, height)

        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

        self.__width = width
        self.__height = height
        self.__backgroundColor = backgroundColor
        self.__focusColor = focusColor
        self.__colorToPaint = self.__backgroundColor
        self.__textColor = textColor
        self.__radius = radius
        self.__mode = 1 if mode == "password" else 0

    def paintEvent(self, a0) -> None:

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(self.__colorToPaint))
        rect = QRect(0, 0, self.__width, self.__height)
        p.drawRoundedRect(rect, self.__radius, self.__radius)
        pen = QPen(QColor(self.__textColor), 100)
        p.setFont(QFont('American Typewriter', 20))
        p.setPen(pen)
        rect = rect.marginsAdded(QMargins(-15, 0, 0, 0))
        if self.__mode:
            text = len(self.text()) * '✧'
            p.drawText(rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, 
                        text)
        else:
            p.drawText(rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                        self.text())

        p.end();

    def focusInEvent(self, a0) -> None:
        self.__colorToPaint = self.__focusColor
        self.update()

    def focusOutEvent(self, a0) -> None:
        self.__colorToPaint = self.__backgroundColor
        self.update()
        