# WorkFlow Pro

import os
import sys
import mysql.connector
import datetime

# Python bindings for Qt
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QBarSet, QBarSeries, QDateTimeAxis, QValueAxis, QBarCategoryAxis, QBarSet
from PyQt6.QtCore import Qt, QPointF, QTimer, QDateTime
from PyQt6.QtGui import QPainter

# Icon library
import qtawesome # load last to avoid using PyQt5 and breaking icons

from utilities import decrypt_config
from database_utilites import execute_query, execute_insert_query


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi('Logistics-UI.ui', self)

        # Set window icon
        logisticsSet = "mdi.store-24-hour" # fa.wrench
        logisticsIcon = qtawesome.icon(logisticsSet, color="#404258")
        app.setWindowIcon(logisticsIcon)

        ############################################################################################################
        # ICON SETUP (qta-browser)
        # Setting up icons for each button (couldn't find another way to show icons but with buttons)
        self.left_menu_button.setIcon(qtawesome.icon('fa5s.sign-in-alt', color='orange', hflip=True))
        self.pushButton_7.setIcon(qtawesome.icon(logisticsSet, color='orange'))
        self.pushButton_7.setIconSize(QtCore.QSize(32, 32))  # Rezise the icon to 32x32

        self.dashboard_pushButton.setIcon(qtawesome.icon('mdi.monitor-dashboard', color='orange'))
        self.inventory_pushButton.setIcon(qtawesome.icon('mdi.warehouse', color='orange'))
        self.charts_pushButton.setIcon(qtawesome.icon('mdi6.chart-areaspline', color='orange'))
        self.addPart_pushButton.setIcon(qtawesome.icon('mdi6.file-document-edit-outline', color='orange'))

        ############################################################################################################
        # BUTTON CONNECTIONS (signals and slots)
        # show and hide the right_menu_widget when menu_button is clicked
        self.left_menu_button.clicked.connect(lambda: self.left_menu_widget.setHidden(not self.left_menu_widget.isHidden()))
        self.dashboard_pushButton.clicked.connect(lambda: self.switch_page(self.dashboard_view, "DASHBOARD"))
        self.inventory_pushButton.clicked.connect(lambda: self.switch_page(self.inventory_view, "INVENTORY"))
        self.charts_pushButton.clicked.connect(lambda: self.switch_page(self.charts_view, "CHARTS"))
        self.addPart_pushButton.clicked.connect(self.update_new_part_fields)

        ############################################################################################################
        # USER ACTION UPDATES
        self.inventory_table.cellClicked.connect(self.update_line_edits)  
        self.addPart_pushButton_2.clicked.connect(self.add_new_part)      

        ############################################################################################################
        # TABLE SETUP / TAB SETUP
        self.dashboard_bar_chart()
        self.set_newest_jcns()
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
    
    ############################################################################################################
    # DASHBOARD FUNCTIONS
    def dashboard_bar_chart(self):
        dashQuery = "CALL ShowPartsData()"
        
        try:
            work_order_count_per_day = execute_query(dashQuery)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not work_order_count_per_day:
            print("The query is empty.")

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
        query = "SELECT priority, COUNT(*) FROM logistics GROUP BY priority"

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

    def set_newest_jcns(self):
        recentProblemsQuery = "SELECT item_name FROM logistics ORDER BY due_date DESC LIMIT 5;"

        try:
            result = execute_query(recentProblemsQuery)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not result:
            print("The query is empty.")

        for i, work_order in enumerate(result):
            label_name = f"set_{i+1}_count"
            label = getattr(self, label_name, None)
            if label is not None:
                label.setText(str(work_order[0]))

    ##############################################################################################################
    # INVENTORY SECTION
    def load_inventory_data(self):
        # Execute query to get name, stock on hand, min stock, location, cost, vendor, notes, entered by
        # name = users on logistics.entered_by = users.user_id
        # stock_on_hand, minimum_stock_number, stock_location, cost_per_item, vendor, notes

        query = "SELECT  \
                logistics.item_name, \
                logistics.stock_on_hand, \
                logistics.minimum_stock_number, \
                logistics.stock_location, \
                logistics.cost_per_item, \
                logistics.vendor, \
                logistics.notes, \
                users.username\
            FROM \
                logistics\
            JOIN \
                users ON logistics.entered_by = users.user_id"

        try:
            # Fetch all the rows returned by the query
            inventory_data = execute_query(query)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not inventory_data:
            print("The query is empty.")

        # print first row of the query
        # print(inventory_data[2])

        # set the number of rows
        self.inventory_table.setRowCount(len(inventory_data))
        # hide row numbers
        self.inventory_table.verticalHeader().setVisible(False)
        # set column widths
        self.inventory_table.setColumnWidth(0, 100) # Item Name
        self.inventory_table.setColumnWidth(1, 80) # Stock on hand
        self.inventory_table.setColumnWidth(2, 80) # Min stock
        self.inventory_table.setColumnWidth(3, 50) # Stock location
        self.inventory_table.setColumnWidth(4, 70) # Cost
        self.inventory_table.setColumnWidth(5, 70) # Vendor
        self.inventory_table.setColumnWidth(6, 100) # Notes
        self.inventory_table.setColumnWidth(7, 100) # Entered by

        # resize "Notes" column to fill remaining space
        self.inventory_table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)

        # push data into the table
        row_index = 0  # Initialize the row index
        # push data into the table
        for data in inventory_data:
            # 0 item_name
            # 1 stock on hand
            # 2 min stock
            # 3 location
            # 4 cost
            # 5 vendor
            # 6 note
            # 7 entered by
            # print(f"[5][{data[5]}|[7][{data[7]}]]")
            self.inventory_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(data[0])))     # name
            self.inventory_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(data[1])))     # stock on hand
            self.inventory_table.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(data[2])))     # min stock
            self.inventory_table.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(data[3])))     # location
            self.inventory_table.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(data[4])))     # cost
            self.inventory_table.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(data[5])))     # vendor
            self.inventory_table.setItem(row_index, 6, QtWidgets.QTableWidgetItem(str(data[6])))     # note
            self.inventory_table.setItem(row_index, 7, QtWidgets.QTableWidgetItem(str(data[7])))     # entered by
            # print("Vendor:", self.inventory_table.item(row_index, 5).text())                        # Vendor column
            # print("Entered by:", self.inventory_table.item(row_index, 7).text())                    # Entered by column

            row_index += 1                                                                           # Increment the row index

        # if the priority is 1, set the background color of that priority cell to red
        for row in range(self.inventory_table.rowCount()):
            priority_item = self.inventory_table.item(row, 7)
            priority = priority_item.text()
            if priority == "1":
                priority_item.setBackground(QtGui.QColor(255, 0, 0))                                        # Red background
                priority_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))                      # White text color
            elif priority == "2":
                priority_item.setBackground(QtGui.QColor(255, 255, 0))                                      # Yellow background
                priority_item.setForeground(QtGui.QBrush(QtGui.QColor(0, 0, 0)))                            # Black text color
            elif priority == "3":
                priority_item.setBackground(QtGui.QColor(0, 255, 0))                                        # Green background
                priority_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))                      # White text color

    def update_line_edits(self, row):
        item_name = self.inventory_table.item(row, 0)
        stock_on_hand = self.inventory_table.item(row, 1)
        min_stock = self.inventory_table.item(row, 2)
        location = self.inventory_table.item(row, 3)
        cost = self.inventory_table.item(row, 4)
        vendor = self.inventory_table.item(row, 5)
        notes = self.inventory_table.item(row, 6)
        enterer = self.inventory_table.item(row, 7)
        
        # # print all the items in row
        # for i in range(self.inventory_table.columnCount()):
        #     print(f"Row[{i}] text:[{self.inventory_table.item(row, i).text()}]")

        # Now update your line edits and text edits with the content from the clicked row
        self.name_lineEdit.setText(item_name.text())
        self.stock_on_hand_lineEdit.setText(stock_on_hand.text())
        self.min_stock_lineEdit.setText(min_stock.text())
        self.location_lineEdit.setText(location.text())
        self.cost_lineEdit.setText(cost.text())
        self.vendor_lineEdit.setText(vendor.text())
        self.notes_textEdit.setText(notes.text())
        self.enterer_lineEdit.setText(enterer.text())

    #############################################################################################################
    # LOAD CHARTS DATA SECTION 
    def load_charts_data(self):
        # Call DB stored procedure ShowPartsData() to get the last 7 days of data
        topQuery = "CALL ShowPartsData()"

        try:
            parts_data = execute_query(topQuery)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not parts_data:
            print("The query is empty.")

        # item_name, cost_per_item, due_date, priority
        topSeries = QBarSeries()

        barSet = QBarSet("Cost per Item")

        for row in parts_data:
            item_name = row[0]
            cost_per_item = float(row[1])

            barSet.append(cost_per_item)

        topSeries.append(barSet)

        topChart = QChart()
        topChart.addSeries(topSeries)
        # topChart.setTitle("Parts Cost")

        axisX = QBarCategoryAxis()
        topChart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        topSeries.attachAxis(axisX)

        axisY = QValueAxis()
        topChart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        topSeries.attachAxis(axisY)

        self.topChartview = QChartView()
        self.topChartview.setChart(topChart)
        self.topChartview.setRenderHint(QPainter.Antialiasing)

        self.topChartview.setParent(self.chart_top)
        self.topChartview.resize(self.chart_top.size())
        self.topChartview.show()

        # ## Bottom chart
        getInventoryData = "CALL GetInventoryData()"

        try:
            inventory_data = execute_query(getInventoryData)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not inventory_data:
            print("The query is empty.")

        # print(f"Inventory data: {inventory_data}")

        bottomSeries = QBarSeries()

        for row in inventory_data:
            item_name = row[1]
            stock_on_hand = row[0]
            stock = int(stock_on_hand)
            cost_per_item = row[4]

            item_set = QBarSet(item_name)
            item_set.append(stock)

            cost_set = QBarSet(item_name)
            cost_set.append(cost_per_item)

            bottomSeries.append(item_set)
            bottomSeries.append(cost_set)

        bottomChart = QChart()
        bottomChart.addSeries(bottomSeries)
        bottomChart.setTitle("Inventory")

        self.bottomChartview = QChartView()
        self.bottomChartview.setChart(bottomChart)
        self.bottomChartview.setRenderHint(QPainter.Antialiasing)

        self.bottomChartview.setParent(self.chart_bottom)
        self.bottomChartview.resize(self.chart_bottom.size())
        self.bottomChartview.show()

    ############################################################################################################
    ## NEW JCN's SECTION
    def update_new_part_fields(self):
        # change the page
        self.switch_page(self.addPart_view, "NEW PART")

        # Update priority_comboBox drop down to show 1, 2, and 3 priority levels
        self.priority_comboBox.addItem("1")
        self.priority_comboBox.addItem("2")
        self.priority_comboBox.addItem("3")
        # Set default priority to 3
        self.priority_comboBox.setCurrentIndex(2)

        # Update locationType_comboBox with enums from location_type in the logistics table
        # location_types_list = "SELECT location_type FROM logistics"
        location_types_list = "SELECT COLUMN_TYPE FROM information_schema.COLUMNS WHERE TABLE_NAME = 'logistics' AND COLUMN_NAME = 'location_type'"
        
        try:
            location_names = execute_query(location_types_list)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not location_names:
            print("The query is empty.")

        enum_values = location_names[0][0].decode().split("'")[1::2]
        # print(f"enum_values: {enum_values}")

        for name in enum_values:
            self.locationType_comboBox.addItem(name)


        # Center disposition and priority text
        # self.disposition_lineEdit_2.setAlignment(Qt.AlignCenter)
        self.priority_comboBox.setEditable(True)
        self.priority_comboBox.lineEdit().setAlignment(Qt.AlignCenter)

    def add_new_part(self):
        item_name = self.item_name_lineEdit.text()
        min_stock_num = self.min_stock_num_lineEdit.text()
        location = self.location_lineEdit_2.text()
        itemCost = self.itemCost_lineEdit.text()

        # get the username of the person who is logged in
        reportedBy = '3' #self.username
        uniqueIdent = self.uniqueIdent_lineEdit.text()
        notes = self.notes_textEdit_2.toPlainText()
        repairCost = self.repairCost_lineEdit.text()
        vendor = self.vendor_lineEdit_2.text()
        origPN = self.origPN_lineEdit.text()
        serialNumber = self.serialNumber_lineEdit.text()
        nsn = self.nsn_lineEdit.text()
        locationType = self.locationType_comboBox.currentText()

        priority = self.priority_comboBox.currentText()
        stock_on_hand = self.stock_on_hand_lineEdit_2.text()

        reason = self.reason_textEdit_2.toPlainText()  # this wont be used for now.

        # Insert new record into the table
        insert_query = "INSERT INTO logistics (item_name, minimum_stock_number, stock_location, cost_per_item, \
            entered_by, unique_identifier, notes, repair_cost, vendor, original_part_number, serial_number, national_stock_number, location_type, \
            priority, stock_on_hand) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        execute_insert_query(insert_query, (item_name, min_stock_num, location, itemCost, \
                                                 reportedBy, uniqueIdent, notes, repairCost, vendor, origPN, serialNumber, nsn, locationType, \
                                                 priority, stock_on_hand))        

        # Clear the fields
        self.item_name_lineEdit.clear()
        self.min_stock_num_lineEdit.clear()
        self.location_lineEdit_2.clear()
        self.itemCost_lineEdit.clear()
        self.uniqueIdent_lineEdit.clear()
        self.notes_textEdit_2.clear()
        self.repairCost_lineEdit.clear()
        self.vendor_lineEdit_2.clear()
        self.origPN_lineEdit.clear()
        self.serialNumber_lineEdit.clear()
        self.nsn_lineEdit.clear()
        # self.locationType_lineEdit.clear()
        self.priority_comboBox.clear()
        self.stock_on_hand_lineEdit_2.clear()
        self.reason_textEdit_2.clear()

        # update jcn number
        self.update_new_part_fields()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
