import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'utility'))
import pandas as pd
from datetime import datetime
from utility.backend import (
    get_ticker_symbol,
    get_timezone_from_ticker,
    get_currency_from_ticker,
    get_company_logo,
    merge_and_fill,
    get_complete_data,
    format_pct,
    format_num,
    format_date,
    format_news_date
)
import yfinance as yf
import pytz
st.set_page_config(page_title="Stock Dash", layout="wide")

st_autorefresh(interval=500_000, key="datarefresh")

if "selected_symbol" not in st.session_state:
    st.session_state.selected_symbol = None
if "currency" not in st.session_state:
    st.session_state.currency = None
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "timezone" not in st.session_state:
    st.session_state.timezone = pytz.UTC

st.markdown("<h1 style='text-align: center;'> Stock Dash </h1>", unsafe_allow_html=True)
company_name = st.text_input("",help="Type your stock name ",placeholder="Type your stock names here...", value=st.session_state.company_name)




currency_rates_to_usd = {
    "USD": 1,
    "EUR": 1.10,
    "GBP": 1.26,
    "JPY": 0.0073,
    "CHF": 1.12,
    "CAD": 0.74,
    "AUD": 0.67,
    "CNY": 0.14,
    "INR": 0.012,
    "SGD": 0.73,
}

# Currency symbols
currency_symbols = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CHF": "Fr",
    "CAD": "C$",
    "AUD": "A$",
    "CNY": "¥",
    "INR": "₹",
    "SGD": "S$",
}

if company_name != st.session_state.company_name:
    symbol = get_ticker_symbol(company_name)
    if symbol:
        st.session_state.selected_symbol = symbol
        st.session_state.company_name = company_name
        ticker_obj = yf.Ticker(symbol)
    
    else:
        st.info("⚠️ Something went wrong, please try again.")
        st.session_state.selected_symbol = None
        st.session_state.currency = None
        st.session_state.timezone = pytz.UTC
        st.session_state.company_name = company_name
    st.session_state.currency = get_currency_from_ticker(ticker_obj)
    st.session_state.timezone = get_timezone_from_ticker(ticker_obj)
