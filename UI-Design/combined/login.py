import sys
import json
import getpass
import bcrypt
import subprocess
from cryptography.fernet import Fernet
from utilities import decrypt_config, Validator
from database_utilites import execute_query, execute_insert_query
from login_utilities import authenticate, get_user_role, get_user_id

# Python bindings for Qt
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi

# Icon library
import qtawesome  #load last to avoid using PyQt5 and breaking icons

# Decrypt and save the config
config = decrypt_config()

# Set db_host, db_user, db_password, and db_database for later use
db_host = config['host']
db_user = config['user']
db_password = config['password']
db_database = config['database']

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui",self)

        # Set window icon
        icon = qtawesome.icon("mdi6.login-variant", color="#404258")
        app.setWindowIcon(icon)

        self.LoginPushButton.clicked.connect(self.loginfunction)
        self.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.GetAccountPushButton.clicked.connect(self.gotocreateacc)
        
    def lauch_by_os(self, script_name, user_id):
        os = sys.platform
        try:
            if os == 'linux':
                subprocess.Popen(["/usr/local/bin/python3.9", f"{script_name}", "--user_id", f"{user_id}"])
            elif os == 'win32':
                subprocess.Popen(["python", f"{script_name}", "--user_id", f"{user_id}"])
        except subprocess.CalledProcessError as e:
            print("Error executing script: ", e)

    def loginfunction(self):
        username = self.UserNameLineEdit.text()
        password = self.PasswordLineEdit.text()

        # print(f"Username: {username} || Password: {password}")
        # print(f"{Validator.validate_username(username)}")

        if not Validator.validate_username(username):
            self.UserNameLineEdit.setText("Invalid username")
            return
        elif not Validator.validate_password(password):
            self.PasswordLineEdit.setText("Invalid password")
            return
        
        else:
            # switch to the appropriate screen
            # Authenticate the user
            if authenticate(username, password):
                # Execute the appropriate script based on the user's role
                role = get_user_role(username)
                user_id = get_user_id(username)

                # Execute the appropriate script based on the user's role
                if role == 'MANAGER':
                    self.lauch_by_os("Management-UI.py", user_id)
                elif role == 'MAINTENANCE':
                    self.lauch_by_os("Maintenance-UI.py", user_id)
                elif role == 'LOGISTICS':
                    self.lauch_by_os("Logistics-UI.py", user_id)
                else:
                    print("Default failure, no script found to run.")
                    sys.exit(1)
            sys.exit(0)

    # Switches from Login screen to Create Account screen
    def gotocreateacc(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createaccount.ui",self)
        self.CreateAccountPushButton.clicked.connect(self.create_account)
        self.ReturnLoginButton.clicked.connect(self.returntologin)

        self.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ConfirmPasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.RoleComboBox.addItem("MANAGER")
        self.RoleComboBox.addItem("MAINTENANCE")
        self.RoleComboBox.addItem("LOGISTICS")
        self.RoleComboBox.addItem("INSTRUCTOR")

    # Switches from Create Account screen to Login screen
    def returntologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def encrypt_password(self, password):
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password

    def create_account(self):
        username = self.UserNameLineEdit.text()
        role = self.RoleComboBox.currentText()

        if self.PasswordLineEdit.text() == self.ConfirmPasswordLineEdit.text():
            if not Validator.validate_username(username):
                print("Invalid username")
                return
            password = self.PasswordLineEdit.text()
            # Ensure username is not in the database
            check_user = f"SELECT username FROM users WHERE username = '{username}'"
            if execute_query(check_user):
                print("Username already exists")
                return
            else:
                # User is good encrypt the password and insert the new user
                password = self.encrypt_password(password)

                add_user = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
                params = (username, password, role)
                execute_insert_query(add_user, params)

                # Check if the user now exists in the database if it is switch back to the login page
                query = f"SELECT username FROM users WHERE username = '{username}'"
                if execute_query(query):
                    login = Login()
                    widget.addWidget(login)
                    widget.setCurrentIndex(widget.currentIndex()+1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    mainwindow = Login()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(480)
    widget.setFixedHeight(620)
    widget.show()
    app.exec()
