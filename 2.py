import alpaca_trade_api as tradeapi
# from alpaca_trade_api.common import BarTimeFrame
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest


from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import LimitOrderRequest

# to which url we will send request
base_url="https://paper-api.alpaca.markets"

# instantiate REST API
api = tradeapi.REST('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', base_url, api_version='v2')

# obtain account information
# account = api.get_account()
# print(account)

# active_assets=api.list_assets(status='active')
# for asset in active_assets:
#   print(asset)
#   break

# symbols = ["TSLA", "AAPL"]
# # resp = api.get_bars(symbols,timeframe='1Min', start="2022-04-30", end="2022-05-30",limit=10000)
# resp = api.get_bars(symbols, timeframe=TimeFrame.Day, start=datetime(2022, 7, 1),
#                         end=datetime(2022, 9, 1), limit=10000)
# resp.df.reset_index()


client = CryptoHistoricalDataClient()

request_params = CryptoBarsRequest(
                        symbol_or_symbols=["BTC/USD", "ETH/USD"],
                        timeframe=TimeFrame.Day,
                        start=datetime(2022, 7, 1),
                        end=datetime(2022, 7, 25)
                 )

bars = client.get_crypto_bars(request_params)

# # convert to dataframe
# bars.df

# # access bars as list - important to note that you must access by symbol key
# # even for a single symbol request - models are agnostic to number of symbols
print(bars["BTC/USD"])


# trading_client = TradingClient('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', paper=True)


# from alpaca.data.historical import CryptoHistoricalDataClient
# from alpaca.data.requests import CryptoLatestQuoteRequest

# # no keys required
# client = CryptoHistoricalDataClient()

# # single symbol request
# request_params = CryptoLatestQuoteRequest(symbol_or_symbols="BTC/USD")

# latest_quote = client.get_crypto_latest_quote(request_params)

# # must use symbol to access even though it is single symbol
# print(latest_quote["BTC/USD"])

# must use symbol to access even though it is single symbol


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

# limit_order_data = LimitOrderRequest(
#                     symbol="BTC/USD",
#                     limit_price=10000,
#                     notional=10000,
#                     side=OrderSide.BUY,
#                     time_in_force=TimeInForce.IOC
#                    )

# # Limit order
# limit_order = trading_client.submit_order(
#                 order_data=limit_order_data
#               )