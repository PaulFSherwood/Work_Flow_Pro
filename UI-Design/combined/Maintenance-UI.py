# WorkFlow Pro

import os
import sys
import mysql.connector
import datetime

# Python bindings for Qt
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QPieSeries, QBarSet, QBarSeries
from PyQt6.QtCore import Qt, QPointF, QTimer, QDateTime
from PyQt6.QtGui import QPainter

# Icon library
import qtawesome # load last to avoid using PyQt5 and breaking icons

from utilities import decrypt_config
from database_utilites import execute_query, execute_insert_query


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi('Maintenance-UI.ui', self)

        # Data Store
        self.all_debrief_data = None

        # Update Data Store
        self.mission_profile_group = self.run_stored_procedure("CALL GetAllMissionProfiles()")
        self.devices_group = self.run_stored_procedure("CALL GetAllDevices()")
        self.instructors_group = self.run_stored_procedure("CALL GetInstructorUsers()")
        self.maintenance_group = self.run_stored_procedure("CALL GetMaintenanceUsers()")
        
        # Set window icon
        icon = qtawesome.icon("mdi6.account-wrench-outline", color="#404258")
        app.setWindowIcon(icon)

        ############################################################################################################
        # ICON SETUP (qta-browser)
        # Setting up icons for each button (couldn't find another way to show icons but with buttons)
        self.left_menu_button.setIcon(qtawesome.icon('fa5s.sign-in-alt', color='orange', hflip=True))
        self.pushButton_7.setIcon(qtawesome.icon('fa.wrench', color='orange'))
        self.pushButton_7.setIconSize(QtCore.QSize(32, 32))  # Rezise the icon to 32x32

        self.dashboard_pushButton.setIcon(qtawesome.icon('mdi.monitor-dashboard', color='orange'))
        self.work_orders_pushButton.setIcon(qtawesome.icon('ri.list-unordered', color='orange'))
        self.inventory_pushButton.setIcon(qtawesome.icon('mdi.warehouse', color='orange'))
        self.work_orders_pushButton.setIcon(qtawesome.icon('fa.bar-chart-o', color='orange'))
        self.charts_pushButton.setIcon(qtawesome.icon('mdi6.chart-areaspline', color='orange'))
        self.CreateJCN_pushButton.setIcon(qtawesome.icon('mdi6.file-document-edit-outline', color='orange'))
        self.debrief_pushButton.setIcon(qtawesome.icon('mdi.briefcase-download-outline', color='orange'))

        ############################################################################################################
        # BUTTON CONNECTIONS (signals and slots)
        # show and hide the right_menu_widget when menu_button is clicked
        self.left_menu_button.clicked.connect(lambda: self.left_menu_widget.setHidden(not self.left_menu_widget.isHidden()))
        self.dashboard_pushButton.clicked.connect(lambda: self.switch_page(self.dashboard_view, "DASHBOARD"))
        self.work_orders_pushButton.clicked.connect(lambda: self.switch_page(self.work_orders_view, "WORK ORDERS"))
        self.inventory_pushButton.clicked.connect(lambda: self.switch_page(self.inventory_view, "INVENTORY"))
        self.charts_pushButton.clicked.connect(lambda: self.switch_page(self.charts_view, "CHARTS"))
        # self.CreateJCN_pushButton.clicked.connect(lambda: self.switch_page(self.newJCN_view, "NEW JCN"))
        self.CreateJCN_pushButton.clicked.connect(self.update_new_jcn_fields)
        self.disposition_comboBox.currentIndexChanged.connect(self.on_disposition_changed)
        self.debrief_pushButton.clicked.connect(lambda: self.switch_page(self.debrief_view, "DEBRIEF"))

        ############################################################################################################
        # USER ACTION UPDATES
        self.work_order_table.cellClicked.connect(self.update_line_edits)  
        self.addJCN_pushButton.clicked.connect(self.add_new_jcn)     
        self.update_pushButton.clicked.connect(self.update_jcn_database)
        self.debrief_table.cellClicked.connect(self.update_debrief_input_widget) 

        ############################################################################################################
        # TABLE SETUP / TAB SETUP
        self.dashboard_bar_chart()
        self.set_newest_jcns()
        self.load_work_order_data()
        self.load_inventory_data()
        self.load_charts_data()

        self.set_priority_counts()
        self.load_debrief_data()
    
    ############################################################################################################
    # Helper Function
    def switch_page(self, widget, title):
        self.stackedWidget.setCurrentWidget(widget)
        self.title_label.setText(title)

    def run_stored_procedure(self, query):
        try:
            result = execute_query(query)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not result:
            print("The query is empty.")
        return result
    
    # Get the debrief data 
    def getDebriefData(self):
        debrief_query = "SELECT * FROM flight_simulator_db.debrief"
        try:
            self.all_debrief_data = execute_query(debrief_query)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not self.all_debrief_data:
            print("The query is empty.")

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
        priorityQuery = "SELECT priority, COUNT(*) FROM workorders GROUP BY priority"

        try:
            result = execute_query(priorityQuery)
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
        recentProblemsQuery = "SELECT creation_reason FROM workorders ORDER BY creation_date DESC LIMIT 5;"

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

    ############################################################################################################
    # WORK ORDER SECTION
    def load_work_order_data(self):
        # Execute query to get jcn, simulator name, disposition, creation_reason, creation_date, priority, correction_notes
        query = "SELECT  \
                workorders.jcn, \
                workorders.disposition, \
                workorders.creation_reason, \
                workorders.creation_date, \
                workorders.priority, \
                workorders.correction_note, \
                simulators.model\
            FROM \
                workorders\
            JOIN \
                simulators ON workorders.simulator_id = simulators.simulator_id"

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
        self.work_order_table.setColumnWidth(1, 80)  # Simulator
        self.work_order_table.setColumnWidth(2, 80)  # Disposition
        self.work_order_table.setColumnWidth(3, 200) # Reason
        self.work_order_table.setColumnWidth(4, 90)  # Date
        self.work_order_table.setColumnWidth(5, 50)  # Priority
        self.work_order_table.setColumnWidth(6, 100) # Notes

        # resize "Notes" column to fill remaining space
        self.work_order_table.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)

        # push data into the table
        row_index = 0  # Initialize the row index
        # push data into the table
        for work_order in work_order_data:
            # 0 jcn
            # 1 disposition
            # 2 creation_reason
            # 3 creation_date
            # 4 priority
            # 5 correction_note
            # 6 simulator
            self.work_order_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(work_order[0])))     # jcn
            self.work_order_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(work_order[6]))          # simulator
            # Center the disposition
            disposition_item = QtWidgets.QTableWidgetItem(work_order[1])
            disposition_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)                                  # Center disposition
            self.work_order_table.setItem(row_index, 2, disposition_item)

            self.work_order_table.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(work_order[2])))     # creation_reason
            self.work_order_table.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(work_order[3])))     # creation_date

            # Center the priority number
            priority_item = QtWidgets.QTableWidgetItem(str(work_order[4]))                                  # priority
            priority_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)                                    # Center the content
            self.work_order_table.setItem(row_index, 5, priority_item)

            self.work_order_table.setItem(row_index, 6, QtWidgets.QTableWidgetItem(work_order[5]))          # correction_note
            
            row_index += 1                                                                                  # Increment the row index

        # if the priority is 1, set the background color of that priority cell to red
        for row in range(self.work_order_table.rowCount()):
            priority_item = self.work_order_table.item(row, 5)
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
        jcn_item = self.work_order_table.item(row, 0)
        simulator_item = self.work_order_table.item(row, 1)
        disposition_item = self.work_order_table.item(row, 2)
        reason_item = self.work_order_table.item(row, 3)
        priority_item = self.work_order_table.item(row, 5)
        notes_item = self.work_order_table.item(row, 6)

        # Now update your line edits and text edits with the content from the clicked row
        self.JCN_lineEdit.setText(jcn_item.text())
        self.simulator_lineEdit.setText(simulator_item.text())

        # Check if the disposition is "INW" to decide whether to lock the fields
        current_disposition = disposition_item.text()
        self.disposition_comboBox.setCurrentText(current_disposition)
 
        # Update the disposition_comboBox with the list of AWE, AWM, AWT, INW, or CLO  Then make the current selected to be what is in the disposition text
        options = ['AWE', 'AWM', 'AWT', 'INW', 'CLO']
        self.disposition_comboBox.clear()
        self.disposition_comboBox.addItems(options)

        self.priority_lineEdit.setText(priority_item.text())

        # lock fields if INW
        self.reason_textEdit.setText(reason_item.text())
        # self.reason_textEdit.setEnabled(is_disabled)

        self.notes_textEdit.setText(notes_item.text())
        # self.notes_textEdit.setEnabled(is_disabled)


    def on_disposition_changed(self, index):
        # Get the current text
        current_disposition = self.disposition_comboBox.currentText()
        # print(current_disposition)
        is_disabled = current_disposition == "INW"

        # if the current_dispositiion is not "INW" then setEnabled should be false
        self.JCN_lineEdit.setEnabled(is_disabled)
        self.simulator_lineEdit.setEnabled(is_disabled)
        self.priority_lineEdit.setEnabled(is_disabled)
        self.reason_textEdit.setEnabled(is_disabled)
        self.notes_textEdit.setEnabled(is_disabled)

    def update_jcn_database(self):
        # Get the current values from the line edits
        jcn = self.JCN_lineEdit.text()
        simulator = self.simulator_lineEdit.text()
        priority = self.priority_lineEdit.text()
        reason = self.reason_textEdit.toPlainText()
        notes = self.notes_textEdit.toPlainText()
        disposition = self.disposition_comboBox.currentText()

        print("Disposition: ", disposition)

        # Get the simulator_id from the simulator name
        simulator_id_query = "SELECT simulator_id FROM simulators WHERE model = %s"

        try:
            simulator_id = execute_query(simulator_id_query, (simulator,))[0][0]
        except Exception as e:
            print("Error with query: ", e)
            return
        if not simulator_id:
            print("The query is empty.")
            return

        # Update the database
        update_query = "UPDATE workorders SET simulator_id = %s, priority = %s, creation_reason = %s, correction_note = %s, disposition = %s WHERE jcn = %s"
        execute_insert_query(update_query, (simulator_id, priority, reason, notes, disposition, jcn))

        # Clear the fields
        self.JCN_lineEdit.clear()
        self.simulator_lineEdit.clear()
        self.priority_lineEdit.clear()
        self.reason_textEdit.clear()
        self.notes_textEdit.clear()
        self.disposition_comboBox.clear()
        # update jcn number
        self.load_work_order_data()

    ############################################################################################################
    # DEBRIEF SECTION
    def load_debrief_data(self):
        # Update the data
        self.getDebriefData()
        
        # print(self.all_debrief_data[0][11])

        # set the number of rows
        self.debrief_table.setRowCount(len(self.all_debrief_data))
        # hide row numbers
        self.debrief_table.verticalHeader().setVisible(False)
        # set column widths
        # Debrief ID | Date | Instructor | Device | Mission Profile | Start Time | Stop Time
        self.debrief_table.setColumnWidth(0, 120) # Debrief ID
        self.debrief_table.setColumnWidth(1, 100) # Date
        self.debrief_table.setColumnWidth(2, 100) # Instructor
        self.debrief_table.setColumnWidth(3, 100) # Device
        self.debrief_table.setColumnWidth(4, 100) # Mission Profile
        self.debrief_table.setColumnWidth(5, 100) # Start Time
        self.debrief_table.setColumnWidth(6, 100) # Stop Time

        # push data into the table
        row_index = 0  # Initialize the row index
        # push data into the table
        for debrief in self.all_debrief_data:                       ## debrief[#] is the index of the debrief data
            self.debrief_table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(debrief[0])))
            self.debrief_table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(debrief[13])))
            self.debrief_table.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(debrief[11])))
            self.debrief_table.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(debrief[12])))
            self.debrief_table.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(debrief[15])))
            self.debrief_table.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(debrief[7])))
            self.debrief_table.setItem(row_index, 6, QtWidgets.QTableWidgetItem(str(debrief[8])))

            row_index += 1                                                                                  # Increment the row index

        # If the Stop time is past the current time set the background color of that cell to light red
        for row in range(self.debrief_table.rowCount()):
            stop_time_item = self.debrief_table.item(row, 6)
            stop_time = stop_time_item.text()
            if stop_time > QDateTime.currentDateTime().toString("yyyy-MM-ddThh:mm:ss"):
                stop_time_item.setBackground(QtGui.QColor(255, 0, 0))                                        # Red background
                stop_time_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))                      # White text color

    def update_debrief_input_widget(self, row):
        # Actual Start  : start_lineEdit            : time
        # Actual Stop   : stop_lineEdit             : time
        # hours (THE)   : actual_hours_lineEdit     : time
        # MDT           : mdt_lineEdit              : integer
        # Mission Status: mission_status_comboBox   : string (ENUM from database.MissionStatus)
        # MIRT          : mirt_lineEdit             : integer
        # Sched. Start  : sched_start_lineEdit      : time
        # Sched. Stop   : sched_stop_lineEdit       : time
        # Sched. Hours  : sched_hours_lineEdit      : time
        # Debriefer     : debriefer_comboBox        : string (ENUM from database.users) (default is in debrief table but should show other maintenance in users)
        # Instructor    : instructor_comboBox       : string (ENUM from database.users) (default is in debrief table but should show other instructos in users)
        # Device        : device_comboBox           : string (ENUM from database.devices)
        ## need to update database so it has a table for devices, and mission
        # Debrief ID    : debrief_ID_lineEdit       : bigint (example: 202403090732 | year month day hour minute second)
        # JCN           : debrief_jcn_lineEdit      : varchar(255) (will check if the JCN exists when submit is hit [submit_debrief_pushButton])
        # date          : debrief_date_lineEdit     : date (will be the current date)
        # mission profil: mission_profile_comboBox  : string (ENUM from database.MissionProfile)
        # Submit Button : submit_debrief_pushButton : button (will submit the debrief to the database)

        # update the debrief data
        # self.getDebriefData()
        self.all_debrief_data
        # Pull out the data we need
        debrief_id_item = str(self.all_debrief_data[row][0])
        actual_start_time = str(self.all_debrief_data[row][1])
        actual_stop_time = str(self.all_debrief_data[row][2])
        hours = str(self.all_debrief_data[row][3])
        mission_status = str(self.all_debrief_data[row][4])
        mdt = str(self.all_debrief_data[row][5])
        mirt = str(self.all_debrief_data[row][6])
        sched_start_time = str(self.all_debrief_data[row][7])
        sched_stop_time = str(self.all_debrief_data[row][8])
        sched_hours = str(self.all_debrief_data[row][9])
        debriefer = str(self.all_debrief_data[row][10])
        instructor_name = str(self.all_debrief_data[row][11])
        device_name = str(self.all_debrief_data[row][12])
        debrief_date = str(self.all_debrief_data[row][13])
        debrief_jcn = str(self.all_debrief_data[row][14])
        mission_profile = str(self.all_debrief_data[row][15])

        # Now update your line edits and text edits with the content from the clicked row
        self.debrief_ID_lineEdit.setText(debrief_id_item)
        self.start_lineEdit.setText(actual_start_time)
        self.stop_lineEdit.setText(actual_stop_time)
        self.actual_hours_lineEdit.setText(hours)
        self.mdt_lineEdit.setText(mdt)
        self.mirt_lineEdit.setText(mirt)
        self.sched_start_lineEdit.setText(sched_start_time)
        self.sched_stop_lineEdit.setText(sched_stop_time)
        self.sched_hours_lineEdit.setText(sched_hours)
        self.debrief_date_lineEdit.setText(debrief_date)
        self.debrief_jcn_lineEdit.setText(debrief_jcn)

        # Generate mission_status options msOptions
        self.mission_status_comboBox.addItem("Incomplete")
        self.mission_status_comboBox.addItem("Complete")
        self.mission_status_comboBox.setCurrentText(mission_status)

        # print(self.maintenance_group)
        # Add all users to the debriefer_comboBox
        for user in self.maintenance_group:
            self.debriefer_comboBox.addItem(user[0])
        self.debriefer_comboBox.setCurrentText(debriefer)
        
        # Add all users to the instructor_comboBox
        for user in self.instructors_group:
            self.instructor_comboBox.addItem(user[0])
        self.instructor_comboBox.setCurrentText(instructor_name)
        print("Instructor: " + instructor_name)

        # Add all devices to the device_comboBox
        for device in self.devices_group:
            self.device_comboBox.addItem(device[0])
        self.device_comboBox.setCurrentText(device_name)
        # Add all mission profiles to the mission_profile_comboBox
        self.mission_profile_comboBox.clear()
        for profile in self.mission_profile_group:
            self.mission_profile_comboBox.addItem(profile[0])
        self.mission_profile_comboBox.setCurrentText(mission_profile)

        # allow edits
        self.mission_status_comboBox.setEnabled(True)
        # self.mission_status_comboBox.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)





    ##############################################################################################################
    # INVENTORY SECTION
    def load_inventory_data(self):
        # Execute the query to fetch the data
        query = "CALL GetInventoryData()"

        try:
            inventory_data = execute_query(query)
        except Exception as e:
            print("Error with query: ", e)
            return
        if not inventory_data:
            print("The query is empty.")

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
    # LOAD CHARTS DATA SECTION 
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

    ############################################################################################################
    ## NEW JCN's SECTION
    def update_new_jcn_fields(self):
        # change the page
        self.switch_page(self.newJCN_view, "NEW JCN")
        # Get todays date
        today = datetime.date.today()
        date = today.strftime("%Y%m%d")
        # set the date time of 'dateFound_dateTimeEdit' to the current date and time
        self.dateFound_dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        
        # Get the current number of JCNs
        query = f"SELECT COUNT(*) FROM workorders WHERE DATE(creation_date) = CURDATE() AND jcn LIKE '{date}%'" # fstring required for the date

        try:
            count = execute_query(query)[0][0]
        except Exception as e:
            print("Error with query: ", e)
            return
        if not count:
            print("The query is empty.")
        # make the new jcn number
        jcn_number = f"{date}{str(count + 1).zfill(3)}" # zfill is used to pad the number with 0's
        # set the new jcn number
        self.JCN_lineEdit_2.setText(jcn_number)

        # Update the simulator list
        simulator_list = "SELECT model FROM simulators"
        simulator_names = execute_query(simulator_list)
        for sims in simulator_names:
            self.simulator_comboBox.addItem(sims[0])

        # Default disposition to "AWM" awaiting maintenance 'disposition_lineEdit_2'
        self.disposition_lineEdit_2.setText("AWM")

        # Update priority_comboBox drop down to show 1, 2, and 3 priority levels
        self.priority_comboBox.addItem("1")
        self.priority_comboBox.addItem("2")
        self.priority_comboBox.addItem("3")
        # Set default priority to 3
        self.priority_comboBox.setCurrentIndex(2)

        # Update the subsystem list
        subsystem_list = "SELECT name FROM subsystems"
        subsystem_names = execute_query(subsystem_list)
        for subs in subsystem_names:
            self.subsystem_comboBox.addItem(subs[0])

        # Center disposition and priority text
        self.disposition_lineEdit_2.setAlignment(Qt.AlignCenter)
        self.priority_comboBox.setEditable(True)
        self.priority_comboBox.lineEdit().setAlignment(Qt.AlignCenter)

    def add_new_jcn(self):
         # 0 jcn
        # 1 disposition
        # 2 creation_reason
        # 3 creation_date
        # 4 priority
        # 5 correction_note
        # 6 simulator
        jcn = self.JCN_lineEdit_2.text()
        reportedBy = self.reportedBy_lineEdit.text()
        disposition = self.disposition_lineEdit_2.text()
        creation_reason = self.reason_textEdit_2.toPlainText()
        priority = self.priority_comboBox.currentText()
        correction_note = self.notes_textEdit_2.toPlainText()
        
        creation_date = self.dateFound_dateTimeEdit.dateTime().toString("yyyy-MM-dd")

        simulator = self.simulator_comboBox.currentText()
        subsystem = self.subsystem_comboBox.currentText()

        # Get simulator_id and subsystem_id from the names
        sim_id_query = "SELECT simulator_id FROM simulators WHERE model = %s"
        try:
            sim_id = execute_query(sim_id_query, (simulator,))[0][0]
        except Exception as e:
            print("Error with query: ", e)
            return
        if not sim_id:
            print("The query is empty.")

        subs_id_query = "SELECT subsystem_id FROM subsystems WHERE name = %s"
        try:
            subs_id = execute_query(subs_id_query, (subsystem,))[0][0]
        except Exception as e:
            print("Error with query: ", e)
            return
        if not subs_id:
            print("The query is empty.")

        # print(f"jcn: {jcn} reportedBy: {reportedBy} disposition: {disposition} creation_reason: {creation_reason} \
        #         creation_date: {creation_date} priority: {priority} correction_note: {correction_note} \
        #         simulator: {simulator} subsystem: {subsystem}")
        # Insert new JCN
        insert_query = "INSERT INTO workorders (jcn, \
                                                reported_by_name, \
                                                disposition, \
                                                creation_reason, \
                                                creation_date, \
                                                priority, \
                                                correction_note, \
                                                simulator_id, \
                                                subsystem_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"  # make sure the number of %s matches selections
        execute_insert_query(insert_query, (jcn, 
                                                 reportedBy, 
                                                 disposition, 
                                                 creation_reason, 
                                                 creation_date, 
                                                 priority, 
                                                 correction_note, 
                                                 sim_id, 
                                                 subs_id))

        # Clear the fields
        self.disposition_lineEdit_2.clear()
        self.reportedBy_lineEdit.clear()
        self.reason_textEdit_2.clear()
        self.notes_textEdit_2.clear()
        self.priority_comboBox.clear()
        # update jcn number
        self.update_new_jcn_fields()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
