import os
import sys
import argparse
import mysql.connector
from datetime import datetime

# Python bindings for Qt
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QPieSeries, QBarSet, QBarSeries
from PyQt6.QtCore import Qt, QPointF, QTimer
from PyQt6.QtGui import QPainter

# Icon library
import qtawesome  #load last to avoid using PyQt5 and breaking icons

from database_utilites import execute_query, execute_insert_query

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi('Management-UI.ui', self)

        # Set window icon
        managementSet = "fa5s.user-tie"
        managementIcon = qtawesome.icon(managementSet, color="#404258")
        app.setWindowIcon(managementIcon)

        ############################################################################################################
        # ICON SETUP
        # Setting up icons for each button (couldn't find another way to show icons but with buttons)
        self.sign_off_button.setIcon(qtawesome.icon('fa5s.sign-out-alt', color='orange'))
        self.left_menu_button.setIcon(qtawesome.icon('fa5s.sign-in-alt', color='orange', hflip=True))
        self.pushButton_7.setIcon(qtawesome.icon(managementSet, color='orange'))
        self.pushButton_7.setIconSize(QtCore.QSize(32, 32))  # Rezise the icon to 32x32

        self.dashboard_pushButton.setIcon(qtawesome.icon('mdi.monitor-dashboard', color='orange'))
        self.cost_pushButton.setIcon(qtawesome.icon('fa5s.money-bill', color='orange'))
        self.work_orders_pushButton.setIcon(qtawesome.icon('ri.list-unordered', color='orange'))
        self.inventory_pushButton.setIcon(qtawesome.icon('mdi.warehouse', color='orange'))
        self.work_orders_pushButton.setIcon(qtawesome.icon('fa.bar-chart-o', color='orange'))
        self.charts_pushButton.setIcon(qtawesome.icon('mdi6.chart-areaspline', color='orange'))

        # set right_menu_widget as hidden when starting the application
        self.right_menu_widget.setHidden(True)

        ############################################################################################################
        # BUTTON CONNECTIONS
        self.set_1_count.mousePressEvent = lambda event: self.open_sign_off_panel(self.set_1_count, self.jcn_num_1)
        self.set_2_count.mousePressEvent = lambda event: self.open_sign_off_panel(self.set_2_count, self.jcn_num_2)
        self.set_3_count.mousePressEvent = lambda event: self.open_sign_off_panel(self.set_3_count, self.jcn_num_3)
        self.set_4_count.mousePressEvent = lambda event: self.open_sign_off_panel(self.set_4_count, self.jcn_num_4)
        self.set_5_count.mousePressEvent = lambda event: self.open_sign_off_panel(self.set_5_count, self.jcn_num_5)

        self.left_menu_button.clicked.connect(lambda: self.left_menu_widget.setHidden(not self.left_menu_widget.isHidden()))

        ### These buttons need to be updated so the can call for data again to refresh the tables.
        self.dashboard_pushButton.clicked.connect(lambda: self.switch_page(self.dashboard_view, "DASHBOARD"))
        self.cost_pushButton.clicked.connect(lambda: self.switch_page(self.cost_view, "COST"))
        self.work_orders_pushButton.clicked.connect(lambda: self.switch_page(self.work_orders_view, "WORK ORDERS"))
        self.inventory_pushButton.clicked.connect(lambda: self.switch_page(self.inventory_view, "INVENTORY"))
        self.charts_pushButton.clicked.connect(lambda: self.switch_page(self.charts_view, "CHARTS"))

        ############################################################################################################
        # TABLE SETUP / TAB SETUP
        self.dashboard_bar_chart()
        self.set_awaiting_approval()
        self.load_table_data()
        self.load_work_order_data()
        self.load_inventory_data()
        self.load_charts_data()

        self.set_priority_counts()
    
    ############################################################################################################
    # Helper Function
    def switch_page(self, widget, title):
        self.stackedWidget.setCurrentWidget(widget)
        self.title_label.setText(title)

    def resizeEvent(self, event):
        if event:
            event.accept()
        if hasattr(self, 'dashBoardChartView'):
            self.dashBoardChartView.resize(self.dashboard_frame_left.size())
            self.dashBoardChartView.show()
            
        if hasattr(self, 'topChartview'):
            self.topChartview.resize(self.chart_top.size())
            self.topChartview.show()
            
        if hasattr(self, 'bottomChartview'):
            self.bottomChartview.resize(self.chart_bottom.size())
            self.bottomChartview.show()
            
        super().resizeEvent(event)

    def open_sign_off_panel(self, label, jcn_num):
        if label.text() != "...":
            self.right_menu_widget.setHidden(not self.right_menu_widget.isHidden())
            parser = argparse.ArgumentParser()
            parser.add_argument('--user_id', type=int)
            args = parser.parse_args()
            sign_off_id = args.user_id
            
            def execute_and_hide():
                current_date = datetime.now().date().strftime('%Y-%m-%d')
                query = f"UPDATE workorders SET signed_off_id = {sign_off_id}, sign_off_date = '{current_date}' WHERE creation_reason = '{label.text()}' AND jcn = '{jcn_num.text()}' AND {sign_off_id} IN (SELECT user_id FROM users)"
                execute_insert_query(query)

                # update the set count table
                self.set_awaiting_approval()

                self.right_menu_widget.setHidden(not self.right_menu_widget.isHidden())

            self.sign_off_button.clicked.connect(execute_and_hide)

    def create_bar_set(self, label, value):
        barSet = QBarSet(label)
        barSet.append(value)
        return barSet

    ############################################################################################################
    # DASHBOARD FUNCTIONS
    def dashboard_bar_chart(self):

        dashQuery = "CALL GetWorkOrderCountPerDay()"

        try:
            work_order_count_per_day = execute_query(dashQuery)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not work_order_count_per_day:
            return

        dashBoardBarSeries = QBarSeries(self)

        for x, y in enumerate(work_order_count_per_day):
            barSet = QBarSet(str(x))
            barSet.append(y[1])
            dashBoardBarSeries.append(barSet)

        dashBoardChart = QChart()
        dashBoardChart.addSeries(dashBoardBarSeries)
        dashBoardChart.createDefaultAxes()

        self.dashBoardChartView = QChartView()
        self.dashBoardChartView.setChart(dashBoardChart)
        self.dashBoardChartView.setRenderHint(QPainter.Antialiasing)

        self.dashBoardChartView.setParent(self.dashboard_frame_left)
        self.dashBoardChartView.resize(self.dashboard_frame_left.size())
        self.dashBoardChartView.show()

    def set_priority_counts(self):
        query = "SELECT priority, COUNT(*) FROM workorders GROUP BY priority"

        try:
            result = execute_query(query)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not result:
            print("The query is empty.")

        # Store the counts
        priority_totals = {}
        for priority_count in result:
            priority = priority_count[0]
            count = priority_count[1]
            priority_totals[priority] = count

        self.pri_1_count.setText(str(priority_totals[1]))
        self.pri_2_count.setText(str(priority_totals[2]))
        self.pri_3_count.setText(str(priority_totals[3]))

    def set_awaiting_approval(self):
        query = "SELECT creation_reason, jcn FROM flight_simulator_db.workorders WHERE signed_off_id IS NULL OR signed_off_id = '' ORDER BY creation_date DESC LIMIT 5"
        
        try:
            result = execute_query(query)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not result:
            print("The query is empty.")

        # clear all the fields first
        for i in range(1, 6):
            set_0 = f"set_{i}_count"
            set_1 = f"jcn_num_{i}"
            txt_label = getattr(self, set_0, None)
            jcn_label = getattr(self, set_1, None)
            if txt_label is not None:
                txt_label.setText("...")
                jcn_label.setText("...")

        # Update the label with text from result or with an qta icon
        for i, set in enumerate(result):
            work_order = set[0]
            jcn = set[1]
            set_0 = f"set_{i+1}_count"
            set_1 = f"jcn_num_{i+1}"
            txt_label = getattr(self, set_0, None)
            jcn_label = getattr(self, set_1, None)
            if txt_label is not None:
                txt_label.setText(str(work_order))
                jcn_label.setText(str(jcn))
           
    ############################################################################################################
    # LOAD TABLE DATA
    def load_table_data(self):
        #########################
        ## UPPER TABLE
        query = "CALL GetTechSummary()"

        try:
            tech_cost_data = execute_query(query)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not tech_cost_data:
            print("The query is empty.")

        # print(tech_cost_data)

        # set the number of rows
        self.cost_upper_table.setRowCount(len(tech_cost_data))
        # hide row numbers
        self.cost_upper_table.verticalHeader().setVisible(False)

        # push data into the table
        for i, record in enumerate(tech_cost_data):
            self.cost_upper_table.setItem(i, 0, QtWidgets.QTableWidgetItem(record[0]))      # tech name
            self.cost_upper_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(record[1]))) # total cost
            self.cost_upper_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(record[1]))) # total hours

        #########################
        ## LOWER TABLE

        try:
            parts_data = execute_query("CALL ShowPartsData()")
        except Exception as e:
            print("Error with query: ", e)
            return
        if not parts_data:
            print("The query is empty.")

        # set the number of rows
        self.cost_lower_table.setRowCount(len(parts_data))
        # hide row numbers
        self.cost_lower_table.verticalHeader().setVisible(False)
        # push data into the table
        for i, record in enumerate(parts_data):
            self.cost_lower_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(record[0])))  # item name
            self.cost_lower_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(record[1])))  # cost per item
            self.cost_lower_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(record[2])))  # due date
            self.cost_lower_table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(record[3])))  # priority

    def load_work_order_data(self):
        # Execute the query to fetch the data
        query = "SELECT jcn, creation_reason, reported_by_name, priority, notes FROM workorders"

        try:
            # Fetch all the rows returned by the query
            work_order_data = execute_query(query)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not work_order_data:
            print("The query is empty.")

        # set the number of rows
        self.work_order_table.setRowCount(len(work_order_data))
        # hide row numbers
        self.work_order_table.verticalHeader().setVisible(False)
        # set column widths
        self.work_order_table.setColumnWidth(0, 100) # JCN
        self.work_order_table.setColumnWidth(1, 200) # Reason
        self.work_order_table.setColumnWidth(2, 100) # User
        self.work_order_table.setColumnWidth(3, 100) # Priority
        # resize "Notes" column to fill remaining space
        self.work_order_table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        # push data into the table
        row_index = 0  # Initialize the row index
        # push data into the table
        for work_order in work_order_data:
            self.work_order_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(work_order[0])))  # jcn
            self.work_order_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(work_order[1]))  # creation_reason
            self.work_order_table.setItem(row_index, 2, QtWidgets.QTableWidgetItem(work_order[2]))  # reported_by_name
            
            # Center the priority number
            priority_item = QtWidgets.QTableWidgetItem(str(work_order[3]))  # priority
            priority_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the content
            self.work_order_table.setItem(row_index, 3, priority_item)
            
            self.work_order_table.setItem(row_index, 4, QtWidgets.QTableWidgetItem(work_order[4]))  # notes
            row_index += 1  # Increment the row index

        # if the priority is 1, set the background color of that priority cell to red
        for row in range(self.work_order_table.rowCount()):
            priority_item = self.work_order_table.item(row, 3)
            priority = priority_item.text()
            if priority == "1":
                priority_item.setBackground(QtGui.QColor(255, 0, 0))  # Red background
                priority_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # White text color
            elif priority == "2":
                priority_item.setBackground(QtGui.QColor(255, 255, 0))  # Yellow background
                priority_item.setForeground(QtGui.QBrush(QtGui.QColor(0, 0, 0)))  # Black text color
            elif priority == "3":
                priority_item.setBackground(QtGui.QColor(0, 255, 0))  # Green background
                priority_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # White text color

    def load_inventory_data(self):
        # Execute the query to fetch the data
        query = "CALL GetInventoryData()"
        inventory_data = execute_query(query)

        # set the number of rows
        self.inventory_table.setRowCount(len(inventory_data))
        # hide row numbers
        self.inventory_table.verticalHeader().setVisible(False)
        # set all column widths evenly between all columns
        for column in range(self.inventory_table.columnCount()):
            self.inventory_table.setColumnWidth(column, 100)

        # push data into the table
        for i, inventory in enumerate(inventory_data):
            self.inventory_table.setItem(i, 0, QtWidgets.QTableWidgetItem(inventory[1]))  # item_name
            self.inventory_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(inventory[0])))  # stock_on_hand
            self.inventory_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(inventory[2])))  # minimum_stock_number
            self.inventory_table.setItem(i, 3, QtWidgets.QTableWidgetItem(inventory[3]))  # stock_location
            self.inventory_table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(inventory[4])))  # cost_per_item
            self.inventory_table.setItem(i, 5, QtWidgets.QTableWidgetItem(inventory[5]))  # username

        # if the inventory amount is less than the minimum stock, set the background color of that cell to light red
        for row in range(self.inventory_table.rowCount()):
            stock_on_hand_item = self.inventory_table.item(row, 1)
            stock_on_hand = stock_on_hand_item.text()
            minimum_stock_number_item = self.inventory_table.item(row, 2)
            minimum_stock_number = minimum_stock_number_item.text()
            if int(stock_on_hand) < int(minimum_stock_number):
                stock_on_hand_item.setBackground(QtGui.QColor(255, 0, 0))
                minimum_stock_number_item.setBackground(QtGui.QColor(255, 0, 0))

    #############################################################################################################
    # LOAD CHARTS DATA     
    def load_charts_data(self):
        # Call DB stored procedure GetWorkOrderCountPerDay() to get the last 7 days of data
        topQuery = "CALL GetWorkOrderCountPerDay()"

        try:
            work_order_count_per_day_data = execute_query(topQuery)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not work_order_count_per_day_data:
            print("The query is empty.")

        # Send data to the QLineSeries chart
        topSeries = QLineSeries(self)

        for x, y in enumerate(work_order_count_per_day_data):
            point = QPointF(x, y[1])
            topSeries.append(point)

        topChart = QChart()
        topChart.addSeries(topSeries)
        topChart.createDefaultAxes()

        self.topChartview = QChartView()
        self.topChartview.setChart(topChart)
        self.topChartview.setRenderHint(QPainter.Antialiasing)

        self.topChartview.setParent(self.chart_top)
        self.topChartview.resize(self.chart_top.size())
        self.topChartview.show()

        ## Bottom chart
        bottomQuery = "CALL GetHoursWorkedPerPerson()"

        try:
            hours_worked_per_person_data = execute_query(bottomQuery)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not hours_worked_per_person_data:
            print("The query is empty.")


        bottomSeries = QPieSeries()
        for row in hours_worked_per_person_data:
            username = row[0]
            total_hours = row[1]
            bottomSeries.append(username, total_hours)

        bottomChart = QChart()
        bottomChart.addSeries(bottomSeries)
        bottomChart.setTitle("Work load by shift")

        self.bottomChartview = QChartView()
        self.bottomChartview.setChart(bottomChart)
        self.bottomChartview.setRenderHint(QPainter.Antialiasing)

        self.bottomChartview.setParent(self.chart_bottom)
        self.bottomChartview.resize(self.chart_bottom.size())
        self.bottomChartview.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
