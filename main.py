import alpaca_trade_api as tradeapi
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from alpaca.data.requests import CryptoBarsRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import LimitOrderRequest
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest
import datetime

base_url="https://paper-api.alpaca.markets"

api = tradeapi.REST('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', base_url, api_version='v2')
trading_client = TradingClient('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', paper=True)


account = api.get_account()

active_assets=api.list_assets(status='active')
# for asset in active_assets:
#   print(asset)
#   break

def last_price(sysmbol):
    client = CryptoHistoricalDataClient()

    request_params = CryptoLatestQuoteRequest(symbol_or_symbols="BTC/USD")

    latest_quote = client.get_crypto_latest_quote(request_params)

    # must use symbol to access even though it is single symbol
    print(latest_quote["BTC/USD"])

    return latest_quote["BTC/USD"]

def get_histrical(start, end):
    # start_year = int(start.year)
    # start_month = int(start.month)
    # start_day = int(start.day)
    # end_year = int(end.year)
    # end_month = int(end.month)
    # end_day = int(end.day)
    # client = CryptoHistoricalDataClient()
    # request_params = CryptoBarsRequest(
    #                         symbol_or_symbols=["BTC/USD", "ETH/USD"],
    #                         timeframe=TimeFrame.Day,
    #                         start=datetime(2022, 7, 1),
    #                         end=datetime(2022, 7, 25)
    #                  )
    client = CryptoHistoricalDataClient()

    request_params = CryptoBarsRequest(
                            symbol_or_symbols=["BTC/USD", "ETH/USD"],
                            timeframe=TimeFrame.Day,
                            start=datetime(2022, 7, 1),
                            end=datetime(2022, 7, 25)
                    )

    bars = client.get_crypto_bars(request_params)

    print("111111111111list")
    print(bars)
    return bars

def calculate_MN(historical_data, window_size):
    window_size = 3

# Retrieve the closing prices from the historical data
    closing_prices = [data['close'] for data in historical_data]

    # Calculate the Moving Average
    moving_average = sum(closing_prices[-window_size:]) / window_size

    return ""

def get_MN_25():
    current_date = datetime.date.today()
    previous_date_25 = current_date - datetime.timedelta(days=25)

    window_size = 25
    historical_data = get_histrical(previous_date_25, current_date)
    mn = calculate_MN(historical_data, window_size)
    print("MN: ", mn)
    return mn

def get_MN_75():
    current_date = datetime.date.today()
    previous_date_75 = current_date - datetime.timedelta(days=75)
    get_histrical(previous_date_75, current_date)
    return "123"

def order(sysmbol, under, upper):
    # preparing orders
    # market_order_data = MarketOrderRequest(
    #                     symbol="BTC/USD",
    #                     qty=1,
    #                     side=OrderSide.BUY,
    #                     time_in_force=TimeInForce.DAY
    #                     )

    # # Market order
    # market_order = trading_client.submit_order(
    #                 order_data=market_order_data
    #                )

    limit_order_data = LimitOrderRequest(
                        symbol="BTC/USD",
                        limit_price=10000,
                        notional=10000,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.IOC
                       )

    # Limit order
    limit_order = trading_client.submit_order(
                    order_data=limit_order_data
                  )
    return "123"

def main():
    num = get_MN_25()
    print(num)
    print("123")


if __name__ == "__main__":
    main()



