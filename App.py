import streamlit as st
import plotly.graph_objects as go

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

    st.subheader("Company Information")

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

    st.info(f"Market Cap: ₹{data.get('Market Cap')}")

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

       