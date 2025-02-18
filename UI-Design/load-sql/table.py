import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication
import sqlite3

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("table.ui", self)
        self.tableWidget.setColumnWidth(0,200)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,350)
        self.tableWidget.setHorizontalHeaderLabels(["City", "Country", "SubCountry"])
        self.load_data()

    # function to load all the Data
    # Note: this could be dangerous for two reasons:
        # 1. If the file is too big, it will take a long time to load
        # 2. User input could be corrupted
    def load_data(self):
        connection = sqlite3.connect("data.sqlite")
        cursor = connection.cursor()
        sqlquer = "SELECT * FROM worldcities LIMIT 50"

        # Hide row numbers
        self.tableWidget.verticalHeader().setVisible(False)
        # self.tableWidget.setRowCount(0)
        # with open('data.txt') as f:
        #     for row_number, line in enumerate(f):
        #         self.tableWidget.insertRow(row_number)
        #         for column_number, cell in enumerate(line.split('\t')):
        #             self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(cell))
        # self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

# main
app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1120)
widget.setFixedHeight(850)
widget.show()
try:
    sys.exit(app.exec())
except:
    print("Exiting")
