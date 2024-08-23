import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.resize(300, 150)

        # Create the username and password labels, and input fields
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        # Create the login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        # Create a layout and add widgets to it
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "123" and password == "123":
            # Successful login
            self.hide()  # Hide the login page
            self.open_main_dashboard()
        else:
            # Failed login
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_main_dashboard(self):
        self.dashboard = MainDashboard()
        self.dashboard.show()


class MainDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Dashboard")
        self.resize(300, 150)

        # Create input items
        self.input1_label = QLabel("Input 1:")
        self.input1_input = QLineEdit()
        self.input2_label = QLabel("Input 2:")
        self.input2_input = QLineEdit()
        self.input3_label = QLabel("Input 3:")
        self.input3_input = QLineEdit()

        # Create buttons
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        # Create a layout and add widgets to it
        layout = QVBoxLayout()
        layout.addWidget(self.input1_label)
        layout.addWidget(self.input1_input)
        layout.addWidget(self.input2_label)
        layout.addWidget(self.input2_input)
        layout.addWidget(self.input3_label)
        layout.addWidget(self.input3_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())