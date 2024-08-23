from alpaca.trading import TradingClient, MarketOrderRequest, OrderSide, TimeInForce

client = TradingClient('PKH98HD6M9O7OBQE107O','EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4')

current_price = 35603.721 
profit_target_percentage = 0.05  # 5%
stop_loss_percentage = 0.03  # 3%
take_profit_price = current_price * (1 + profit_target_percentage)
stop_loss_price = current_price * (1 - stop_loss_percentage)

order_params = MarketOrderRequest(
symbol='BTC/USD',
side=OrderSide.BUY,
qty=0.400,
time_in_force=TimeInForce.GTC,
stop_price=stop_loss_price,
limit_price=stop_loss_price

)

order = client.submit_order(order_params)