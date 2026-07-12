import yfinance as yf


def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info

    return {
        "Company": info.get("longName"),
        "Current Price": info.get("currentPrice"),
        "Open": info.get("open"),
        "High": info.get("dayHigh"),
        "Low": info.get("dayLow"),
        "Previous Close": info.get("previousClose"),
        "Volume": info.get("volume"),
        "Market Cap": info.get("marketCap")
    }



def get_stock_history(symbol, period="6mo"):
    stock = yf.Ticker(symbol)
    history = stock.history(period=period)
    return history