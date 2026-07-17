import streamlit as st
import plotly.graph_objects as go
import yfinance as yf

from services.stock_services import (
    get_stock_info,
    get_stock_history
)

# Import News Function
from services.news_services import (
    get_company_news
)

st.set_page_config(
    page_title="Financial Research AI",
    layout="wide"
)

st.title(" Financial Research AI Agent")

st.markdown("""Analyze stocks, market trends, company fundamentals and financial news using AI-powered insights""")

symbol = st.text_input(
    "Enter Stock Symbol",
    "RELIANCE.NS"
)

period = st.selectbox(
    "Select Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y"
    ]
)

if st.button("Analyze Stock"):

    data = get_stock_info(symbol)


    # ----- COMPANY OVERVIEW -----
    st.subheader("Company Information")

    company_name = data.get("Company")
    sector = data.get("Sector")
    industry = data.get("Industry")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"{company_name}")
    
    with col2:
        st.info(f"{sector}" if sector else "Sector Not Available")

    with col3:
        st.info(f"{industry}" if industry else "Industry Not Available")


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Price", data.get("Current Price"))

        st.metric("Open", data.get("Open"))

    with col2:
        st.metric("High", data.get("High"))

        st.metric("Low", data.get("Low"))

    with col3:
        st.metric("Volume", data.get("Volume"))

        st.metric("Previous Close", data.get("Previous Close"))

    market_cap = data.get("Market Cap")

    if market_cap:
        st.info(
            f"Market Cap: ₹{market_cap/1000000000000:.2f} Trillion"
        )
    else:
        st.info("Market Cap: Not Available")



    # ----------- FINANCIAL HEALTH SCORE -----------
    # Evaluates stock fundamentals using 
    # 1. P/E Ratio
    # 2. Market Cap
    # NOTE : Higher score indicates stronger fundamentals based on valuation and company size

    score = 0

    market_cap = data.get("Market Cap")

    stock = yf.Ticker(symbol)
    info = stock.info

    pe_ratio = info.get("trailingPE")

    recommendation = "N/A"

    if pe_ratio:
        if pe_ratio < 20:
            score += 40
            recommendation = "BUY"
        elif pe_ratio < 35:
            score += 25
            recommendation = "HOLD"
        else:
            score += 10
            recommendation = "SELL"

    if market_cap:
        if market_cap > 1000000000000:  # > 1 Trillion
            score += 30
        elif market_cap > 500000000000:  # > 500 Billion
            score += 20
        else:
            score += 10

    st.markdown("---")
    st.subheader("Financial Health Score")
    
    st.progress(score)
    st.success(f"Financial Health Score: {score}/100")

    # ------------ INVESTMENT RECOMMENDATION ENGINE -------------

    st.subheader("Investment Recommendation")

    if recommendation == "BUY":
        st.success("🟢 BUY")
    elif recommendation == "HOLD":
        st.warning("🟡 HOLD")
    elif recommendation == "SELL":
        st.error("🔴 SELL")

    



    history = get_stock_history(symbol, period)

    if history is None or history.empty:
        st.error("No data found for the selected Symbol")
        st.stop()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["Close"],
            mode="lines",
            name="Closing Price"
        )
    )

    fig.update_layout(
        title=f"{symbol} Closing Price",
        xaxis_title="Date",
        yaxis_title="Price (₹)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    company_name = data.get("Company")


    # ------ NEWS MODEL ------
    # This section fetches recent company-related news articles 
    # Using Google News RSS feed and displays them inside Streamlit

    st.subheader("Latest News")


    # NOTE :
    # Previously this block was commented out, which caused the application to display only the "Latest News" heading without fetching any news articles


    if company_name:

        news = get_company_news(company_name)

        st.write(f"Searching News For: {company_name}")
        st.write(f"Articles Found: {len(news)}")

        if news:

            for article in news:

                st.markdown(f"### {article.get('title')}")

                # Display article summary only if available 
                # if article.get("description"):
                #    st.caption(article["description"][:200] + "...")

                if article.get("url"):
                   st.link_button("Read Full Article", article["url"])

                st.write("---")

        else:

            st.warning("No News Found")

    else:

        st.error("Company name not found.")

       