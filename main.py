import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="12mo")
    return hist

def calculate_valuation_metrics(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    try:
        pe_ratio = info.get("trailingPE", "N/A")
        pb_ratio = info.get("priceToBook", "N/A")
        ev_ebitda = info.get("enterpriseToEbitda", "N/A")
        roe = info.get("returnOnEquity", "N/A")
        roa = info.get("returnOnAssets", "N/A")
        free_cash_flow = info.get("freeCashflow", "N/A")
        market_cap = info.get("marketCap", "N/A")
        dcf = info.get("discountedCashFlow", "N/A")
        return {
            "P/E Ratio": pe_ratio,
            "P/B Ratio": pb_ratio,
            "EV/EBITDA": ev_ebitda,
            "ROE": roe,
            "ROA": roa,
            "Free Cash Flow": free_cash_flow,
            "Market Cap": market_cap,
            "Discounted Cash Flow (DCF)": dcf
        }
    except:
        return {}

# Streamlit UI
st.title("📈 Indian Stock Market Dashboard")

# User input for stock selection
ticker = st.text_input("Enter Stock Ticker (e.g., RELIANCE.NS)", "RELIANCE.NS")
if ticker:
    st.subheader(f"Stock Price Data for {ticker}")
    data = fetch_stock_data(ticker)
    if not data.empty:
        fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Price Trend")
        st.plotly_chart(fig)
    else:
        st.warning("Could not fetch data. Check the ticker symbol.")
    
    # Valuation Metrics
    st.subheader("📊 Valuation Metrics")
    metrics = calculate_valuation_metrics(ticker)
    if metrics:
        st.write(pd.DataFrame(metrics.items(), columns=["Metric", "Value"]))
    else:
        st.warning("No valuation data available.")
    
    # Additional Interactive Features
    st.sidebar.header("Customize View")
    show_volume = st.sidebar.checkbox("Show Volume Data")
    if show_volume:
        st.subheader("📉 Trading Volume")
        fig_volume = px.line(data, x=data.index, y='Volume', title=f"{ticker} Trading Volume")
        st.plotly_chart(fig_volume)
