from PyQt6.QtWidgets import QWidget, QApplication, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
import sys

# sample database
tasks = ["Write email", "Finish Feature", "Watch tutorial"]

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("Schedular.ui", self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.updateTaskList()


    def calendarDateChanged(self):
        dateSelected = self.calendarWidget.selectedDate().toPyDate()#.strftime("%d/%m/%Y")
        print(dateSelected)


    def updateTaskList(self):
        for task in tasks:
            # item = 
            item = QListWidgetItem(task)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.tasksListWidget.addItem(item)


if __name__ == "__main__":  
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

