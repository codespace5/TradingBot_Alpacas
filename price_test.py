import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTabWidget, QGridLayout, QSizePolicy, QComboBox, QMessageBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import alpaca_trade_api as tradeapi
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from alpaca.data.requests import CryptoBarsRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import StopOrderRequest, StopLimitOrderRequest
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest
import datetime
import pandas as pd
from alpaca.trading.enums import OrderSide
import requests

base_url="https://paper-api.alpaca.markets"

api = tradeapi.REST('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', base_url, api_version='v2')
trading_client = TradingClient('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', paper=True)
openai_key = "sssssssssssssssssssssssggggggggggggggyk4TIBiKckoessct" "yhU5T3BlbkFJz68IXN6mOfDhFkAXGkG3"
account = api.get_account()
active_assets=api.list_assets(status='active')
Bot_status = True
quantity = 0.0134
symbol = "BTC/USD"
strategy = ""
stop_loss = 123
limit = 123
class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.resize(300, 150)
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
        self.resize(600, 400)
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(0, 0, self.width(), self.height())
        self.strategy_tab = QWidget()
        self.tab_widget.addTab(self.strategy_tab, "Strategy Settings")
        self.strategy_layout = QGridLayout(self.strategy_tab)

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.stop_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.strategy_layout.addWidget(self.start_button, 4, 0)
        self.strategy_layout.addWidget(self.stop_button, 4, 1)
        self.start_button.clicked.connect(self.startalertMessage)

        # Add widgets to the order list tab
        self.order_layout = QVBoxLayout(self.order_tab)
        self.order_layout.addWidget(QLabel("Order List"))

        # Add widgets to the profile tab
        self.profile_layout = QVBoxLayout(self.profile_tab)
        self.profile_layout.addWidget(QLabel("Profile"))

    def resizeEvent(self, event):
        self.tab_widget.setGeometry(0, 0, self.width(), self.height())
        event.accept()
    def startalertMessage(self):
        QMessageBox.information(self, "Alert", "The bot is started")
        global Bot_status
        global quantity
        global symbol
        global limit
        global stop_loss
        global strategy
        while(Bot_status):
            ma_25days, price25_list  = get_MN_25()
            # ma_75days, price75_list = get_MN_75()
            current_price = last_price("BTC/USD")
            print(current_price)
            buy_price = current_price.ask_price
            # print("current pirce:", buy_price)

            order(buy_price)
def order(price):
    stop_loss_pct = 0.03  # Stop loss percentage
    take_profit_pct = 0.05  # Take profit percentage
    trade_duration = pd.Timedelta(hours=1)  # Maximum trade duration

    stop_loss_price = price * (1 - stop_loss_pct)
    take_profit_price = price * (1 + take_profit_pct)
    stop_order_id = StopOrderRequest(
        symbol=symbol,
        qty=0.0134,
        side=OrderSide.SELL,
        type='stop',
        time_in_force='gtc',
        stop_price = stop_loss_price
    )
    print(stop_order_id)


def last_price(symbol):
    client = CryptoHistoricalDataClient()
    request_params = CryptoLatestQuoteRequest(symbol_or_symbols="BTC/USD")

    latest_quote = client.get_crypto_latest_quote(request_params)
    return latest_quote[symbol]

def get_historical(start, end):
    client = CryptoHistoricalDataClient()

    request_params = CryptoBarsRequest(
        symbol_or_symbols=["BTC/USD"],
        timeframe=TimeFrame.Hour,
        start=start,
        end=end
    )
    bars = client.get_crypto_bars(request_params)
    return bars['BTC/USD']

def get_historical_day(start, end):
    client = CryptoHistoricalDataClient()

    request_params = CryptoBarsRequest(
        symbol_or_symbols=["BTC/USD"],
        timeframe=TimeFrame.Day,
        start=start,
        end=end
    )

    bars = client.get_crypto_bars(request_params)

    return bars['BTC/USD']

def get_MN_25():
    current_date = datetime.date.today()
    previous_date_25 = current_date - datetime.timedelta(hours=600)

    window_size = 10
    historical_data = get_historical(previous_date_25, current_date)
    close_prices = [bar.close for bar in historical_data]
    df = pd.DataFrame(close_prices, columns=['Close'])
    sma = df['Close'].rolling(window=600).mean()
    sma_value = sma.values[-1]
    previous_25days = current_date - datetime.timedelta(days=25)
    historial_25days = get_historical_day(previous_25days, current_date)
    price_values = [bar.close  for bar in historial_25days]
    
    return sma_value, price_values


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())