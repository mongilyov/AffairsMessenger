from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor

class MDS__PartnerWidget(QWidget):
    def __init__ (self, id: int, name: str, parent = None):
        super().__init__(parent)
        self.id = id
        self.text = QLabel(name)
        self.text.setObjectName("partnerName")
        
        self.unreadCount = 0
        self.unreadCountText = QLabel(str(self.unreadCount))
        self.unreadCountText.setObjectName("unreadCounter")
        self.flag = False

        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.text, 
                              alignment=Qt.AlignmentFlag.AlignLeft |
                              Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.unreadCountText, 
                              alignment=Qt.AlignmentFlag.AlignRight)
        self.unreadCountText.hide()
        self.setLayout(self.layout)
    
    def increaseUnreadCount(self, i: int = 1):
        self.unreadCount += i
        self.unreadCountText.setText(str(self.unreadCount))
        self.unreadCountText.show()

    def decreaseUnreadCount(self, i: int = 1):
        if self.unreadCount - i < 0:
            return
        self.unreadCount -= i
        if not self.unreadCount:
            self.unreadCountText.hide()
            return
        self.unreadCountText.setText(str(self.unreadCount))
        