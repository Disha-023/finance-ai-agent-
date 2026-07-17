import streamlit as st
import plotly.graph_objects as go

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

st.title("📈 Financial Research AI Agent")


# --------------------------------------------------
# User Inputs
# --------------------------------------------------

symbol = st.text_input(
    "Enter Stock Symbol",
    value="RELIANCE.NS"
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

    data = get_stock_info(symbol)

    st.subheader("🏢 Company Information")
    st.write(data)

    # ==========================================
    # Stock Price Chart
    # ==========================================

    history = get_stock_history(symbol, period)

    if history is not None and not history.empty:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=history.index,
                y=history["Close"],
                mode="lines",
                name="Closing Price",
            )
        )

        fig.update_layout(
            title=f"{symbol} Closing Price",
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

    st.subheader("📰 Latest News")

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

                if article.get("source"):
                    st.caption(f"📰 Source: {article['source']}")

                if article.get("publishedAt"):
                    st.caption(
                        f"📅 Published: {article['publishedAt'][:10]}"
                    )

                if article.get("url"):
                    st.link_button(
                        "🔗 Read Full Article",
                        article["url"],
                    )

                st.divider()

        else:
            st.warning("No news found.")

    else:
        st.error("Company name not found.")