import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest

# Replace 'your_api_key' and 'your_api_secret' with your actual Alpaca API key and secret
api_key = 'PKH98HD6M9O7OBQE107O'
api_secret = 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4'
base_url = 'https://paper-api.alpaca.markets'  # For the paper trading environment

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Specify the symbol (BTC/USD) and quantity of BTC you want to trade
# symbol = 'BTC/USD'
# quantity = 0.001  # Adjust the quantity as needed
symbol = 'SPY'
quantity = 100  # Adjust the quantity as needed

def last_price(symbol):
    client = CryptoHistoricalDataClient()

    request_params = CryptoLatestQuoteRequest(symbol_or_symbols="BTC/USD")

    latest_quote = client.get_crypto_latest_quote(request_params)

    print(latest_quote[symbol])

    return latest_quote[symbol]


# Get the current market price for BTC/USD
# current_price = 35603.721 
current_price = 500
profit_target_percentage = 0.05  # 5%
stop_loss_percentage = 0.03  # 3%
take_profit_price = current_price * (1 + profit_target_percentage)
stop_loss_price = current_price * (1 - stop_loss_percentage)

# Place a market order with take-profit and stop-loss parameters
order = api.submit_order(
    symbol=symbol,
    qty=quantity,
    side='buy',  # 'buy' for a long position, 'sell' for a short position
    type='market',
    time_in_force='gtc',  # Good 'til canceled
    take_profit={'limit_price': take_profit_price},
    stop_loss={'stop_price': stop_loss_price}
)

# Print the order details
print("Order ID:", order.id)
print("Take Profit Price:", take_profit_price)
print("Stop Loss Price:", stop_loss_price)