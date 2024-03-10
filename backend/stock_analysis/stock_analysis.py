import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from stock_analysis.stock_symbol_llm import llm_stock_symbol

def get_stock_history(company_name, end_date, num_days=7,):
    try:
        stock_info = yf.Ticker(company_name)
        ticker_symbol = stock_info.info['symbol']
        # end_date = datetime.today().strftime('%Y-%m-%d')
        end_date = end_date
        start_date = (end_date - timedelta(days=num_days)).strftime('%Y-%m-%d')
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

        return stock_data
    except Exception as e:
        print(f"Error: {e}")
        return None

# def plot_stock_history(stock_data, company_name):
#     plt.figure(figsize=(10, 6))
#     plt.plot(stock_data['Close'], label=f'{company_name} Stock Price')
#     plt.title(f'{company_name} Stock Price History')
#     plt.xlabel('Date')
#     plt.ylabel('Stock Price (USD)')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

def parse_relative_time(relative_time_str):
    # Extract the numeric value and unit (day or hour)
    value, unit = relative_time_str.split(' ')[0:2]
    
    # Convert the value to an integer
    value = int(value)
    
    # Initialize timedelta parameters
    kwargs = {}
    
    # Set the appropriate keyword argument based on the time unit
    if 'day' in unit:
        kwargs['days'] = value
    elif 'hour' in unit:
        kwargs['hours'] = value
    elif 'month' in unit:
        kwargs['months'] = value

    delta = timedelta(**kwargs)
    # Calculate the datetime object
    parsed_time = datetime.now() - delta
    
    return parsed_time

def stock_extraction(company_name, end_date_str):
    # company_name = input("Enter the company name: ")
    
    if isinstance(end_date_str, str):  # Check if end_date_str is a string
        end_date = parse_relative_time(end_date_str)  # Convert end_date_str to datetime object
    else:
        end_date = end_date_str
        print(end_date)
    # end_date = parse_relative_time(end_date_str)
    company_stock_symbol = llm_stock_symbol(company_name)
    stock_history = get_stock_history(company_stock_symbol, end_date)
    

    if stock_history is not None:
        # print("\nStock History:\n", stock_history.head())
        # plot_stock_history(stock_history, company_stock_symbol)
        closing_price = stock_history['Close'].tolist()
        volume = stock_history['Volume'].tolist()
        
        return closing_price, volume
    else:
        return None, None

# if __name__ == "__main__":
#     main()

# closing_price, volume = stock_extraction("Apple Inc.", "3 days ago")
# print(closing_price)
# print(volume)