import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

@st.cache_data
def predict_stock_price(ticker):
    # Load HDFC stock data from Yahoo Finance
    stock_data = yf.Ticker(ticker).history(period="max")
    stock_data = stock_data['Close']
    stock_data.index = pd.to_datetime(stock_data.index)

    # Train a model to predict the closing stock price of HDFC bank using SARIMAX
    model = SARIMAX(stock_data, order=(1,1,1), seasonal_order=(1,1,1,12))
    model_fit = model.fit(disp=0)

    # Make predictions for the next 30 days
    forecast = model_fit.forecast(steps=31)

    # Create a date range for the next 30 days
    last_date = stock_data.index[-1]
    date_range = pd.date_range(last_date, periods=31, freq='D')[1:]

    # Create a DataFrame with the predicted values
    predicted_data = pd.DataFrame({
        'Date': date_range,
        'Predicted Price': forecast[1:]
    })
    predicted_data.set_index('Date', inplace=True)

    # Plot the actual and predicted stock prices
    chart_data = pd.concat([stock_data, predicted_data], axis=1)
    st.line_chart(chart_data)


# Streamlit app code

