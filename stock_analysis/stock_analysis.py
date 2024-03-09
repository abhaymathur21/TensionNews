import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_stock_history(company_name, num_days=365):
    try:
        stock_info = yf.Ticker(company_name)
        ticker_symbol = stock_info.info['symbol']
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=num_days)).strftime('%Y-%m-%d')
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

        return stock_data
    except Exception as e:
        print(f"Error: {e}")
        return None

def plot_stock_history(stock_data, company_name):
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label=f'{company_name} Stock Price')
    plt.title(f'{company_name} Stock Price History')
    plt.xlabel('Date')
    plt.ylabel('Stock Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    company_name = input("Enter the company name: ")
    stock_history = get_stock_history(company_name)

    if stock_history is not None:
        print("\nStock History:\n", stock_history.head())
        plot_stock_history(stock_history, company_name)

if __name__ == "__main__":
    main()
