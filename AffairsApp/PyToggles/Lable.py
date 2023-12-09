from PyQt6.QtWidgets import QLabel

from PyQt6 import QtCore, QtGui

from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QRect, QPoint

class Label(QLabel):
    def __init__(self, text: str, parent = None):
        super().__init__(parent)
        self.setGeometry(0, 0, 100, 50)
        self.text = text

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        
        p.setPen(Qt.PenStyle.NoPen)
        rect = QRect(0, 0, 100, 50)
        p.setBrush(QColor('blue'))
        p.drawRect(rect)
        p.setPen(QPen(QColor('red')))
        p.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text)
        
        p.end();

    def enterEvent(self, event) -> None:
        print('enter')
    def leaveEvent(self, a0) -> None:
        print('leave')