import streamlit as st
import yfinance as yf

@st.cache_data(ttl=300)
def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info

    return {
        "Company": info.get("longName"),
        "Sector": info.get("sector"),
        "Industry": info.get("industry"),
        "Current Price": info.get("currentPrice"),
        "Open": info.get("open"),
        "High": info.get("dayHigh"),
        "Low": info.get("dayLow"),
        "Previous Close": info.get("previousClose"),
        "Volume": info.get("volume"),
        "Market Cap": info.get("marketCap")
    }


@st.cache_data(ttl=300)
def get_stock_history(symbol, period="6mo"):
    stock = yf.Ticker(symbol)
    history = stock.history(period=period)
    history["MA20"] = history["Close"].rolling(window=20).mean()
    history["MA50"] = history["Close"].rolling(window=50).mean()
    history["RSI"] = calculate_rsi(history)
    return history

def calculate_rsi(data, period=14):

    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi