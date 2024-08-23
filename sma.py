import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTabWidget, QGridLayout, QSizePolicy, QComboBox, QMessageBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import *
import alpaca_trade_api as tradeapi
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from alpaca.data.requests import CryptoBarsRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.requests import StopOrderRequest, StopLimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import LimitOrderRequest
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest
import datetime
import pandas as pd
import openai

import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal

base_url="https://paper-api.alpaca.markets"
openai.api_key = "skkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk-yk4TIBiKckoe" "ssctyhU5T3BlbkFJz68IXN6mOfDhFkAXGkG3"
api = tradeapi.REST('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', base_url, api_version='v2')
trading_client = TradingClient('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', paper=True)
openai_key = "skkkkkkkkkkkkkkkkkkkkkkkk-yk4TIBiKckoessct" "yhU5T3BlbkFJz68IXN6mOfDhFkAXGkG3"

account = api.get_account()

active_assets=api.list_assets(status='active')


Bot_status = True


class BotThread(QThread):
    alert_signal = pyqtSignal(str)

    def run(self):
        print("123")
        # while Bot_status:


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
            self.open_main_window()
        else:
            # Failed login
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(1200, 800)

        # Create a tab widget
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(0, 0, self.width(), self.height())

        # Create the strategy settings tab
        self.strategy_tab = QWidget()
        self.tab_widget.addTab(self.strategy_tab, "Strategy Settings")

        # Create the order list tab
        self.order_tab = QWidget()
        self.tab_widget.addTab(self.order_tab, "Order List")

        # Create the profile tab
        self.profile_tab = QWidget()
        self.tab_widget.addTab(self.profile_tab, "Profile")

        # Add widgets to the strategy settings tab
        self.strategy_layout = QGridLayout(self.strategy_tab)

        self.symbol_label = QLabel("Symbol:")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.stop_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.symbol_label.setAlignment(Qt.AlignCenter)
        self.amount_label.setAlignment(Qt.AlignCenter)
        self.profit_price_label.setAlignment(Qt.AlignCenter)
        self.loss_price_label.setAlignment(Qt.AlignCenter)

        self.strategy_layout.addWidget(self.symbol_label, 0, 0)
        self.strategy_layout.addWidget(self.start_button, 4, 0)
        self.strategy_layout.addWidget(self.stop_button, 4, 1)

        self.start_button.clicked.connect(self.startalertMessage)
        self.stop_button.clicked.connect(self.stopbuttonMessage)
        # Add widgets to the order list tab
        self.order_layout = QVBoxLayout(self.order_tab)
        self.order_layout.addWidget(QLabel("Order List"))
        self.order_table = QTableWidget(self)
        self.order_table.setColumnCount(10)
        self.order_table.setRowCount(20)
        self.order_table.setItem(0, 0, QTableWidgetItem("Asset"))
        self.order_table.setItem(0, 1, QTableWidgetItem("Side"))
        self.order_table.setItem(0, 2, QTableWidgetItem("Type"))
        self.order_table.setItem(0, 3, QTableWidgetItem("Source"))
        self.order_table.setItem(0, 4, QTableWidgetItem("Qty"))
        self.order_table.setItem(0, 5, QTableWidgetItem("Filled Qty"))
        self.order_table.setItem(0, 6, QTableWidgetItem("Limit Price"))
        self.order_table.setItem(0, 7, QTableWidgetItem("Stop Price"))
        self.order_table.setItem(0, 8, QTableWidgetItem("Submitted At"))
        self.order_table.setItem(0, 9, QTableWidgetItem("Filled At"))


        self.order_table.horizontalHeader().setStretchLastSection(True) 
        self.order_table.horizontalHeader().setSectionResizeMode( 
            QHeaderView.Stretch) 

        self.order_layout.addWidget(self.order_table)
        # Add widgets to the profile tab
        self.profile_layout = QVBoxLayout(self.profile_tab)
        self.profile_layout.addWidget(QLabel("Profile"))
    def resizeEvent(self, event):
        self.tab_widget.setGeometry(0, 0, self.width(), self.height())
        event.accept()
    def stopbuttonMessage(self):
        global Bot_status
        Bot_status = False
        print("The bot is stoped")
        QMessageBox.information(self, "Alert", "The bot is stoped")
    def startalertMessage(self):
        self.bot_thread = BotThread()
        # Connect the alert signal to a slot that displays the message
        self.bot_thread.alert_signal.connect(self.display_alert_message)
        # Start the bot thread
        self.bot_thread.start()
    def display_alert_message(self, message):
        QMessageBox.information(self, "Alert", message)

    def extract_qdata(self):
        CHUNK_SIZE = 500
        all_orders = []
        start_time = pd.to_datetime('now', utc=True)
        check_for_more_orders = True
        api_orders = api.list_orders(status='all',
                                            until=start_time.isoformat(),
                                            direction='desc',
                                            limit=CHUNK_SIZE,
                                            nested=False,
                                            )

        all_orders.extend(api_orders)
        orders_df = pd.DataFrame([order._raw for order in all_orders])
        orders_df.drop_duplicates('id', inplace=True)
        print("1111111111111111")
        order_data = orders_df.iloc[:, [13, 22, 21, 16, 26, 17, 24, 25, 4, 5, 23]]

        print(order_data.iloc[1, 3])
        print(type(order_data.iloc[1, 1]))
        
        self.order_table.setRowCount(len(order_data.index))
        for i in range(len(order_data.index)):
            for j in range(11):
                # print("table")
                self.order_table.setItem(0, 0, QTableWidgetItem(str(order_data.iloc[i, j])))
        print('end')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())