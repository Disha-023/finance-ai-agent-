import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
from textblob import TextBlob
from datetime import datetime       # For Current Time
import pytz                         # For Indian Timezone      
import plotly.express as px         # For Plotly Express charts

from services.stock_services import (
    get_stock_info,
    get_stock_history,
)

from services.news_services import get_company_news
from services.sentiment_services import analyze_sentiment
from services.ai_services import generate_stock_analysis

# watchlist database functions
from services.watchlist_service import (
    init_db,
    add_stock,
    get_watchlist
)

# Portfolio database functions
from services.portfolio_service import (
    init_portfolio_db,
    add_to_portfolio,
    get_portfolio
)

# Custom CSS for metric cards
st.markdown("""
<style>
.metric-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 10px;
}

.metric-title {
    font-size: 14px;
    color: #666666;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #111111;
}

.confidence-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 10px;
}

.confidence-title {
    font-size: 14px;
    color: #666666;
}

.confidence-value {
    font-size: 28px;
    font-weight: bold;
    color: #111111;
}

.stProgress > div > div > div {
    background-color: #667eea;
}

.stProgress > div > div > div > div {
    background-color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)


# Page Configuration

st.set_page_config(
    page_title="Financial Research AI",
    layout="wide",
)

# Create watchlist database if not exists init_db()
init_db()

# Create portfolio database if not exists init_portfolio_db()
init_portfolio_db()

# st.title("Financial Research AI Agent")

# st.markdown(
#     """
# Analyze stocks, market trends, company fundamentals and financial news using AI-powered insights.
# """
# )

st.markdown("""
<div style="
background: linear-gradient(90deg,#0f172a,#1e293b);
padding:25px;
border-radius:15px;
margin-bottom:20px;
">

<h1 style="color:white;margin:0;">Financial Research AI Agent</h1>

<p style="color:#cbd5e1;font-size:18px;">
AI-Powered Stock Analysis • Portfolio Intelligence • Market Sentiment
</p>

</div>
""", unsafe_allow_html=True)

# ---------- Indian Market Status ----------

india = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(india)

market_open = current_time.replace(
    hour=9,
    minute=15,
    second=0
)

market_close = current_time.replace(
    hour=15,
    minute=30,
    second=0
)

# if market_open <= current_time <= market_close:

#     st.success(
#         f" NSE Market Open | {current_time.strftime('%I:%M %p IST')}"
#     )

# else:

#     st.error(
#         f" NSE Market Closed | {current_time.strftime('%I:%M %p IST')}"
#     )

if market_open <= current_time <= market_close:

    st.markdown(f"""
    <div style="
    background:#dcfce7;
    padding:15px;
    border-radius:12px;
    border-left:6px solid green;
    ">
     NSE Market Open | {current_time.strftime('%I:%M %p IST')}
    </div>
    """, unsafe_allow_html=True)

else:

    st.markdown(f"""
    <div style="
    background:#fee2e2;
    padding:15px;
    border-radius:12px;
    border-left:6px solid red;
    ">
     NSE Market Closed | {current_time.strftime('%I:%M %p IST')}
    </div>
    """, unsafe_allow_html=True)


# User Inputs

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

# ---------- Sidebar Controls improvement ----------
with st.sidebar:

    st.title(" Stock Controls ")

    symbol1 = st.text_input("Stock 1",value="RELIANCE.NS")

    if st.button(f"Add {symbol1} to Watchlist", use_container_width=True):
        add_stock(symbol1)
        st.success(f"{symbol1} added to WatchList")

    symbol2 = st.text_input("Stock 2",value="TCS.NS")

    if st.button(f"Add {symbol2} to WatchList", use_container_width=True):
        add_stock(symbol2)
        st.success(f"{symbol2} added to WatchList")

    period = st.selectbox(
        "Time Period",
        [
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y",
            "5y",
        ],
    )

    analyze_button = st.button(" Analyze Stocks ",use_container_width=True)


    st.markdown("---")
    st.subheader("My Watchlist")

    watchlist = get_watchlist()

    if watchlist:
        for stock in watchlist:
            st.write(stock[0])
    
    else:
        st.info("No Stock in Watchlist yet!")


    # ---------- Adding Portfolio Controls ---------- 
    st.markdown("---")
    st.subheader("Portfolio Tracker")

    portfolio_symbol = st.text_input("Portfolio Stock",value="RELIANCE.NS")

    portfolio_qty = st.number_input("Quantity",min_value=1,value=1)

    portfolio_buy_price = st.number_input("Buy Price (₹)",min_value=1.0,value=1000.0)

    if st.button("Add To Portfolio",use_container_width=True):
        add_to_portfolio(
            portfolio_symbol,
            portfolio_qty,
            portfolio_buy_price
        )

    st.success(f"{portfolio_symbol} added to Portfolio")

    
    # ---------- Portfolio DashBoard ----------

    st.subheader("## Portfolio Dashboard")

    portfolio_data = get_portfolio()

    if portfolio_data:

        portfolio_table = []

        total_investment = 0
        total_current_value = 0

        for stock in portfolio_data:

            symbol = stock[0]
            quantity = stock[1]
            buy_price = stock[2]

            current_data = get_stock_info(symbol)

            current_price = current_data["Current Price"]

            investment = quantity * buy_price
            current_value = quantity * current_price

            profit_loss = current_value - investment

            total_investment += investment
            total_current_value += current_value

            portfolio_table.append({
                "Stock": symbol,
                "Quantity": quantity,
                "Buy Price": f"₹{buy_price:.2f}",
                "Current Price": f"₹{current_price:.2f}",
                "Investment": f"₹{investment:.2f}",
                "Current Value": f"₹{current_value:.2f}",
                "Profit/Loss": f"₹{profit_loss:.2f}"
            })

        st.dataframe(portfolio_table,use_container_width=True)

        total_profit = (total_current_value - total_investment)

        portfolio_return = (total_profit / total_investment) * 100

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f"""
    <div style="background:#E3F2FD;padding:15px;border-radius:12px;text-align:center;">
        <h5>Total Investment</h5>
        <h2>₹{total_investment:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
    <div style="background:#E8F5E9;padding:15px;border-radius:12px;text-align:center;">
        <h5>Current Value</h5>
        <h2>₹{total_current_value:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
    <div style="background:#FFF3E0;padding:15px;border-radius:12px;text-align:center;">
        <h5>Total Profit</h5>
        <h2>₹{total_profit:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
    <div style="background:#F3E5F5;padding:15px;border-radius:12px;text-align:center;">
        <h5>Return %</h5>
        <h2>{portfolio_return:.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
    <div style="background:#FFEBEE;padding:15px;border-radius:12px;text-align:center;">
        <h5>Stocks</h5>
        <h2>{len(portfolio_data)}</h2>
    </div>
    """, unsafe_allow_html=True)

        # Finding Top Gainer / Loser

        best_stock = max(portfolio_table,
            key=lambda x: float(
                x["Profit/Loss"]
                .replace("₹", "")
                .replace(",", "")
            )
        )

        worst_stock = min(portfolio_table,
            key=lambda x: float(
                x["Profit/Loss"]
                .replace("₹", "")
                .replace(",", "")
            )
        )

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"Top Gainer: {best_stock['Stock']}")
            st.write(f"Profit: {best_stock['Profit/Loss']}")

        with col2:
            st.error(f"Top Loser: {worst_stock['Stock']}")
            st.write(f"Profit: {worst_stock['Profit/Loss']}")

        
        st.subheader("## SIP Goal Planner")

        goal_amount = st.number_input("Target Amount (₹)",min_value=10000,value=1000000)

        years = st.number_input("Investment Duration (Years)",min_value=1,value=10)

        expected_return = st.slider("Expected Annual Return (%)",1,30,12)

        monthly_rate = expected_return / 100 / 12
        months = years * 12

        sip = (goal_amount * monthly_rate / (((1 + monthly_rate) ** months) - 1))
        sip = sip / (1 + monthly_rate)

        st.success(f"Required Monthly SIP: ₹{sip:,.0f}")

        st.subheader("## Portfolio Allocation")

        allocation_data = []

        for stock in portfolio_data:

            symbol = stock[0]
            quantity = stock[1]
            buy_price = stock[2]

            value = quantity * buy_price

            allocation_data.append({"Stock": symbol,"Value": value})

        if allocation_data:
            fig = px.pie(allocation_data,names="Stock",values="Value",title="Portfolio Allocation")

            st.plotly_chart(fig,use_container_width=True)



    else:
        st.info("No stocks in portfolio yet.")



