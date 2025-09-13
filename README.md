# 📈 Stock Dash

A modern, interactive Streamlit dashboard for visualizing and analyzing stock market data. This app lets you search for companies, view financial metrics, historical charts, analyst recommendations, and the latest news—all in a beautiful, modular UI.

---

## 🚀 Features

- **Company Search:** Type a company name to instantly fetch its ticker and financial data.
- **Financial Metrics:** View key statistics, ratios, and financial highlights in a clean, organized layout.
- **Currency Conversion:** Convert all metrics and charts to your preferred currency.
- **Interactive Charts:** Candlestick, OHLC, and line charts powered by Plotly.
- **Analyst Recommendations:** See analyst ratings, price targets, and sentiment.
- **Latest News:** Stay updated with recent headlines and provider logos.
- **Responsive UI:** Optimized for desktop and mobile, with tabs and cards for easy navigation.

---
## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/stock-dash.git
   cd stock-dash
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   streamlit run StockDash/fin4.py
   ```

---

## 🗂️ Project Structure

```
StockDash/
├── fin4.py                # Main Streamlit app
├── utility/
│   └── backend.py         # Backend logic (data fetching, formatting)
├── assets/                # SVGs, images, and video for UI and gallery
│   ├── home.jpg
│   └── ...
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 🧑‍💻 How It Works

- **Frontend:** Built with Streamlit, using columns, tabs, and custom SVGs for a modern look.
- **Backend:** All data fetching and formatting is handled in `utility/backend.py` for clean separation.
- **Assets:** SVGs and images are used for icons, logos, and gallery previews. You can add your own visuals to the `assets/` folder.

---

## 💡 Customization

- Add more SVGs or PNGs to the `assets/` folder for new icons or gallery images.
- Modify `utility/backend.py` to add new data sources or metrics.
- Tweak the UI in `StockDash.py` for your branding or layout preferences.

---

## 🤝 Contributing

Pull requests, issues, and suggestions are welcome! Please open an issue or PR if you have ideas for new features, bug fixes, or UI improvements.

---

### 🚧 Upcoming Features

- **Finance AI Agent:**
  - Researches recent financial events and news.
  - Provides major insights and summaries for stocks and markets.
  - Offers technical analysis and actionable recommendations.

Stay tuned for more intelligent features to make Stock Dash your go-to finance dashboard!

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [Yahoo Finance](https://finance.yahoo.com/)
- [Clearbit Logo API](https://clearbit.com/logo)

---

## 📬 Contact

For questions or feedback, reach out via [GitHub Issues](https://github.com/yourusername/stock-dash/issues) or email ranjithjayakumar322@gmail.com
