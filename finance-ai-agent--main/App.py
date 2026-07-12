import streamlit as st
import plotly.graph_objects as go

from services.stock_services import (
    get_stock_info,
    get_stock_history
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

    st.write(data)

    history = get_stock_history(symbol, period)

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

    st.subheader("Latest News")

    if company_name:

        news = get_company_news(company_name)

        st.write(f"Searching News For: {company_name}")
        st.write(f"Articles Found: {len(news)}")

        if news:

            for article in news:

                st.markdown(f"### {article.get('title')}")

                if article.get("description"):
                   st.write(article["description"])

                if article.get("url"):
                   st.markdown(f"[Read Full Article]({article['url']})")

                st.write("---")

        else:

            st.warning("No News Found")

    else:

        st.error("Company name not found.")

       