# ---------- Analyze Button ----------

if analyze_button:

    # Fetch Stock Data

    data = get_stock_info(symbol1)
    data2 = get_stock_info(symbol2)

    history = get_stock_history(symbol1, period)
    history2 = get_stock_history(symbol2, period)

    
    # Company Information

    st.subheader(" Company Information")

    col1, col2 = st.columns(2)

    # ---------- Fundamental Analysis Comparison ----------

    with col1:
        # st.info(f"{symbol1}")

        # st.markdown(f"""
        #     **Company:** {data['Company']}  
        #     **Sector:** {data['Sector']}  
        #     **Industry:** {data['Industry']}
        # """)

        st.markdown(f"""
        <div style="
            background:#f8fafc;
            padding:20px;
            border-radius:15px;
            border:1px solid #e2e8f0;
        ">

        <h3>{symbol1}</h3>

        <b>Company:</b> {data['Company']}<br>
        <b>Sector:</b> {data['Sector']}<br>
        <b>Industry:</b> {data['Industry']}

        </div>
        """, unsafe_allow_html=True)



    with col2:
        # st.info(f"{symbol2}")

        # st.markdown(f"""
        #     **Company:** {data2['Company']}  
        #     **Sector:** {data2['Sector']}  
        #     **Industry:** {data2['Industry']}
        # """)

        st.markdown(f"""
        <div style="
            background:#f8fafc;
            padding:20px;
            border-radius:15px;
            border:1px solid #e2e8f0;
        ">

        <h3>{symbol2}</h3>

        <b>Company:</b> {data2['Company']}<br>
        <b>Sector:</b> {data2['Sector']}<br>
        <b>Industry:</b> {data2['Industry']}

        </div>
        """, unsafe_allow_html=True)
    

    # col1, col2 = st.columns(2)

    # with col1:
    #     st.markdown(f"### {symbol1}")
    #     st.write(data)

    # with col2:
    #     st.markdown(f"### {symbol2}")
    #     st.write(data2)


   
    # Stock Comparison

    st.subheader(" Stock Comparison")

    comparison_data = {
        "Metric": [
            "Current Price",
            "High",
            "Low",
            "Market Cap",
            "P/E Ratio",
            "EPS",
            "Dividend Yield",
            "52W High",
            "52W Low"
        ],
        symbol1: [
            data["Current Price"],
            data["High"],
            data["Low"],
            data["Market Cap"],
            data.get("PE Ratio"),
            data.get("EPS"),
            data.get("Dividend Yield"),
            data.get("52W High"),
            data.get("52W Low")
        ],
        symbol2: [
            data2["Current Price"],
            data2["High"],
            data2["Low"],
            data2["Market Cap"],
            data2.get("PE Ratio"),
            data2.get("EPS"),
            data2.get("Dividend Yield"),
            data2.get("52W High"),
            data2.get("52W Low")
        ],
    }

    st.table(comparison_data)

    # ---------- Fundamental Health Comparison ----------

    st.subheader("Fundamental Health")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"{symbol1}")

        m1,m2,m3 = st.columns(3)

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Debt/Equity</div>
                <div class="metric-value">{data.get("Debt To Equity","N/A")}</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">ROE</div>
                <div class="metric-value">{data.get("ROE","N/A")}</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Revenue Growth</div>
                <div class="metric-value">{data.get("Revenue Growth","N/A")}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"{symbol2}")

        m1,m2,m3 = st.columns(3)

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Debt/Equity</div>
                <div class="metric-value">{data2.get("Debt To Equity","N/A")}</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">ROE</div>
                <div class="metric-value">{data2.get("ROE","N/A")}</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Revenue Growth</div>
                <div class="metric-value">{data2.get("Revenue Growth","N/A")}</div>
            </div>
            """, unsafe_allow_html=True)

    
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

        # 20 Day Moving Average

        fig.add_trace(
            go.Scatter(
                x=history.index,
                y=history["MA20"],
                mode="lines",
                name=f"{symbol1} MA20",
                line=dict(dash="dot"),
            )
        )

        # 50 Day Moving Average

        fig.add_trace(
            go.Scatter(
                x=history.index,
                y=history["MA50"],
                mode="lines",
                name=f"{symbol1} MA50",
                line=dict(dash="dash"),
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

        # 20 Day Moving Average
        fig.add_trace(
            go.Scatter(
                x=history2.index,
                y=history2["MA20"],
                mode="lines",
                name=f"{symbol2} MA20",
                line=dict(dash="dot"),
            )
        )

        # 50 Day Moving Average
        fig.add_trace(
            go.Scatter(
                x=history2.index,
                y=history2["MA50"],
                mode="lines",
                name=f"{symbol2} MA50",
                line=dict(dash="dash"),
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

            sentiment_score = 0

            for article in news:

                # ----- SENTIMENT ANALYSIS -----
                # Calculates overall market sentiment from recent news headlines using TextBlob polarity score 

                headline = article["title"]

                analysis = TextBlob(headline)

                sentiment_score += analysis.sentiment.polarity

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

            # ----- SENTIMENT SUMMARY -----
            # Displays overall market sentiment based on news analysis

            avg_sentiment = sentiment_score / len(news)

            st.subheader("AI Market Sentiment Dashboard")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Sentimate Score", f"{avg_sentiment:.2f}")

            with col2:
                sentiment_percentage = int(((avg_sentiment + 1) / 2) * 100)
                st.metric("Confidence Level", f"{sentiment_percentage}%")

            st.progress(sentiment_percentage)


            # ----- AI Reasearch Summary -----
            st.subheader("📋 AI Research Summary")

            if avg_sentiment > 0.1:

                st.success(""" Recent news coverage is largely positive.
                            The company is receiving favorable attention from the market which may improve investor confidence and future growth expectations.""")

            elif avg_sentiment < -0.1:

                st.error("""Recent news coverage contains negative signals.
                            Investors should carefully evaluate recent developments before making decisions.""")

            else:

                st.info("""News sentiment appears neutral.
                            No major positive or negative trend is currently visible from recent headlines.""")


            
            # ----- Financial Health Score -----
            score = 0
            recommendation = "N/A"

            stock = yf.Ticker(symbol1)
            info = stock.info

            pe_ratio = info.get("trailingPE")
            market_cap = data.get("Market Cap")

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

            st.subheader("Financial Health Score")
            st.progress(score)
            st.success(f"Financial Health Score: {score}/100")

            # ----- Investment Confidence Score -----
            confidence = score + (avg_sentiment * 20)

            confidence = max(0, min(100, confidence))



            st.subheader("Investment Confidence Score")

            st.markdown(f"""
            <div class="confidence-card">
                <div class="confidence-title">Confidence Score</div>
                <div class="confidence-value">{confidence:.0f}/100</div>
            </div>
            """, unsafe_allow_html=True)

            # ---------- AI Investment Scorecard ----------


            st.subheader(" AI Investment Scorecard ")

            rsi = history["RSI"].iloc[-1]

            technical_score = 50

            if rsi < 30:
                technical_score = 80

            elif rsi < 70:
                technical_score = 60

            else:
                technical_score = 40


            overall_score = (score + technical_score + confidence) / 3

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Financial Health</div>
                    <div class="metric-value">{score}/100</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Technical Strength</div>
                    <div class="metric-value">{technical_score}/100</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Confidence</div>
                    <div class="metric-value">{confidence:.0f}/100</div>
                </div>
                """, unsafe_allow_html=True)
    

            st.progress(int(overall_score))

            st.success(f"Overall Investment Score: {overall_score:.1f}/100")



            # ----- AI Recommendation -----
            recommendation = "HOLD"

            if avg_sentiment > 0.3:
                recommendation = "BUY"
            elif avg_sentiment < -0.3:
                recommendation = "SELL"


            # ----- AI Final Verdict -----
            st.subheader("🤖 AI Final Verdict")

            if recommendation == "BUY" and avg_sentiment > 0:

                st.success("""Strong Fundamentals + Positive News
                                AI Verdict:
                                This stock currently shows promising characteristics for further research.""")

            elif recommendation == "SELL" and avg_sentiment < 0:

                st.error("""Weak Fundamentals + Negative News
                                AI Verdict:
                                Investors should proceed cautiously.""")

            else:

                st.warning("""Mixed Signals Detected
                                AI Verdict:
                                Additional analysis is recommended before making investment decisions.""")

            

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