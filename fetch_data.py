import yfinance as yf
import pandas as pd
import os

def fetch_data(tickers, start_date, end_date, output_file="historical_data.csv"):
    """
    Fetch historical stock data for a list of tickers and save it to a CSV file.

    Args:
        tickers (list): List of stock tickers (e.g., ['AAPL', 'GOOG']).
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        output_file (str): Name of the output CSV file (default: 'historical_data.csv').

    Returns:
        None
    """
    # Initialize an empty dictionary to store data for each ticker
    all_data = {}

    for ticker in tickers:
        try:
            print(f"Fetching data for {ticker}...")
            stock_data = yf.download(ticker, start=start_date, end=end_date)
            if not stock_data.empty:
                all_data[ticker] = stock_data
            else:
                print(f"Warning: No data found for {ticker}.")
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    # Combine data into a single DataFrame
    if all_data:
        combined_data = pd.concat(all_data, axis=1)
        combined_data.columns = [f"{col[0]}_{col[1]}" for col in combined_data.columns]

        # Save to CSV
        combined_data.to_csv(output_file)
        print(f"Data successfully saved to {output_file}")
    else:
        print("No data was fetched. Please check the tickers or date range.")

if __name__ == "__main__":
    # Example configuration
    tickers = ["AAPL", "GOOG", "TSLA", "SPY"]  # List of stock tickers
    start_date = "2022-01-01"  # Start date for fetching data
    end_date = "2023-01-01"    # End date for fetching data
    output_file = "historical_data.csv"  # Output file name

    # Check if the output file already exists
    if os.path.exists(output_file):
        print(f"Warning: {output_file} already exists and will be overwritten.")

    # Fetch data and save to CSV
    fetch_data(tickers, start_date, end_date, output_file)
