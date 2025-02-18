from PyQt6 import QtWidgets, uic, QtCore
import qtawesome as qta
import sys

# Python QT Charts
# https://www.youtube.com/watch?v=20ed0Ytkxuw&list=PLJ8t3BKaQLhPltjWNb0QApviqiXSqHeb6
import os
# import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

import random

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi('interface.ui', self)

        # Set the icon for your QPushButton
        # ri.pie-chart-line     # QT Charts
        ## mdi.equalizer         # percent
        ## ri.temp-hot-fill      # temperature
        ## mdi.bullseye          # Nested Donut Chart
        ## fa.code-fork          # Line Chart
        ## fa.bar-chart-o        # Bar Chart
        ## fa5.smile-wink        # Support
        # mdi6.patreon          # Patreon
        # mdi6.youtube-studio   # Youtube
        # fa.paypal             # Paypal
        # fa5.window-restore    # Maximize
        # mdi.close-thick     # Close

        # set self.pushButton_6 and resize it to 32x32
        self.pushButton_6.setIcon(qta.icon('ri.align-center', color='orange'))
        self.pushButton_6.setIconSize(QtCore.QSize(32, 32))  # Rezise the icon to 32x32


        # self.pushButton_6.setIcon(qta.icon('ri.align-center', color='orange'))

        self.min_btn.setIcon(qta.icon('fa5.window-minimize', color='orange'))
        self.max_btn.setIcon(qta.icon('fa5.window-restore', color='orange'))
        self.close_btn.setIcon(qta.icon('mdi.close-thick', color='orange'))

        self.pushButton_7.setIcon(qta.icon('ri.pie-chart-line', color='orange'))
        self.pushButton_7.setIconSize(QtCore.QSize(32, 32))  # Rezise the icon to 32x32
        # self.frame_3.setIcon(qta.icon('ri.pie-chart-line', color='orange'))
        self.pushButton.setIcon(qta.icon('mdi.equalizer', color='orange'))
        self.pushButton_5.setIcon(qta.icon('ri.temp-hot-fill', color='orange'))
        self.pushButton_2.setIcon(qta.icon('mdi.bullseye', color='orange'))
        self.pushButton_3.setIcon(qta.icon('fa.code-fork', color='orange'))
        self.pushButton_4.setIcon(qta.icon('fa.bar-chart-o', color='orange'))


        self.pushButton_8.setIcon(qta.icon('fa5.smile-wink', color='orange'))
        self.pushButton_8.setIconSize(QtCore.QSize(32, 32))  # Change the numbers to your desired width and height

        # pixmap = qta.icon('mdi6.patreon', color='orange').pixmap(32, 32)
        # pixmap = pat_icon.pixmap(32, 32)
        self.pat_label.setPixmap(qta.icon('mdi6.patreon', color='orange').pixmap(32, 32))
        self.you_label.setPixmap(qta.icon('mdi6.youtube-studio', color='orange').pixmap(32, 32))
        self.pay_label.setPixmap(qta.icon('fa.paypal', color='orange').pixmap(32, 32))

        self.display_sample_bar_chart()
        # self.pushButton.clicked.connect(self.display_bar_chart)
        # self.frame_16.setStyleSheet("background-color: red;")

        # print(self.stackedWidget.currentIndex()) # show the frame number
        # print(self.stackedWidget.currentWidget()) # show the widget

    def resizeEvent(self, event):
        # print("frame_16 size:", self.size())  # Print the size of frame_16
        self.canvas.setGeometry(self.frame_16.rect())
        event.accept()

    def display_sample_bar_chart(self):
        # Generate sample data for the bar chart
        self.labels = ['A', 'B', 'C', 'D', 'E']
        self.data = [10, 5, 8, 12, 3]

        # Create a figure and axis for the bar chart
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        # Set the positions of the bars on the x-axis
        self.x = np.arange(len(self.labels))

        # Plot the bar chart
        self.ax.bar(self.x, self.data)

        # Set labels and title
        self.ax.set_xlabel('Categories')
        self.ax.set_ylabel('Values')
        self.ax.set_title('Sample Bar Chart')

        # Create a FigureCanvas widget for the plot
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.frame_16)
        self.canvas.setGeometry(self.rect())

        # # Create a QVBoxLayout for frame_16
        # layout = QtWidgets.QVBoxLayout(self.frame_16)
        # layout.addWidget(self.canvas)

        # # Set the QVBoxLayout as the layout for frame_16
        # self.frame_16.setLayout(layout)

        # # Set a tight layout for the frame
        # layout.setContentsMargins(0, 0, 0, 0)  # Set layout margins to zero
        # layout.setSpacing(0)  # Set spacing between widgets to zero
        # layout.addStretch(1)  # Add a stretchable space at the end of the layout

        # Show the canvas and redraw
        self.canvas.setVisible(True)
        self.canvas.draw()








if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
