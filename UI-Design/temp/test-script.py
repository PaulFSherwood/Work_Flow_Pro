import sys
import qtawesome
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
#from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Click Me", self)
        icon = qtawesome.icon("fa5s.user", color="green")
        self.setWindowIcon(icon)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())
