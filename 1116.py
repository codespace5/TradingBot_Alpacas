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
openai.api_key = "wwwwwwwwwwsgggggggggk-yk4TIBiKckoessctyh" "U5T3BlbkFJz68IXN6mOfDhFkAXGkG3"
api = tradeapi.REST('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', base_url, api_version='v2')
trading_client = TradingClient('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', paper=True)
openai_key = "wwwwwwwwwwwwwwwwwwwwwsggggggk-yk4TIBiKckoessctyhU5T3" "BlbkFJz68IXN6mOfDhFkAXGkG3"

account = api.get_account()

active_assets=api.list_assets(status='active')


Bot_status = True
quantity = 0.0134
symbol = "BTC/USD"
strategy = ""
stop_loss = 123
limit = 123


class BotThread(QThread):
    alert_signal = pyqtSignal(str)

    def run(self):
        global quantity
        global symbol
        global limit
        global stop_loss
        global strategy
        ma_25days = 0
        ma_75days = 0
        last_ma25days = 0
        last_ma75days = 0
        i = 0

        current_price = last_price("BTC/USD")
        buy_price = current_price.ask_price
        order(buy_price)
        print("Buy Order")
        while Bot_status:
            ma_25days, price25_list  = get_MN_25()
            ma_75days, price75_list = get_MN_75()
            current_price = last_price("BTC/USD")
            # print(current_price)
            buy_price = current_price.ask_price
            # print("current pirce:", buy_price)

            # order(buy_price)
            # print("25 days for last and ma: ",last_ma25days,  ma_25days)
            # print("The price list for 25 days:", price25_list)
            
            # print("75 days for last and ma: ", last_ma75days,  ma_75days)
            # print("the price list for 75 days: ", price75_list)


            prompt = str(symbol) + " data is as follows: \n" + str(current_price) +"\n" + "MA25 is" + str(ma_25days) + "\n MA75 is" + str(ma_75days) + "\n" +"the price values for 25 days:\n" + str(price25_list) + "\n" +"the price values for 75 days:" + str(price75_list) + "\n" +"Please analyze MA25 and MA75 and let me know if I can make money if I buy BTC/USD now. Which is better: buy or hold?Answer the only one word."
            print(prompt)
            res = chat_with_chatgpt(prompt)
            if res == "Buy":
                # order(buy_price)
                print("buy")
            elif res == "Hold":
                print("Hold")
            elif res == "Sold":
                print("Sold")
            if ma_25days > ma_75days and last_ma25days <= last_ma75days and last_ma25days != 0:
                print("BUY ORDER")
                order(buy_price)
            # print("2222")

            last_ma25days = ma_25days
            last_ma75days = ma_75days



            # Emit a signal to display the alert message
            # self.alert_signal.emit("The bot is started")



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
        self.resize(600, 400)

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
        # self.symbol_input = QLineEdit()
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItems(['BTC/USD', 'ETH/USD', 'LTC/USD'])

        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
        self.amount_input.setText("0.0134")

        self.profit_price_label = QLabel("Profit Price:")
        self.profit_price_input = QLineEdit()
        self.profit_price_input.setText("5")

        self.loss_price_label = QLabel("Loss Price:")
        self.loss_price_input = QLineEdit()
        self.loss_price_input.setText("3")

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.stop_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.symbol_label.setAlignment(Qt.AlignCenter)
        self.amount_label.setAlignment(Qt.AlignCenter)
        self.profit_price_label.setAlignment(Qt.AlignCenter)
        self.loss_price_label.setAlignment(Qt.AlignCenter)

        self.strategy_layout.addWidget(self.symbol_label, 0, 0)
        self.strategy_layout.addWidget(self.symbol_combo, 0, 1)
        self.strategy_layout.addWidget(self.amount_label, 1, 0)
        self.strategy_layout.addWidget(self.amount_input, 1, 1)
        self.strategy_layout.addWidget(self.profit_price_label, 2, 0)
        self.strategy_layout.addWidget(self.profit_price_input, 2, 1)
        self.strategy_layout.addWidget(self.loss_price_label, 3, 0)
        self.strategy_layout.addWidget(self.loss_price_input, 3, 1)
        self.strategy_layout.addWidget(self.start_button, 4, 0)
        self.strategy_layout.addWidget(self.stop_button, 4, 1)

        self.start_button.clicked.connect(self.startalertMessage)
        self.stop_button.clicked.connect(self.stopbuttonMessage)
        # Add widgets to the order list tab
        self.order_layout = QVBoxLayout(self.order_tab)
        self.order_layout.addWidget(QLabel("Order List"))

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
        global Bot_status
        global quantity
        global symbol
        global limit
        global stop_loss
        global strategy
        Bot_status = True

        quantity = float(self.amount_input.text())
        symbol = self.symbol_combo.currentText()
        stop_loss = float(self.loss_price_input.text())
        limit = float(self.profit_price_input.text())

        self.bot_thread = BotThread()
        # Connect the alert signal to a slot that displays the message
        self.bot_thread.alert_signal.connect(self.display_alert_message)
        # Start the bot thread
        self.bot_thread.start()
    def display_alert_message(self, message):
        QMessageBox.information(self, "Alert", message)

