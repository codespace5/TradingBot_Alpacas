
import alpaca_trade_api as tradeapi
from alpaca.trading.client import TradingClient
base_url="https://paper-api.alpaca.markets"
api = tradeapi.REST('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', base_url, api_version='v2')
trading_client = TradingClient('PKH98HD6M9O7OBQE107O', 'EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4', paper=True)
openai_key = "eeeeeeeeeeeeeeeee-yk4TIBiKckoessctyhU5T" "3BlbkFJz68IXN6mOfDhFkAXGkG3"

account = api.get_account()
print(account)
active_assets=api.get_asset("BTC/USD")
print(active_assets)
# api.cancel_all_orders()
# account = trading_client.get_account()

# # Check our current balance vs. our balance at the last market close
# balance_change = float(account.equity) - float(account.last_equity)
# print(f'Today\'s portfolio balance change: ${balance_change}')

# balance = account.equity
# print("balance", balance)