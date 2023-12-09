import asyncio
import sys
from MainWindow import MainWindow
from Application import Application
from qasync import QEventLoop
from client import Client
from pathlib import Path

async def create_client(loop):
    return await loop.create_connection(
        lambda: Client(), '127.0.0.1', 8888
    )

app = Application(sys.argv)
app.setStyleSheet(Path('styles.qss').read_text())
app.setApplicationName('Affairs')
loop = QEventLoop(app)
asyncio.set_event_loop(loop)

mainWindow = MainWindow()
mainWindow.showMaximized()
mainWindow.show()

with loop:
    try:
        _, protocol = loop.run_until_complete(create_client(loop))
        mainWindow.setProtocol(protocol)
        loop.run_forever()
    except:
        print('Server is not online')
        