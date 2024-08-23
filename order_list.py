import alpaca_trade_api as alpacaapi
import pandas as pd
ALPACA_API_ENDPOINT_PAPER = 'https://paper-api.alpaca.markets'
YOUR_API_KEY_ID = "PKH98HD6M9O7OBQE107O"
YOUR_API_SECRET_KEY = "EjxanHRx46ihNeN643WMaODU8oCE5D1ZRJ4dVVJ4"
 
api = alpacaapi.REST(YOUR_API_KEY_ID, YOUR_API_SECRET_KEY, ALPACA_API_ENDPOINT_PAPER)
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
# selected_cols = ['side', 'type', 'qty']
# orders_df = orders_df[selected_cols]
# print(orders_df["side"])
order_data = orders_df.iloc[:, [13, 22, 21, 16, 26, 17, 24, 25, 4, 5, 23]]

print(order_data.iloc[1, 3])
print(type(order_data.iloc[1, 1]))

print(order_data)

print(len(order_data.index))

# for i in range(len(order_data.index)):
#     for j in range(11):
#         print("table")