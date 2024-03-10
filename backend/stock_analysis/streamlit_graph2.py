import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        st.error(f"Failed to fetch data for {symbol}. Error: {str(e)}")
        return None

def main():
    st.title('Stock Price Comparison')
    
    # Define symbols for the companies you want to compare
    symbols = st.text_input("Enter symbols of companies separated by commas (e.g., AAPL, MSFT, GOOGL):")
    symbols = [symbol.strip().upper() for symbol in symbols.split(",") if symbol.strip()]
    
    # Define date range (last year)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Fetch data and plot
    if symbols:
        st.subheader("Stock Prices for the Last Year")
        num_cols = len(symbols)
        columns = st.columns(num_cols)
        for i, symbol in enumerate(symbols):
            with columns[i]:
                st.write(f"### {symbol}")
                stock_data = fetch_stock_data(symbol, start_date, end_date)
                if stock_data is not None:
                    st.line_chart(stock_data['Adj Close'])

if __name__ == "__main__":
    main()
