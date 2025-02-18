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
import qtawesome as qta


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi('Maintenance-UI.ui', self)

        # Connect to the MySQL database
        self.db = mysql.connector.connect(
            host='localhost',
            user='sherwood',
            password='sherwood',
            database='flight_simulator_db'
        )

        ############################################################################################################
        # ICON SETUP (qta-browser)
        # Setting up icons for each button (couldn't find another way to show icons but with buttons)
        self.left_menu_button.setIcon(qta.icon('fa5s.sign-in-alt', color='orange', hflip=True))
        self.pushButton_7.setIcon(qta.icon('fa.wrench', color='orange'))
        self.pushButton_7.setIconSize(QtCore.QSize(32, 32))  # Rezise the icon to 32x32

        self.dashboard_pushButton.setIcon(qta.icon('mdi.monitor-dashboard', color='orange'))
        self.work_orders_pushButton.setIcon(qta.icon('ri.list-unordered', color='orange'))
        self.inventory_pushButton.setIcon(qta.icon('mdi.warehouse', color='orange'))
        self.work_orders_pushButton.setIcon(qta.icon('fa.bar-chart-o', color='orange'))
        self.charts_pushButton.setIcon(qta.icon('mdi6.chart-areaspline', color='orange'))
        self.CreateJCN_pushButton.setIcon(qta.icon('mdi6.file-document-edit-outline', color='orange'))

        # QTimer.singleShot(0, lambda: self.resizeEvent(None)) # force resize on start

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

        ############################################################################################################
        # USER ACTION UPDATES
        self.work_order_table.cellClicked.connect(self.update_line_edits)  
        self.addJCN_pushButton.clicked.connect(self.add_new_jcn)      

        ############################################################################################################
        # TABLE SETUP / TAB SETUP
        self.dashboard_bar_chart()
        self.set_awaiting_approval()
        self.load_work_order_data()
        self.load_inventory_data()
        self.load_charts_data()

        self.set_priority_counts()

    ############################################################################################################
    # SQL FUNCTION
    def execute_query(self, query, params=None):
        # Connection to the flight sim database
        db = mysql.connector.connect(
            host='localhost',
            user='sherwood',
            password='sherwood',
            database='flight_simulator_db'
        )
        # Create the cursor for the look in the db
        cursor = db.cursor()
        # Execute the query passed in by the user / function
        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        # save the result
        result = cursor.fetchall()
        # close the connection
        cursor.close()
        db.close()
        return result
    
    def execute_insert_query(self, query, params=None):
        db = mysql.connector.connect(
            host = 'localhost',
            user = 'sherwood',
            password = 'sherwood',
            database = 'flight_simulator_db'
        )
        cursor = db.cursor()
        try:
            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
        finally:
            cursor.close()
            db.close()
    
    ############################################################################################################
    # Helper Function
    def switch_page(self, widget, title):
        self.stackedWidget.setCurrentWidget(widget)
        self.title_label.setText(title)

    def resizeEvent(self, event):
        # print("frame_16 size:", self.size())  # Print the size of frame_16
        if event:
            event.accept()
        if hasattr(self, 'dashBoardChartView'):
            self.dashBoardChartView.resize(self.dashboard_frame_left.size())
            self.dashBoardChartView.show()
            # print("Chart dashBoard Size Hint:", self.dashBoardChartView.sizeHint())
            # print("Chart dashBoard Minimum Size:", self.dashBoardChartView.minimumSize())

        if hasattr(self, 'topChartview'):
            self.topChartview.resize(self.chart_top.size())
            self.topChartview.show()
            # print("Chart topChartview Size Hint:", self.topChartview.sizeHint())
            # print("Chart topChartview Minimum Size:", self.topChartview.minimumSize())

        if hasattr(self, 'bottomChartview'):
            self.bottomChartview.resize(self.chart_bottom.size())
            self.bottomChartview.show()
            # print("Chart bottomChartview Size Hint:", self.bottomChartview.sizeHint())
            # print("Chart bottomChartview Minimum Size:", self.bottomChartview.minimumSize())

        super().resizeEvent(event)

    def create_bar_set(self, label, value):
        barSet = QBarSet(label)
        barSet.append(value)
        return barSet
    
    ############################################################################################################
    # DASHBOARD FUNCTIONS
    def dashboard_bar_chart(self):
        dashQuery = "CALL GetWorkOrderCountPerDay()"
        work_order_count_per_day = self.execute_query(dashQuery)

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
        result = self.execute_query(query)

        # Store the counts
        priority_totals = {}
        for priority_count in result:
            priority = priority_count[0]
            count = priority_count[1]
            priority_totals[priority] = count

        # set pri_1_count
        self.pri_1_count.setText(str(priority_totals[1]))
        # set pri_2_count
        self.pri_2_count.setText(str(priority_totals[2]))
        # set pri_3_count
        self.pri_3_count.setText(str(priority_totals[3]))

    def set_awaiting_approval(self):
        recentProblemsQuery = "SELECT creation_reason FROM workorders ORDER BY creation_date DESC LIMIT 5;"
        # query = "SELECT creation_reason FROM workorders ORDER BY creation_date DESC LIMIT 5"
        # result = self.execute_query(query)
        result = self.execute_query(recentProblemsQuery)

        # for i, work_order in enumerate(result):
        #     label_name = f"set_{i+1}_count"  # Assuming the QLabel attribute names follow the pattern set_1_count, set_2_count, etc.
        #     label = getattr(self, label_name, None)
        #     if label is not None:
        #         label.setText(str(work_order[0]))
        for i, work_order in enumerate(result):
            label_name = f"set_{i+1}_count"
            label = getattr(self, label_name, None)
            if label is not None:
                label.setText(str(work_order[0]))

    ############################################################################################################
    # LOAD TABLE DATA
    # def load_table_data(self):
    #     #########################
    #     ## UPPER TABLE
    #     query = "CALL GetTechSummary()"
    #     tech_cost_data = self.execute_query(query)

    #     # print(tech_cost_data)

    #     # set the number of rows
    #     self.cost_upper_table.setRowCount(len(tech_cost_data))
    #     # hide row numbers
    #     self.cost_upper_table.verticalHeader().setVisible(False)

    #     # push data into the table
    #     for i, record in enumerate(tech_cost_data):
    #         self.cost_upper_table.setItem(i, 0, QtWidgets.QTableWidgetItem(record[0]))      # tech name
    #         self.cost_upper_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(record[1]))) # total cost
    #         self.cost_upper_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(record[1]))) # total hours

    #     #########################
    #     ## LOWER TABLE
    #     parts_data = self.execute_query("CALL show_parts_data()")
    #     # set the number of rows
    #     self.cost_lower_table.setRowCount(len(parts_data))
    #     # hide row numbers
    #     self.cost_lower_table.verticalHeader().setVisible(False)
    #     # push data into the table
    #     for i, record in enumerate(parts_data):
    #         self.cost_lower_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(record[0])))  # item name
    #         self.cost_lower_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(record[1])))  # cost per item
    #         self.cost_lower_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(record[2])))  # due date
    #         self.cost_lower_table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(record[3])))  # priority

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

        # Fetch all the rows returned by the query
        work_order_data = self.execute_query(query)

        # set the number of rows
        self.work_order_table.setRowCount(len(work_order_data))
        # hide row numbers
        self.work_order_table.verticalHeader().setVisible(False)
        # set column widths
        self.work_order_table.setColumnWidth(0, 100) # JCN
        self.work_order_table.setColumnWidth(1, 80) # Simulator
        self.work_order_table.setColumnWidth(2, 80) # Disposition
        self.work_order_table.setColumnWidth(3, 200) # Reason
        self.work_order_table.setColumnWidth(4, 90) # Date
        self.work_order_table.setColumnWidth(5, 50) # Priority
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
        self.disposition_lineEdit.setText(disposition_item.text())
        self.priority_lineEdit.setText(priority_item.text())
        self.reason_textEdit.setText(reason_item.text())
        self.notes_textEdit.setText(notes_item.text())

    ##############################################################################################################
    # INVENTORY SECTION
    def load_inventory_data(self):
        # Execute the query to fetch the data
        query = "CALL GetInventoryData()"
        inventory_data = self.execute_query(query)

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
        work_order_count_per_day_data = self.execute_query(topQuery)

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
        hours_worked_per_person_data = self.execute_query(bottomQuery)


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
        count = self.execute_query(query)[0][0]
        # make the new jcn number
        jcn_number = f"{date}{str(count + 1).zfill(3)}" # zfill is used to pad the number with 0's
        # set the new jcn number
        self.JCN_lineEdit_2.setText(jcn_number)

        # Update the simulator list
        simulator_list = "SELECT model FROM simulators"
        simulator_names = self.execute_query(simulator_list)
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
        subsystem_names = self.execute_query(subsystem_list)
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
        sim_id = self.execute_query(sim_id_query, (simulator,))[0][0]

        subs_id_query = "SELECT subsystem_id FROM subsystems WHERE name = %s"
        subs_id = self.execute_query(subs_id_query, (subsystem,))[0][0]

        print(f"jcn: {jcn} reportedBy: {reportedBy} disposition: {disposition} creation_reason: {creation_reason} \
                creation_date: {creation_date} priority: {priority} correction_note: {correction_note} \
                simulator: {simulator} subsystem: {subsystem}")
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
        self.execute_insert_query(insert_query, (jcn, 
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
