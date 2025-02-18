import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi

# Libraries for email validation
import re

class Validator:
    @staticmethod
    def validate_email(email):
        match = re.compile(r"^[-\w\.]+@([\w-]+\.)+[\w-]{2,4}$")
        return bool(match.fullmatch(str(email).lower()))

    @staticmethod
    def validate_password(password):
        # I wanted to add in all special characters but that could limit passwords
        sql_keywords = ['select', 'drop', ';', '--', 'insert', 'delete', 'update', 'union', 'create', 'alter']
        return not any(keyword in password.lower() for keyword in sql_keywords)

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui",self)
        self.LoginPushButton.clicked.connect(self.loginfunction)
        self.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.GetAccountPushButton.clicked.connect(self.gotocreateacc)

    def loginfunction(self):
        email = self.EmailLineEdit.text()
        password = self.PasswordLineEdit.text()
        if not Validator.validate_email(email):
                print("Invalid email")
                return
        print("Successfully logged in with email ", email, " and password ", password)

    # Switches from Login screen to Create Account screen
    def gotocreateacc(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)
        


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createaccount.ui",self)
        self.SignUpPushButton.clicked.connect(self.createaccfunction)
        self.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ConfirmPasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def createaccfunction(self):
        email = self.EmailLineEdit.text()
        print("pass: ", self.PasswordLineEdit.text(), " confirmpass: ", self.ConfirmPasswordLineEdit.text())
        if self.PasswordLineEdit.text() == self.ConfirmPasswordLineEdit.text():
            if not Validator.validate_email(email):
                print("Invalid email")
                return
            password = self.PasswordLineEdit.text()
            print("Successfully created account with email ", email, " and password ", password)
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
