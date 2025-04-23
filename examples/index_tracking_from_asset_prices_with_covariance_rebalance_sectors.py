import pandas as pd
import numpy as np

import iq.api.iqrestapi

# Initialize API credentials
iq.api.iqrestapi.initialize_credentials("<your-api-key>")

def read_from_csv(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file into a Pandas DataFrame.
    
    Parameters:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: DataFrame containing the CSV data.
    """
    return pd.read_csv(file_path, index_col=0, parse_dates=True)

def read_csv_as_dict(file_path: str, no_header: bool) -> dict:
    """
    Reads a CSV file into a dictionary.
    Assumes the first column contains keys and the second column contains values.
    
    Parameters:
        file_path (str): Path to the CSV file.
    
    Returns:
        dict: Dictionary containing the CSV data.
    """
    if (no_header):
        df = pd.read_csv(file_path, index_col=0, header=None)
    else:
        df = pd.read_csv(file_path, index_col=0)
    return df.squeeze().to_dict()

# Load required data
assets_index_prices = read_from_csv("data/asset_prices.csv")
previous_portfolio = read_csv_as_dict("data/previous_portfolio.csv", True)
sector_weights = read_csv_as_dict("data/sector_weights.csv", True)
sector_distribution = read_csv_as_dict("data/sector_distribution.csv", True)

# Write sector weights from percentage points to [0, 1) values.
sector_weights = {asset : weight_pct / 100.0 for asset, weight_pct in sector_weights.items()}

# Print the asset prices for verification
print("Asset Index Prices:")
print(assets_index_prices.head())

# Define the date range for analysis
date_from = "2022-06-30"
date_to = "2024-07-18"

# Compute the covariance matrix
cov_matrix, cov_vector, tickers = iq.tools.quadratic_utility.compute_covariance_matrix(
    assets_index_prices=assets_index_prices,
    benchmark_column="IXIC Index",
    date_from=date_from,
    date_to=date_to,
    EMWA_halflife=252,
    maximum_missing_data_ratio_allowed=0.25,
    l2_regularization=0.01
)

# Display covariance matrix results
print("\nCovariance Matrix:")
print(cov_matrix)

print("\nCovariance Vector:")
print(cov_vector)

print("\nTickers:")
print(tickers)

# Solve for the optimal portfolio allocation
portfolio, status, error_description = iq.finance.index_tracking.solve_index_tracking(
    description="Index Tracking Example",
    assets_utility_matrix=cov_matrix,
    assets_to_benchmark_utility_vector=cov_vector,
    portfolio_size=60,
    asset_names=tickers,
    minimum_weight=0.005,
    maximum_weight=0.10,
    previous_portfolio=previous_portfolio,
    max_companies_rotation=15,
    max_sales_rotation=0.2,
    sectorial_weights=sector_weights,
    sectorial_distribution=sector_distribution,
    sectorial_weight_tolerance=0.05
)

# Display the optimal portfolio results
print("\nOptimal Portfolio Weights:")
portfolio = {asset : round(100 * weight, 4) for asset, weight in portfolio.items()}
print(portfolio)

if status == "Ok":
    print("✅ No errors encountered.")
elif error_description:
    print(f"❌ Error: {error_description}")
