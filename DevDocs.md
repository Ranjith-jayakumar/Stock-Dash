# 📚 Developer Documentation: Stock Dash

This document provides a comprehensive overview of the Stock Dash application, including its architecture, main modules, and developer guidelines. It covers both the main Streamlit app (`StockDash.py`) and the backend utility module (`utility/backend.py`).

---

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Main App: StockDash.py](#main-app-stockdashpy)
- [Backend Utility: backend.py](#backend-utility-backendpy)
- [Data Flow](#data-flow)
- [Extending the App](#extending-the-app)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

---

## Architecture Overview

Stock Dash is a modular Streamlit application for stock market analytics. It separates frontend UI logic from backend data processing, making the codebase maintainable and extensible.

- **Frontend/UI:** `StockDash.py` (Streamlit app)
- **Backend/Data:** `utility/backend.py` (data fetching, formatting, helpers)
- **Assets:** Images, SVGs, and videos for UI and documentation

---

## Main App: StockDash.py

### Purpose
- Provides the user interface for searching companies, viewing financial metrics, charts, analyst recommendations, and news.
- Handles user input, session state, and layout using Streamlit components.

### Key Components
- **Imports:**
  - Streamlit, Plotly, yfinance, pandas, pytz, and custom backend functions.
- **Session State:**
  - Tracks selected symbol, currency, company name, and timezone for persistent user experience.
- **UI Elements:**
  - Text input for company search
  - Option menu for navigation (summary, charts)
  - Columns and tabs for organized display
  - Metrics, charts, and news sections
- **Currency Conversion:**
  - Uses `currency_rates_to_usd` and `currency_symbols` for dynamic conversion and display.
- **Search Logic:**
  - On company name change, fetches ticker symbol and updates session state.
  - Handles errors gracefully with user-friendly messages.
- **Charting:**
  - Interactive Plotly charts (Candlestick, OHLC, Line)
  - Historical data fetched via yfinance
- **Tabs:**
  - Summary, Key Stats, Financials, Dividends, Analyst Views, News

### Example UI Flow
1. User enters a company name.
2. App fetches ticker symbol and financial data.
3. UI updates with metrics, charts, and news.
4. User can switch tabs for more details.

---

## Backend Utility: backend.py

### Function Documentation

#### `get_ticker_symbol(company_name)`
- **Description:** Searches Yahoo Finance for the ticker symbol of a given company name.
- **Args:**
  - `company_name` (str): The name of the company to search for.
- **Returns:**
  - `symbol` (str or None): The ticker symbol if found, else None.
- **Usage:**
  ```python
  symbol = get_ticker_symbol('Apple')
  ```

#### `get_timezone_from_ticker(ticker)`
- **Description:** Extracts the timezone information from a yfinance Ticker object.
- **Args:**
  - `ticker` (yfinance.Ticker): The ticker object.
- **Returns:**
  - `timezone` (pytz.timezone): The timezone of the exchange, or UTC if not found.
- **Usage:**
  ```python
  tz = get_timezone_from_ticker(ticker)
  ```

#### `get_currency_from_ticker(ticker)`
- **Description:** Gets the currency code for the selected ticker.
- **Args:**
  - `ticker` (yfinance.Ticker): The ticker object.
- **Returns:**
  - `currency` (str): The currency code (e.g., 'USD', 'EUR').
- **Usage:**
  ```python
  currency = get_currency_from_ticker(ticker)
  ```

#### `get_company_logo(company_name)`
- **Description:** Fetches the company logo using the Clearbit Logo API.
- **Args:**
  - `company_name` (str): The name of the company.
- **Returns:**
  - `logo_url` (str or None): The URL of the logo if found, else None.
- **Usage:**
  ```python
  logo_url = get_company_logo('Apple')
  ```

#### `merge_and_fill(annual, quarterly)`
- **Description:** Merges annual and quarterly financial DataFrames, filling missing data with the first available value.
- **Args:**
  - `annual` (pd.DataFrame): Annual financials.
  - `quarterly` (pd.DataFrame): Quarterly financials.
- **Returns:**
  - `dict`: Dictionary of merged financial data.
- **Usage:**
  ```python
  merged = merge_and_fill(annual_df, quarterly_df)
  ```

#### `get_complete_data(ticker_symbol)`
- **Description:** Fetches and merges all key financial data for a ticker symbol.
- **Args:**
  - `ticker_symbol` (str): The ticker symbol.
- **Returns:**
  - `dict`: Dictionary containing income, balance, cashflow, and info.
- **Usage:**
  ```python
  data = get_complete_data('AAPL')
  ```

#### `format_pct(val)`
- **Description:** Formats a value as a percentage string.
- **Args:**
  - `val` (float or None): The value to format.
- **Returns:**
  - `str`: Formatted percentage or 'N/A'.
- **Usage:**
  ```python
  pct = format_pct(0.1234)  # '12.34%'
  ```

#### `format_num(val)`
- **Description:** Formats a value as a human-readable number with commas.
- **Args:**
  - `val` (float or None): The value to format.
- **Returns:**
  - `str`: Formatted number or 'N/A'.
- **Usage:**
  ```python
  num = format_num(1234567)  # '1,234,567'
  ```

#### `format_date(ts)`
- **Description:** Converts a timestamp to a readable date string.
- **Args:**
  - `ts` (int or float): Unix timestamp.
- **Returns:**
  - `str`: Formatted date or 'N/A'.
- **Usage:**
  ```python
  date_str = format_date(1694563200)
  ```

#### `format_news_date(timestamp)`
- **Description:** Formats a news timestamp for display.
- **Args:**
  - `timestamp` (int or float): Unix timestamp.
- **Returns:**
  - `str`: Formatted date or 'N/A'.
- **Usage:**
  ```python
  news_date = format_news_date(1694563200)
  ```

---

## Data Flow

1. **User Input:**
   - User enters a company name in the UI.
2. **Backend Query:**
   - `get_ticker_symbol` fetches the ticker symbol.
   - Other backend functions fetch and format financial data.
3. **Session State Update:**
   - Selected symbol, currency, and timezone are stored.
4. **UI Rendering:**
   - Metrics, charts, and news are displayed using Streamlit components.

---

## Extending the App

- **Add New Metrics:**
  - Implement new functions in `backend.py` for additional financial data.
  - Update UI in `StockDash.py` to display new metrics.
- **Support More Currencies:**
  - Add rates and symbols to `currency_rates_to_usd` and `currency_symbols`.
- **Custom Visualizations:**
  - Use Plotly or other libraries for new chart types.
- **UI Customization:**
  - Modify layout, colors, and assets for branding.

---

## Error Handling

- All backend functions use try/except blocks to avoid crashing the app.
- UI displays generic messages ("Something went wrong, please try again") for user-facing errors.
- Data validation and fallback values are used throughout.

---

## Best Practices

- **Separation of Concerns:** Keep UI and backend logic separate.
- **Session State:** Use Streamlit's session state for persistent user experience.
- **Modular Functions:** Write reusable, well-documented functions in `backend.py`.
- **Graceful Error Handling:** Never expose raw errors to users; use friendly messages.
- **Version Control:** Commit all code, assets, and documentation to GitHub.
- **Documentation:** Keep `README.md` and `DevDocs.md` up to date for users and developers.

---

## References
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Docs](https://plotly.com/python/)
- [Yahoo Finance API](https://finance.yahoo.com/)
- [Clearbit Logo API](https://clearbit.com/logo)

---

For further questions, open an issue or contact the maintainer.