def order(price):
    stop_loss_pct = 0.03  # Stop loss percentage
    take_profit_pct = 0.05  # Take profit percentage
    trade_duration = pd.Timedelta(hours=1)  # Maximum trade duration

    stop_loss_price = price * (1 - stop_loss_pct)
    take_profit_price = price * (1 + take_profit_pct)

    expiration_time = datetime.date.today() + trade_duration

    api.submit_order(
        symbol='BTCUSD',
        qty=0.0134,  # Set the quantity as per your requirement
        side='buy',
        type='market',
        time_in_force='gtc'  # Good 'til cancelled
    )

    # Place the stop loss order
    # Place the take profit order
    api.submit_order(
        symbol='BTCUSD',
        qty=0.0134,
        side='sell',
        type='limit',
        time_in_force='gtc',
        limit_price=take_profit_price
    )

    api.submit_order(
        symbol='BTCUSD',
        qty=0.0134,
        side='sell',
        type='stop_limit',
        time_in_force='gtc',
        stop_price=stop_loss_price,
        limit_price=stop_loss_price  # Set the limit price equal to the stop price to trigger a market order
    )
# cancel_time = datetime.now() + trade_duration
# api.cancel_order(buy_order.id)
# api.cancel_order(stop_loss_order.id)
# api.cancel_order(take_profit_order.id)

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

    # print(latest_quote[symbol])

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

    # print("Historical Data:")
    # print(bars)

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
    # print(historical_data)

    # Extract the 'close' prices from the historical data
    close_prices = [bar.close for bar in historical_data]

    # Create a DataFrame with the close prices
    df = pd.DataFrame(close_prices, columns=['Close'])

    # Calculate the SMA using the rolling window
    sma = df['Close'].rolling(window=600).mean()
    # print(sma)
    sma_value = sma.values[-1]
    # print(sma_value)

    previous_25days = current_date - datetime.timedelta(days=25)
    historial_25days = get_historical_day(previous_25days, current_date)
    price_values = [bar.close  for bar in historial_25days]
    
    return sma_value, price_values

def get_MN_75():
    current_date = datetime.date.today()
    previous_date_25 = current_date - datetime.timedelta(hours=1800)

    window_size = 10
    historical_data = get_historical(previous_date_25, current_date)
    # print(historical_data)

    # Extract the 'close' prices from the historical data
    close_prices = [bar.close for bar in historical_data]

    # Create a DataFrame with the close prices
    df = pd.DataFrame(close_prices, columns=['Close'])

    # Calculate the SMA using the rolling window
    sma = df['Close'].rolling(window=1800).mean()
    # print(sma)
    sma_value = sma.values[-1]
    # print(sma_value)
    previous_75days = current_date - datetime.timedelta(days=75)
    historial_75days = get_historical_day(previous_75days, current_date)
    price_values = [bar.close  for bar in historial_75days]

    return sma_value, price_values

def chat_with_chatgpt(prompt):

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=1,
    )  
    answer = response.choices[0].text.strip()
    return answer        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())