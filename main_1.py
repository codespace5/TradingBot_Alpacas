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

def last_price(symbol):
    client = CryptoHistoricalDataClient()

    request_params = CryptoLatestQuoteRequest(symbol_or_symbols="BTC/USD")

    latest_quote = client.get_crypto_latest_quote(request_params)

    print(latest_quote[symbol])

    return latest_quote[symbol]

def get_historical(start, end):
    client = CryptoHistoricalDataClient()

    request_params = CryptoBarsRequest(
        symbol_or_symbols=["BTC/USD"],
        timeframe=TimeFrame.Day,
        start=start,
        end=end
    )

    bars = client.get_crypto_bars(request_params)

    print("Historical Data:")
    # print(bars)

    return bars['BTC/USD']

def calculate_sum_close(historical_data, window_size):
    print(historical_data)
    close_sum = sum(item.close for item in historical_data)
    mn = (close_sum/window_size)
    print("MN of 'close':", mn)
    return mn

def get_MN_25():
    current_date = datetime.date.today()
    previous_date_25 = current_date - datetime.timedelta(days=3)

    window_size = 3
    historical_data = get_historical(previous_date_25, current_date)
    mn = calculate_sum_close(historical_data, window_size)
    print("MN: ", mn)
    return mn

def get_MN_75():
    current_date = datetime.date.today()
    previous_date_25 = current_date - datetime.timedelta(days=75)

    window_size = 3
    historical_data = get_historical(previous_date_25, current_date)
    mn = calculate_sum_close(historical_data, window_size)
    print("MN: ", mn)
    return mn

def order(symbol, lower, upper):
    limit_order_data = LimitOrderRequest(
        symbol="BTC/USD",
        limit_price=10000,
        notional=10000,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.IOC
    )

    limit_order = trading_client.submit_order(
        order_data=limit_order_data
    )
    return "123"

def main():
    # num = get_MN_25()
    # print(num)
    # print("123")

    # Submit the OCO order
    # response = api.submit_order(
    #     symbol=symbol,
    #     qty=qty,
    #     side='buy',
    #     time_in_force='gtc',
    #     order_class='oco',
    #     take_profit=dict(
    #         limit_price=limit_price
    #     ),
    #     stop_loss=dict(
    #         stop_price=stop_price
    #     )
    # )


    # Submit the OCO order
    # response = api.submit_order(
    #     symbol=symbol,
    #     qty=qty,
    #     side='sell',
    #     type='limit',
    #     time_in_force='day',
    #     order_class='oco',
    #     take_profit=dict(
    #         limit_price=limit_price
    #     ),
    #     stop_loss=dict(
    #         stop_price=stop_price,
    #         # limit_price=stop_limit_price
    #     )
    # )

    price = last_price('BTC/USD')
    print(print)
    current_price = 35603.721  # Replace with the actual current price

# Define the profit target and stop-loss levels as percentages
    profit_target_percentage = 0.05  # 5%
    stop_loss_percentage = 0.03  # 3%
    
    response = api.submit_order(
        symbol='BTC/USD',
        qty=100,
        side='buy',
        type='market',
        time_in_force='gtc',
        order_class='bracket',
        take_profit=dict(
            limit_price=current_price * (1 + profit_target_percentage)
        ),
        stop_loss=dict(
            stop_price=current_price * (1 - stop_loss_percentage),
            # limit_price=stop_limit_price
        )
)


# Print the order details
    print(response)


if __name__ == "__main__":
    main()