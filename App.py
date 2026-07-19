import streamlit as st
import plotly.graph_objects as go

from services.stock_services import (
    get_stock_info,
    get_stock_history,
)

from services.news_services import get_company_news
from services.sentiment_services import analyze_sentiment
from services.ai_services import generate_stock_analysis



# Page Configuration


st.set_page_config(
    page_title="Financial Research AI",
    layout="wide",
)

st.title("Financial Research AI Agent")

st.markdown(
    """
Analyze stocks, market trends, company fundamentals and financial news using AI-powered insights.
"""
)


# User Inputs

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



# Analyze Button


if st.button("Analyze Stock"):

    # Fetch Stock Data

    data = get_stock_info(symbol1)
    data2 = get_stock_info(symbol2)

    history = get_stock_history(symbol1, period)
    history2 = get_stock_history(symbol2, period)

    
    # Company Information

    st.subheader(" Company Information")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### {symbol1}")
        st.write(data)

    with col2:
        st.markdown(f"### {symbol2}")
        st.write(data2)

   
    # Stock Comparison

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

    
    # Quick Comparison
    
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
        st.info("Both stocks performed equally today.")


    # Stock Price Chart

    if (
        history is not None
        and not history.empty
        and history2 is not None
        and not history2.empty
    ):

        st.subheader(" Stock Price Comparison")

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

        
        # RSI Chart

        st.subheader(" Relative Strength Index (RSI)")

        rsi_fig = go.Figure()

        rsi_fig.add_trace(
            go.Scatter(
                x=history.index,
                y=history["RSI"],
                mode="lines",
                name=f"{symbol1} RSI",
            )
        )

        rsi_fig.add_trace(
            go.Scatter(
                x=history2.index,
                y=history2["RSI"],
                mode="lines",
                name=f"{symbol2} RSI",
            )
        )

        rsi_fig.add_hline(
            y=70,
            line_dash="dash",
            annotation_text="Overbought (70)",
        )

        rsi_fig.add_hline(
            y=30,
            line_dash="dash",
            annotation_text="Oversold (30)",
        )

        rsi_fig.update_layout(
            title="14-Day RSI Comparison",
            xaxis_title="Date",
            yaxis_title="RSI",
            template="plotly_white",
        )

        st.plotly_chart(
            rsi_fig,
            use_container_width=True,
        )

    else:
        st.error("Unable to fetch stock history.")

 
    # Latest News

    st.subheader("Latest News")

    company_name = data.get("Company")

    if company_name:

        st.write(f"Searching News For: **{company_name}**")

        news = get_company_news(company_name)

        if news:

            st.success(f"Found {len(news)} Articles")

            for article in news:

                st.markdown(f"### {article['title']}")

                if article.get("description"):
                    st.write(article["description"])

                headline = article["title"]

                if article.get("description"):
                    headline += " " + article["description"]

                sentiment, score = analyze_sentiment(headline)

                if sentiment == "Positive":
                    st.success(
                        f" Sentiment: {sentiment} ({score:.2f})"
                    )

                elif sentiment == "Negative":
                    st.error(
                        f" Sentiment: {sentiment} ({score:.2f})"
                    )

                else:
                    st.info(
                        f" Sentiment: {sentiment} ({score:.2f})"
                    )

                if article.get("source"):
                    st.caption(
                        f" Source: {article['source']}"
                    )

                if article.get("publishedAt"):
                    st.caption(
                        f"Published: {article['publishedAt'][:10]}"
                    )

                if article.get("url"):
                    st.link_button(
                        "Read Full Article",
                        article["url"],
                    )

                st.divider()

        else:
            st.warning("No news found.")

    else:
        st.error("Company name not found.")
    

    # AI Financial Analysis
   
    st.subheader(" AI Financial Analysis")

    if (
        history is not None
        and not history.empty
        and "RSI" in history.columns
    ):

        prompt = f"""
You are a professional financial analyst.

Analyze the following stock in simple language.

Company: {data["Company"]}

Current Price: {data["Current Price"]}
Open: {data["Open"]}
High: {data["High"]}
Low: {data["Low"]}
Previous Close: {data["Previous Close"]}
Volume: {data["Volume"]}
Market Cap: {data["Market Cap"]}

Current RSI: {history["RSI"].iloc[-1]:.2f}

Provide:

1. Overall Trend
2. RSI Interpretation
3. Risk Level
4. Short-Term Outlook
5. Buy / Hold / Sell Recommendation
6. Explain your reasoning in simple language.
"""

        try:
            analysis = generate_stock_analysis(prompt)
            st.write(analysis)

        except Exception as e:
            st.error(f"AI Analysis Error: {e}")

    else:
        st.warning("Unable to generate AI analysis because RSI data is unavailable.")


# import streamlit as st
# import plotly.graph_objects as go
# import yfinance as yf
# from services.sentiment_services import analyze_sentiment
# from services.ai_services import generate_stock_analysis

# from services.stock_services import (
#     get_stock_info,
#     get_stock_history,
# )

# from services.news_services import get_company_news


# # --------------------------------------------------
# # Page Configuration
# # --------------------------------------------------

# st.set_page_config(
#     page_title="Financial Research AI",
#     layout="wide",
# )

