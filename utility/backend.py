import yfinance as yf
import pandas as pd
import requests
import pytz
from datetime import datetime


def get_ticker_symbol(company_name):
    url = "https://query1.finance.yahoo.com/v1/finance/search"
    params = {"q": company_name, "quotes_count": 1, "news_count": 0}
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        results = response.json()
        if results["quotes"]:
            return results["quotes"][0]["symbol"]
    return None

def get_timezone_from_ticker(ticker):
    info = ticker.info
    tz = info.get("exchangeTimezoneName")
    if tz:
        return pytz.timezone(tz)
    return pytz.UTC

def get_currency_from_ticker(ticker):
    info = ticker.info
    return info.get("currency", "Unknown")

def get_company_logo(company_name):
    domain = company_name.replace(" ", "").lower() + ".com"
    logo_url = f"https://logo.clearbit.com/{domain}"
    try:
        response = requests.get(logo_url)
        if response.status_code == 200:
            return logo_url
    except:
        pass
    return None

def merge_and_fill(annual, quarterly):
    combined = pd.concat([annual, quarterly], axis=1)
    filled = combined.bfill(axis=1).iloc[:, 0]  # First non-null column
    return filled.to_dict()

def get_complete_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = {
        "income": merge_and_fill(ticker.financials, ticker.quarterly_financials),
        "balance": merge_and_fill(ticker.balance_sheet, ticker.quarterly_balance_sheet),
        "cashflow": merge_and_fill(ticker.cashflow, ticker.quarterly_cashflow),
        "info": ticker.info
    }
    return data

def format_pct(val):
    return f"{val:.2%}" if val is not None else "N/A"

def format_num(val):
    return f"{val:,.0f}" if val is not None else "N/A"

def format_date(ts):
    try:
        return datetime.fromtimestamp(ts).strftime("%b %d, %Y")
    except:
        return "N/A"

def format_news_date(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime("%b %d, %Y")
    except:
        return "N/A"
