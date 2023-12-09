from PyQt6 import QtGui
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPlainTextEdit
from PyQt6.QtCore import Qt, QRect, QMargins
from PyQt6.QtGui import QTextDocument

class MDS__MessageText(QPlainTextEdit):
    def __init__(self, text: str, parent = None):
        super().__init__(parent)
        self.setPlainText(text)
        self.setReadOnly(True)

    def heightForWidth(self, a0: int) -> int:
        return int(self.document().size().height()) + 15

class MDS__MessageWidget(QWidget):
    def __init__(self, messageId: int, text: str, isSelf = True, parent = None):
        super().__init__(parent)
        self.messageId = messageId
        self.text2 = MDS__MessageText(text)

        layout = QHBoxLayout(self)
        
        if isSelf:
            layout.addWidget(self.text2, alignment = Qt.AlignmentFlag.AlignRight)
        else:
            layout.addWidget(self.text2, alignment = Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)