if st.session_state.selected_symbol:
    symbol = st.session_state.selected_symbol
    company_name = st.session_state.company_name
    base_currency = st.session_state.currency or "USD"
    local_tz = st.session_state.timezone
    ticker = yf.Ticker(symbol)
    company_logo = get_company_logo(company_name)

    selected_option = option_menu(
        None,
        [f"summary","charts"],
        icons=["organization", "bar-chart-line"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected_option == "charts":
        # === Middle column: currency selector ===
        currency_list = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY", "INR", "SGD"]
        default_currency_index = currency_list.index(base_currency) if base_currency in currency_list else 0
        left, middle, right = st.columns([2,1,3])

        with middle:
            selected_currency = st.selectbox(
                "Select currency",
                options=currency_list,
                index=default_currency_index,
                help="Select currency to convert metrics and charts"
            )

        try:
            to_usd_rate = currency_rates_to_usd.get(base_currency, 1)
            from_usd_rate = 1 / currency_rates_to_usd.get(selected_currency, 1)
            exchange_rate = to_usd_rate * from_usd_rate
        except Exception:
            exchange_rate = 1

        currency_symbol = currency_symbols.get(selected_currency, selected_currency)

        with left:
            if company_logo:
                st.image(company_logo, width=150)
            else:
                st.write("No company logo available")
            st.subheader(f"Metrics for {symbol} ({company_name})")

            info = ticker.info

            def conv(val):
                try:
                    return round(val * exchange_rate, 2)
                except:
                    return None

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Day High", f"{currency_symbol}{conv(info.get('dayHigh', None)) or 'N/A'}")
                st.metric("Day Low", f"{currency_symbol}{conv(info.get('dayLow', None)) or 'N/A'}")
                st.metric("Open", f"{currency_symbol}{conv(info.get('open', None)) or 'N/A'}")
                st.metric("Previous Close", f"{currency_symbol}{conv(info.get('previousClose', None)) or 'N/A'}")
                st.metric("Debt to Equity Ratio", f"{info.get('debtToEquity', 'N/A')}")
            with col2:
                st.metric("Volume", f"{info.get('volume', 'N/A')}")
                st.metric("Market Cap", f"{format_num(info.get('marketCap'))}")
                st.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
                st.metric("Dividend Yield", f"{format_pct(info.get('dividendYield'))}")
                st.metric("Net Income", f"{currency_symbol}{conv(info.get('netIncomeToCommon', None)) or 'N/A'}")

        with right:
            st.subheader("📈 Historical Chart")
            col1, col2, col3 = st.columns(3)
            with col1:
                period = st.selectbox(
                    "Select period",
                    ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"],
                    index=2,
                )
            with col2:
                interval = st.selectbox(
                    "Select interval",
                    ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
                    index=8,
                )
            with col3:
                chart_type = st.selectbox(
                    "Select chart type",
                    ["Candlestick", "Line", "OHLC"],
                    index=0,
                )

            hist = ticker.history(period=period, interval=interval)

            if hist.empty:
                st.warning("⚠️ No data available for this period and interval.")
            else:
                for col in ['Open', 'High', 'Low', 'Close']:
                    if col in hist.columns:
                        hist[col] = hist[col] * exchange_rate

                if interval in ["1d", "5d", "1wk", "1mo", "3mo"]:
                    date_range = pd.date_range(start=hist.index.min(), end=hist.index.max(), freq='D')
                    hist = hist.reindex(date_range)
                    hist[['Open', 'High', 'Low', 'Close']] = hist[['Open', 'High', 'Low', 'Close']].fillna(method='ffill')

                if hist.index.tz is None and interval not in ["1d", "5d", "1wk", "1mo", "3mo"]:
                    hist.index = hist.index.tz_localize('UTC')
                if hist.index.tz:
                    hist.index = hist.index.tz_convert(local_tz)

                if chart_type == "Candlestick":
                    fig = go.Figure(data=[go.Candlestick(
                        x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'],
                        increasing_line_color='green',
                        decreasing_line_color='red'
                    )])
                elif chart_type == "OHLC":
                    fig = go.Figure(data=[go.Ohlc(
                        x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'],
                        increasing_line_color='green',
                        decreasing_line_color='red'
                    )])
                else:  
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close'))

                fig.update_layout(
                    title=f"{symbol} ({period}, {interval}) - {chart_type} Chart",
                    xaxis_title="Date/Time",
                    yaxis_title=f"Price ({currency_symbol})",
                    xaxis_rangeslider_visible=False,
                    template="plotly_white",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)

    elif selected_option == f"summary":
        st.markdown(f"# {company_name}")
        def format_date(ts):
            try:
                return datetime.fromtimestamp(ts).strftime("%b %d, %Y")
            except:
                return "N/A"

        
       
        logo_col, summary_col = st.columns([1, 4])
        with logo_col:
            if company_logo:
                st.image(company_logo, width=120)
            else:
                st.write("No logo available")
        info = ticker.info
        ex_div_date = format_date(info.get('exDividendDate'))
        last_split_date = format_date(info.get('lastSplitDate'))
        last_split_factor = info.get('lastSplitFactor', 'N/A')
        with summary_col:
            st.markdown("# Company Overview")
            st.write(ticker.info.get('longBusinessSummary', "No summary available."))

        st.markdown("---")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Key Stats", "Financials", "Dividends", "Analyst Views", "News"
        ])

        with tab1:
            st.subheader("Statistics")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Market Cap", format_num(info.get('marketCap')))
                st.metric("Enterprise Value", format_num(info.get('enterpriseValue')))
                st.metric("Beta", info.get('beta', "N/A"))
                st.metric("52W High", info.get('fiftyTwoWeekHigh', 'N/A'))

            with col2:
                st.metric("52W Low", info.get('fiftyTwoWeekLow', 'N/A'))
                st.metric("Trailing P/E", info.get('trailingPE', 'N/A'))
                st.metric("Forward P/E", info.get('forwardPE', 'N/A'))
                st.metric("PEG Ratio", info.get('pegRatio', 'N/A'))

            with col3:
                st.metric("Price/Book", info.get('priceToBook', 'N/A'))
                st.metric("Price/Sales", info.get('priceToSalesTrailing12Months', 'N/A'))
                st.metric("Dividend Yield", format_pct(info.get('dividendYield')))
                st.metric("Shares Outstanding", format_num(info.get('sharesOutstanding')))

        with tab2:
            st.subheader("Financial Highlights")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Revenue (TTM)", format_num(info.get('totalRevenue')))
                st.metric("Gross Profit", format_num(info.get('grossProfits')))
                st.metric("EBITDA", format_num(info.get('ebitda')))

            with col2:
                st.metric("Operating Income", format_num(info.get('operatingIncome')))
                st.metric("Net Income", format_num(info.get('netIncomeToCommon')))
                st.metric("Free Cash Flow", format_num(info.get('freeCashflow')))

            with col3:
                st.metric("Op. Cash Flow", format_num(info.get('operatingCashflow')))
                st.metric("Current Assets", format_num(info.get('currentAssets')))
                st.metric("Current Liabilities", format_num(info.get('currentLiab')))

        with tab3:
            st.subheader("Dividends & Splits")
            col1, col2, col3 = st.columns(3)

            col1.metric("Dividend Yield", format_pct(info.get('dividendYield')))
            col2.metric("Dividend Rate", info.get('dividendRate') or "N/A")
            col3.metric("Payout Ratio", format_pct(info.get('payoutRatio')))

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("## Ex-Dividend Date")
                st.metric(label="", value=ex_div_date)

            with col2:
                st.markdown("## Last Split")
                st.metric(label="", value=f"{last_split_factor}", delta=last_split_date)

    
        with tab4:
            st.subheader("Analyst Recommendations")

            col1, col2 = st.columns(2)
            rec_mean = info.get("recommendationMean")
            price_target = info.get("targetMeanPrice")
            rec_key = info.get("recommendationKey")

            if rec_mean:
                col1.metric("Recommendation Score", f"{rec_mean:.2f}", "1 = Strong Buy")
            else:
                col1.info("No recommendation score available")

            if price_target:
                col2.metric("Target Price", f"${price_target:.2f}")
            else:
                col2.info("No target price available")

            if rec_key:
                st.markdown(f"## Sentiment: `{rec_key.capitalize()}`")

        
    

        with tab5:
            st.subheader("Latest News")
            news = ticker.get_news(count=10)

            if news:
                for article in news:
                    content = article['content']
                    title = content.get('title', 'No title')
                    link = content.get('canonicalUrl', {}).get('url', '#')
                    provider = content.get('provider', {}).get('displayName', 'Unknown Source')
                    logo = content.get('provider', {}).get('logo', {}).get('url', None)
                    pub_date = format_news_date(content.get('pubDate', 0))

                    with st.container():
                        cols = st.columns([1, 9])
                        
                        with cols[0]:
                            if logo:
                                st.image(logo, width=40)
                            else:
                                st.markdown("📰")

                        with cols[1]:
                            st.markdown(f"### [{title}]({link})")
                            st.markdown(f"<small>🕒 {pub_date} — *{provider}*</small>", unsafe_allow_html=True)

                        st.markdown("---")
            else:
                st.info("No recent news available.")

    else:
        st.write("Feature under development.")

else:
    st.info("Please enter a valid company name to enable dashboard features.")