# st.title("Financial Research AI Agent")


# # --------------------------------------------------
# # User Inputs
# # --------------------------------------------------

# st.markdown("""Analyze stocks, market trends, company fundamentals and financial news using AI-powered insights""")

# col1, col2 = st.columns(2)

# with col1:
#     symbol1 = st.text_input(
#         "Stock 1",
#         value="RELIANCE.NS"
#     )

# with col2:
#     symbol2 = st.text_input(
#         "Stock 2",
#         value="TCS.NS"
#     )

# period = st.selectbox(
#     "Select Time Period",
#     [
#         "1mo",
#         "3mo",
#         "6mo",
#         "1y",
#         "2y",
#         "5y",
#     ],
# )


# # --------------------------------------------------
# # Analyze Button
# # --------------------------------------------------

# if st.button("Analyze Stock"):

#     # ==========================================
#     # Company Information
#     # ==========================================
    

#     st.write(analysis)
#     data = get_stock_info(symbol1)
#     data2 = get_stock_info(symbol2)

#     st.subheader("🏢 Company Information")
#     st.write(data)

#     with col2:
#         st.markdown(f"### {symbol2}")
#         st.write(data2)

#     # ==========================================
#     # Comparison Table
#     # ==========================================

#     st.subheader(" Stock Comparison")

#     comparison_data = {
#         "Metric": [
#             "Current Price",
#             "Open",
#             "High",
#             "Low",
#             "Previous Close",
#             "Volume",
#             "Market Cap",
#         ],
#         symbol1: [
#             data["Current Price"],
#             data["Open"],
#             data["High"],
#             data["Low"],
#             data["Previous Close"],
#             data["Volume"],
#             data["Market Cap"],
#         ],
#         symbol2: [
#             data2["Current Price"],
#             data2["Open"],
#             data2["High"],
#             data2["Low"],
#             data2["Previous Close"],
#             data2["Volume"],
#             data2["Market Cap"],
#         ],
#     }

#     st.table(comparison_data)

#     # ==========================================
#     # Quick Comparison
#     # ==========================================

#     st.subheader(" Quick Comparison")

#     change1 = data["Current Price"] - data["Previous Close"]
#     change2 = data2["Current Price"] - data2["Previous Close"]

#     if change1 > change2:

#         st.success(
#             f" Better Performer Today: {symbol1}"
#         )

#         st.write(f"Today's Gain: ₹{change1:.2f}")

#     elif change2 > change1:

#         st.success(
#             f" Better Performer Today: {symbol2}"
#         )

#         st.write(f"Today's Gain: ₹{change2:.2f}")

#     else:

#         st.info(" Both stocks performed equally today.")

    
# # ==========================================
# # Stock Price Chart
# # ==========================================

# history = get_stock_history(symbol1, period)
# history2 = get_stock_history(symbol2, period)

# if (
#     history is not None
#     and not history.empty
#     and history2 is not None
#     and not history2.empty
# ):

#     fig = go.Figure()

#     fig.add_trace(
#         go.Scatter(
#             x=history.index,
#             y=history["Close"],
#             mode="lines",
#             name=symbol1,
#         )
#     )

#     fig.add_trace(
#         go.Scatter(
#             x=history2.index,
#             y=history2["Close"],
#             mode="lines",
#             name=symbol2,
#         )
#     )

#     fig.update_layout(
#         title=f"{symbol1} vs {symbol2} Closing Price",
#         xaxis_title="Date",
#         yaxis_title="Price (₹)",
#         template="plotly_white",
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True,
#     )

# else:
#     st.error("Unable to fetch stock history.")

#     # ==========================================
#     # Latest News
#     # ==========================================

#     st.subheader("Latest News")

#     company_name = data.get("Company")



#     # ------ NEWS MODEL ------
#     # This section fetches recent company-related news articles 
#     # Using News API and displays them inside Streamlit

#     if company_name:

#         st.write(f"Searching News For: **{company_name}**")

#         news = get_company_news(company_name)

#         if news:

#             st.success(f"Found {len(news)} Articles")

#             for article in news:

#                 st.markdown(f"### {article['title']}")

#                 if article.get("description"):
#                     st.write(article["description"])

#                 # ---------------- Sentiment Analysis ----------------

#                 headline = article["title"]

#                 if article.get("description"):
#                     headline += " " + article["description"]

#                 sentiment, score = analyze_sentiment(headline)

#                 if sentiment == "Positive":
#                     st.success(f" Sentiment: {sentiment} ({score:.2f})")

#                 elif sentiment == "Negative":
#                     st.error(f"Sentiment: {sentiment} ({score:.2f})")

#                 else:
#                     st.info(f" Sentiment: {sentiment} ({score:.2f})")

#                 if article.get("source"):
#                     st.caption(f" Source: {article['source']}")

#                 if article.get("publishedAt"):
#                     st.caption(
#                         f" Published: {article['publishedAt'][:10]}"
#                     )

#                 if article.get("url"):
#                     st.link_button(
#                         " Read Full Article",
#                         article["url"],
#                     )

#                 st.divider()

#         else:
#             st.warning("No news found.")


#     else:
#         st.error("Company name not found.")