import requests
import json
from apis.api_keys import FINNHUB_API_KEY

def get_realtime_stock_data(symbol):
    # endpoint for real-time price data
    # documentation: https://finnhub.io/docs/api/quote
    URL = "https://finnhub.io/api/v1/quote"
  
    # params for request
    PARAMS = {
        'symbol': symbol,
        'token': FINNHUB_API_KEY
    }
  
    # send GET request
    response = requests.get(url = URL, params = PARAMS)
  
    # return parsed json
    return json.dumps(response.json(), indent=4)


# example w/ AAPL
# res = get_realtime_stock_data("AAPL")
# print(res)

# res = get_realtime_stock_data("AAPL")
# print(res)

# example res
# {
#     "c": 162.36,
#     "d": 1.59,
#     "dp": 0.989,
#     "h": 162.47,
#     "l": 161.271,
#     "o": 161.53,
#     "pc": 160.77,
#     "t": 1680206404
# }