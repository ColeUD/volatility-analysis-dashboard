import pandas as pd
import numpy as np

# Constants
TRADING_DAYS_YEAR = 252

# Helper Functions
def calculate_z_score(series, window):
    """
    Calculate the Z-score for a rolling window.

    Args:
        series (pd.Series): Input data series.
        window (int): Rolling window size.

    Returns:
        pd.Series: Z-scores for the series.
    """
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    return (series - rolling_mean) / rolling_std

def calculate_realized_volatility(data, window):
    """
    Calculate realized volatility using log returns.

    Args:
        data (pd.Series): Series of stock prices.
        window (int): Rolling window size.

    Returns:
        pd.Series: Realized volatility series.
    """
    log_returns = np.log(data / data.shift(1))
    return log_returns.rolling(window=window).std() * np.sqrt(TRADING_DAYS_YEAR)

def calculate_returns(data, periods):
    """
    Calculate percentage returns over specified periods.

    Args:
        data (pd.Series): Series of stock prices.
        periods (list): List of periods for return calculations (e.g., [5, 20, 60]).

    Returns:
        dict: A dictionary of returns for each period.
    """
    returns = {}
    for period in periods:
        returns[f"Return_{period}d"] = data.pct_change(periods=period)
    return pd.DataFrame(returns)

if __name__ == "__main__":
    # Load historical data
    file_name = "historical_data.csv"
    try:
        data = pd.read_csv(file_name, index_col=0, parse_dates=True)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found. Make sure 'fetch_data.py' was run successfully.")
        exit()

    # Process data for each ticker
    metrics = []
    periods = [5, 20, 60]  # Weekly (5d), Monthly (20d), Quarterly (60d)
    rolling_window = 20  # 20-day window for Z-score and volatility

    for ticker in set(col.split('_')[0] for col in data.columns if '_Close' in col):
        close_prices = data[f"{ticker}_Close"]

        # Calculate returns
        returns = calculate_returns(close_prices, periods)

        # Calculate realized volatility
        realized_vol = calculate_realized_volatility(close_prices, rolling_window)

        # Calculate Z-scores for prices
        z_scores = calculate_z_score(close_prices, rolling_window)

        # Combine all metrics into a single DataFrame for the ticker
        ticker_metrics = pd.concat([returns, 
                                    pd.DataFrame({"Realized_Volatility": realized_vol, 
                                                  "Z_Score": z_scores})], axis=1)
        ticker_metrics["Ticker"] = ticker
        metrics.append(ticker_metrics)

    # Combine all tickers into a single DataFrame
    all_metrics = pd.concat(metrics, keys=[m["Ticker"][0] for m in metrics])

    # Save to CSV
    output_file = "calculated_metrics.csv"
    all_metrics.to_csv(output_file)
    print(f"Metrics successfully saved to {output_file}")
