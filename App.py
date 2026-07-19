import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from services.sentiment_services import analyze_sentiment

from services.stock_services import (
    get_stock_info,
    get_stock_history,
)

from services.news_services import get_company_news


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Financial Research AI",
    layout="wide",
)

st.title("Financial Research AI Agent")


# --------------------------------------------------
# User Inputs
# --------------------------------------------------

st.markdown("""Analyze stocks, market trends, company fundamentals and financial news using AI-powered insights""")

col1, col2 = st.columns(2)

with col1:
    symbol1 = st.text_input(
        "Stock 1",
        value="RELIANCE.NS"
    )

with col2:
    symbol2 = st.text_input(
        "Stock 2",
        value="TCS.NS"
    )

period = st.selectbox(
    "Select Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
    ],
)


# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

if st.button("Analyze Stock"):

    # ==========================================
    # Company Information
    # ==========================================

    data = get_stock_info(symbol1)
    data2 = get_stock_info(symbol2)

    st.subheader("🏢 Company Information")
    st.write(data)

    with col2:
        st.markdown(f"### {symbol2}")
        st.write(data2)

    # ==========================================
    # Comparison Table
    # ==========================================

    st.subheader(" Stock Comparison")

    comparison_data = {
        "Metric": [
            "Current Price",
            "Open",
            "High",
            "Low",
            "Previous Close",
            "Volume",
            "Market Cap",
        ],
        symbol1: [
            data["Current Price"],
            data["Open"],
            data["High"],
            data["Low"],
            data["Previous Close"],
            data["Volume"],
            data["Market Cap"],
        ],
        symbol2: [
            data2["Current Price"],
            data2["Open"],
            data2["High"],
            data2["Low"],
            data2["Previous Close"],
            data2["Volume"],
            data2["Market Cap"],
        ],
    }

    st.table(comparison_data)

    # ==========================================
    # Quick Comparison
    # ==========================================

    st.subheader(" Quick Comparison")

    change1 = data["Current Price"] - data["Previous Close"]
    change2 = data2["Current Price"] - data2["Previous Close"]

    if change1 > change2:

        st.success(
            f" Better Performer Today: {symbol1}"
        )

        st.write(f"Today's Gain: ₹{change1:.2f}")

    elif change2 > change1:

        st.success(
            f" Better Performer Today: {symbol2}"
        )

        st.write(f"Today's Gain: ₹{change2:.2f}")

    else:

        st.info(" Both stocks performed equally today.")

    
# ==========================================
# Stock Price Chart
# ==========================================

history = get_stock_history(symbol1, period)
history2 = get_stock_history(symbol2, period)

if (
    history is not None
    and not history.empty
    and history2 is not None
    and not history2.empty
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["Close"],
            mode="lines",
            name=symbol1,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history2.index,
            y=history2["Close"],
            mode="lines",
            name=symbol2,
        )
    )

    fig.update_layout(
        title=f"{symbol1} vs {symbol2} Closing Price",
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        template="plotly_white",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

else:
    st.error("Unable to fetch stock history.")

    # ==========================================
    # Latest News
    # ==========================================

    st.subheader("Latest News")

    company_name = data.get("Company")



    # ------ NEWS MODEL ------
    # This section fetches recent company-related news articles 
    # Using News API and displays them inside Streamlit

    if company_name:

        st.write(f"Searching News For: **{company_name}**")

        news = get_company_news(company_name)

        if news:

            st.success(f"Found {len(news)} Articles")

            for article in news:

                st.markdown(f"### {article['title']}")

                if article.get("description"):
                    st.write(article["description"])

                # ---------------- Sentiment Analysis ----------------

                headline = article["title"]

                if article.get("description"):
                    headline += " " + article["description"]

                sentiment, score = analyze_sentiment(headline)

                if sentiment == "Positive":
                    st.success(f" Sentiment: {sentiment} ({score:.2f})")

                elif sentiment == "Negative":
                    st.error(f"Sentiment: {sentiment} ({score:.2f})")

                else:
                    st.info(f" Sentiment: {sentiment} ({score:.2f})")

                if article.get("source"):
                    st.caption(f" Source: {article['source']}")

                if article.get("publishedAt"):
                    st.caption(
                        f" Published: {article['publishedAt'][:10]}"
                    )

                if article.get("url"):
                    st.link_button(
                        " Read Full Article",
                        article["url"],
                    )

                st.divider()

        else:
            st.warning("No news found.")


    else:
        st.error("Company name not found.")