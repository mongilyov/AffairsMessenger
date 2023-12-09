from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QKeyEvent

class MDS__TextEdit(QPlainTextEdit):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.document().contentsChanged.connect(self.sizeChange)
        self.signalToSend = parent.sendMessageViaTextEdit

        self.heightMin = 0
        self.heightMax = 500

    def sizeChange(self):
        docHeight = int(self.document().size().height())
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight)
    
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_Return:
            self.signalToSend.emit()
            return
        return super().keyPressEvent(e)