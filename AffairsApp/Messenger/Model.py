from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QListWidgetItem

from PyToggles.MDS__PartnerWidget import MDS__PartnerWidget
from PyToggles.MDS__MessageWidget import MDS__MessageWidget

class Model:
    def __init__(self, protocol, catalogue, mD):
        self.selectedUser = None
        self.idToMessages = {}
        self.idToWidgetInCatalogue = {}
        self.nameToId = {}
        self.__protocol = protocol
        self.__messageDisplay = mD
        self.__catalogue = catalogue
        self.__catalogue.itemClicked.connect(self.catalogueClicked)

        self.__protocol.getUsersForFill()

    def catalogueClicked(self, item):
        id = self.__catalogue.itemWidget(item).id
        if self.selectedUser == id:
            return
        self.selectedUser = id
        if self.selectedUser in self.idToMessages:
            self.showExistingMessages()
            return
        self.__protocol.getMessages(id)

    def fillCatalogue(self, l: list):
        self.__catalogue.clear()
        for elem in l:
            partner = MDS__PartnerWidget(elem["id"], elem["name"])
            item = QListWidgetItem()
            item.setSizeHint(partner.sizeHint())
            self.__catalogue.addItem(item)
            self.__catalogue.setItemWidget(item, partner)
            self.idToWidgetInCatalogue[elem["id"]] = item
            self.nameToId[elem["name"]] = elem["id"]

    def addNewToCatalogue(self, msg: dict, select: bool = True):
        partner = MDS__PartnerWidget(msg["id"], msg["name"])
        item = QListWidgetItem()
        item.setSizeHint(partner.sizeHint())
        self.__catalogue.insertItem(0, item)
        self.__catalogue.setItemWidget(item, partner)
        self.idToWidgetInCatalogue[msg["id"]] = item
        if select:
            self.selectedUser = msg["id"]
            self.__catalogue.setCurrentItem(item)
            self.__messageDisplay.clear()

    def fillMessagesDisplay(self, l: list):
        self.__messageDisplay.clear()
        listForUpdatingData = []
        for message in l:
            partner = MDS__MessageWidget(message["messageId"],
                                          message["message"], 
                                          message["isSelf"])
            item = QListWidgetItem(self.__messageDisplay)
            item.setSizeHint(partner.sizeHint())
            self.__messageDisplay.addItem(item)
            self.__messageDisplay.setItemWidget(item, partner)
            self.__messageDisplay.scrollToItem(item)
            if not message["isSelf"] and not message["isRead"]:
                listForUpdatingData.append({"messageId": message["messageId"]})
            message["isRead"] = 1

        self.idToMessages[self.selectedUser] = l

        if len(listForUpdatingData):
            self.markAsReaded(listForUpdatingData)
    
    def showExistingMessages(self):
        self.__messageDisplay.clear()
        for message in self.idToMessages[self.selectedUser]:
            partner = MDS__MessageWidget(message["messageId"],
                                          message["message"], 
                                          message["isSelf"])
            item = QListWidgetItem(self.__messageDisplay)
            item.setSizeHint(partner.sizeHint())
            self.__messageDisplay.addItem(item)
            self.__messageDisplay.setItemWidget(item, partner)
            self.__messageDisplay.scrollToItem(item)

        self.getNewMessagesFromUser()

    def getNewMessagesFromUser(self):
        self.__protocol.getOnlyUnreadMessages(self.selectedUser)

    def addNewMessagesToUser(self, l: list):
        if self.selectedUser not in self.idToMessages:
            self.idToMessages[self.selectedUser] = []
        self.idToMessages[self.selectedUser].extend(l) # fix isRead
        listForUpdatingData = []
        for message in l:
            partner = MDS__MessageWidget(message["messageId"],
                                          message["message"], 
                                          message["isSelf"])
            item = QListWidgetItem(self.__messageDisplay)
            item.setSizeHint(partner.sizeHint())
            self.__messageDisplay.addItem(item)
            self.__messageDisplay.setItemWidget(item, partner)
            self.__messageDisplay.scrollToItem(item)
            if not message["isSelf"]:
                listForUpdatingData.append({"messageId": message["messageId"]})

        if len(listForUpdatingData):
            self.markAsReaded(listForUpdatingData)

    def markAsReaded(self, l: list):
        self.__catalogue.itemWidget(
            self.idToWidgetInCatalogue[self.selectedUser]).decreaseUnreadCount(len(l))
        self.__protocol.markAsReaded(l)

    def dealWithMessage(self, text: str): # send and add to list of messsages
        self.__protocol.sendMessage(self.selectedUser, text)
    
    def dealWithNotification(self, idFrom: int):
        if idFrom not in self.idToWidgetInCatalogue:
            self.addNewToCatalogue({"id": idFrom, "name": ''}, select = False)
            self.__protocol.getNameForNewUser(idFrom)
        self.__catalogue.itemWidget(
            self.idToWidgetInCatalogue[idFrom]).increaseUnreadCount()
        if self.selectedUser == idFrom:
            self.getNewMessagesFromUser()

    def nameUserInCatalogue(self, msg: dict):
        self.__catalogue.itemWidget(
            self.idToWidgetInCatalogue[msg["id"]]).text.setText(msg["name"])
        self.nameToId[msg["name"]] = msg["id"]

    def dealWithNewUser(self, username: str):
        if username in self.nameToId:
            self.selectedUser = self.nameToId[username]
            if self.selectedUser in self.idToMessages:
                self.showExistingMessages()
            else:
                self.__protocol.getMessages(self.selectedUser)
            return
        self.__protocol.newUser(username)
