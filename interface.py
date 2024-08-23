import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Username and password labels and fields
        username_label = QLabel("Username:")
        layout.addWidget(username_label)
        self.username_field = QLineEdit()
        layout.addWidget(self.username_field)

        password_label = QLabel("Password:")
        layout.addWidget(password_label)
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_field)

        # Login button
        login_button = QPushButton("Login")
        layout.addWidget(login_button)

        # Connect login button to login function
        login_button.clicked.connect(self.login)

    def login(self):
        username = self.username_field.text()
        password = self.password_field.text()

        if username == "123" and password == "123":
            self.parent().showMainWindow()
            self.close()
        else:
            print("Invalid username or password")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Trading Bot")
        self.setFixedSize(600, 400)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.strategy_tab = QWidget()
        self.order_list_tab = QWidget()
        self.profile_tab = QWidget()

        self.tab_widget.addTab(self.strategy_tab, "Strategy")
        self.tab_widget.addTab(self.order_list_tab, "Order List")
        self.tab_widget.addTab(self.profile_tab, "Profile")

        self.createStrategyTab()

    def createStrategyTab(self):
        layout = QVBoxLayout(self.strategy_tab)

        # Strategy inputs
        symbol_label = QLabel("Symbol:")
        symbol_field = QLineEdit()
        layout.addLayout(self.createInputLayout(symbol_label, symbol_field))

        amount_label = QLabel("Amount:")
        amount_field = QLineEdit()
        layout.addLayout(self.createInputLayout(amount_label, amount_field))

        profit_label = QLabel("Profit Price:")
        profit_field = QLineEdit()
        layout.addLayout(self.createInputLayout(profit_label, profit_field))

        loss_label = QLabel("Loss Price:")
        loss_field = QLineEdit()
        layout.addLayout(self.createInputLayout(loss_label, loss_field))

        # Start and stop buttons
        start_button = QPushButton("Start")
        start_button.setStyleSheet("background-color: blue; color: white;")
        stop_button = QPushButton("Stop")
        stop_button.setStyleSheet("background-color: blue; color: white;")

        button_layout = QHBoxLayout()
        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)
        layout.addLayout(button_layout)

    def createInputLayout(self, label, input_field):
        input_layout = QHBoxLayout()
        input_layout.addWidget(label)
        input_layout.addWidget(input_field)

        return input_layout

    def showMainWindow(self):
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    main_window = MainWindow()
    login_window.setParent(main_window)

    login_window.show()

    sys.exit(app.exec_())