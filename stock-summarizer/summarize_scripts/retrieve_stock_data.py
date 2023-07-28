import pandas as pd
import yfinance as yf

def stock_data(name):
    data = yf.download(name, period="max", interval="1d")

    data = data.to_dict("index")

    filter_data = []
    
    for date in data:
        dict = {}
        dict["Date"] = date.strftime('%Y-%m-%d')
        dict["Close"] = data[date]["Close"]
        filter_data.append(dict)

    return filter_data