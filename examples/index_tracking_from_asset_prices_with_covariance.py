import pandas as pd
import numpy as np

import iq.api.iqrestapi
import iq.tools.quadratic_utility 
import iq.finance.index_tracking 

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

# Load required data
assets_index_prices = read_from_csv("data/asset_prices.csv")

# Print the asset prices for verification
print("\nAsset Index Prices:")
print(assets_index_prices.head())

# Define the date range for analysis
date_from = "2022-06-30"
date_to = "2024-07-18"

# Compute the covariance matrix
cov_matrix, cov_vector, tickers =iq.tools.quadratic_utility.compute_covariance_matrix(
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
    minimum_weight=0.01,
    maximum_weight=0.55
)

# Format and display the optimal portfolio results
print("\nOptimal Portfolio Weights:")
portfolio = {asset: round(100 * weight, 4) for asset, weight in portfolio.items()}
print(portfolio)

# Check status and print appropriate messages
if status == "Ok":
    print("✅ No errors encountered.")
elif error_description:
    print(f"❌ Error: {error_description}")