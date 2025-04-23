# 4.- Index Tracking tools and complete examples
So far we have used synthetic data for the Index Tracking examples. But as we have defined, the utility function matrix must be a covariance or quadratic distance matrix, which must be calculated from a price history. 

We provide a tool to calculate this data from a covariance history, which we explain in this section. 

## 4.1.- Calculate the covariance matrix
The `compute_covariance_matrix` function computes the covariance matrix of asset returns using an **Exponentially Weighted Moving Average (EWMA)** approach. This method gives greater importance to recent data points while calculating the covariance, making it useful for financial modeling and risk management.

### Function Signature

```python
import pandas as pd

def compute_covariance_matrix(
    assets_index_prices: pd.DataFrame,
    benchmark_column: str,
    date_from: str | pd.Timestamp,
    date_to: str | pd.Timestamp,
    EMWA_halflife: int = 252,
    maximum_missing_data_ratio_allowed: float = 0.25,
    l2_regularization: float = 0.0
):
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `assets_index_prices` | `pd.DataFrame` | N/A | A DataFrame containing time series price data for different assets. Each column represents an asset, and the index represents the date. |
| `benchmark_column` | `str` | N/A | The name of the benchmark asset column used for comparison. |
| `date_from` | `str` or `pd.Timestamp` | N/A | The start date for the covariance calculation period. |
| `date_to` | `str` or `pd.Timestamp` | N/A | The end date for the covariance calculation period. |
| `EMWA_halflife` | `int` | `252` | The half-life parameter for the exponential weighting, measured in trading days. The default is 252, corresponding to one trading year. |
| `maximum_missing_data_ratio_allowed` | `float` | `0.25` | The maximum allowable ratio of missing data points for any asset before exclusion. The default is 0.25 (25%). |
| `l2_regularization` | `float` | `0.0` | The L2 regularization strength, which adds a small value to the diagonal elements of the covariance matrix to improve numerical stability. |

### Returns

The function returns three objects:

- **`cost_matrix`** (`numpy.ndarray`): A square matrix representing the covariance between assets, excluding the benchmark asset.
- **`benchmark_cost_vector`** (`numpy.ndarray`): A vector containing the covariance values of each asset with the benchmark asset.
- **`tickers`** (`list[str]`): A list of asset tickers excluding the benchmark asset.

### Key Features

- **Exponentially Weighted Moving Average (EWMA):**
  - Recent observations are given greater importance compared to older ones.
  - Helps in tracking changes in asset volatility more efficiently.

- **Handles Missing Data:**
  - Assets with too many missing values (above `maximum_missing_data_ratio_allowed`) are excluded from the computation.

- **L2 Regularization:**
  - Helps in conditioning the covariance matrix to avoid numerical instabilities.
  - Useful when dealing with highly correlated assets.

### Example Usage

```python
import pandas as pd
from datetime import datetime
from iq.tools.quadratic_utility import compute_covariance_matrix

# Sample Data
data = {
    "Asset_A": [100, 102, 101, 103, 105],
    "Asset_B": [50, 51, 52, 50, 49],
    "Asset_C": [200, 198, 202, 205, 210]
}
dates = pd.date_range(start="2024-01-01", periods=5, freq='D')
assets_df = pd.DataFrame(data, index=dates)

# Compute covariance matrix
cost_matrix, benchmark_cost_vector, tickers = compute_covariance_matrix(
    assets_index_prices=assets_df,
    benchmark_column="Asset_A",
    date_from="2024-01-01",
    date_to="2024-01-05"
)

print("Cost Matrix:", cost_matrix)
print("Benchmark Cost Vector:", benchmark_cost_vector)
print("Tickers:", tickers)
```


## 4.2.- Calculate the quadratic distance matrix

The `compute_cumulative_returns_distance_matrix` function computes the quadratic distance matrix of asset returns using an **Exponentially Weighted Moving Average (EWMA)** approach. This method assigns greater importance to recent data points when calculating quadratic distances, making it valuable for financial modeling and risk management.

### Function Signature

```python
import pandas as pd

def compute_cumulative_returns_distance_matrix(
    assets_index_prices: pd.DataFrame,
    benchmark_column: str,
    date_from: str | pd.Timestamp,
    date_to: str | pd.Timestamp,
    EMWA_halflife: int = 252,
    maximum_missing_data_ratio_allowed: float = 0.25,
    l2_regularization: float = 0.0
):
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `assets_index_prices` | `pd.DataFrame` | N/A | A DataFrame containing time series price data for different assets. Each column represents an asset, and the index represents the date. |
| `benchmark_column` | `str` | N/A | The name of the benchmark asset column used for comparison. |
| `date_from` | `str` or `pd.Timestamp` | N/A | The start date for the quadratic distance calculation period. |
| `date_to` | `str` or `pd.Timestamp` | N/A | The end date for the quadratic distance calculation period. |
| `EMWA_halflife` | `int` | `252` | The half-life parameter for the exponential weighting, measured in trading days. The default is 252, corresponding to one trading year. |
| `maximum_missing_data_ratio_allowed` | `float` | `0.25` | The maximum allowable ratio of missing data points for any asset before exclusion. The default is 0.25 (25%). |
| `l2_regularization` | `float` | `0.0` | The L2 regularization strength, which adds a small value to the diagonal elements of the quadratic distance matrix to improve numerical stability. |

### Returns

The function returns three objects:

- **`cost_matrix`** (`numpy.ndarray`): A square matrix representing the quadratic distance between assets, excluding the benchmark asset.
- **`benchmark_cost_vector`** (`numpy.ndarray`): A vector containing the quadratic distance values of each asset with the benchmark asset.
- **`tickers`** (`list[str]`): A list of asset tickers excluding the benchmark asset.

### Key Features

- **Exponentially Weighted Moving Average (EWMA):**
  - Recent observations are given greater importance compared to older ones.
  - Helps in tracking changes in asset distance relationships more efficiently.

- **Handles Missing Data:**
  - Assets with too many missing values (above `maximum_missing_data_ratio_allowed`) are excluded from the computation.

- **L2 Regularization:**
  - Helps in conditioning the distance matrix to avoid numerical instabilities.
  - Useful when dealing with highly correlated assets.

### Example Usage

```python
import pandas as pd
from datetime import datetime
from iq.tools.quadratic_utility import compute_cumulative_returns_distance_matrix

# Sample Data
data = {
    "Asset_A": [100, 102, 101, 103, 105],
    "Asset_B": [50, 51, 52, 50, 49],
    "Asset_C": [200, 198, 202, 205, 210]
}
dates = pd.date_range(start="2024-01-01", periods=5, freq='D')
assets_df = pd.DataFrame(data, index=dates)

# Compute cumulative returns distance matrix
cost_matrix, benchmark_cost_vector, tickers = compute_cumulative_returns_distance_matrix(
    assets_index_prices=assets_df,
    benchmark_column="Asset_A",
    date_from="2024-01-01",
    date_to="2024-01-05"
)

print("Cost Matrix:", cost_matrix)
print("Benchmark Cost Vector:", benchmark_cost_vector)
print("Tickers:", tickers)
```

## 4.3.- Example: calculate a portfolio from historical asset prices using covariance

This code can be found in [index_tracking_from_asset_prices_with_covariance.py](../examples/index_tracking_from_asset_prices_with_covariance.py). It uses the data stored in [asset_prices.csv](../examples/data/asset_prices.csv) to calculate the covariances matrix and vector, that are used to launch the Index Tracking computation.

```python
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
```

## 4.4.- Example: rebalancing a previous portfolio and adding sectorial constraints
Here we go a step forward, to not only build a portfolio from scratch, also creating one from a previous one, imposing rebalance conditions, and also sector conditions.

The code that we show here is in [index_tracking_from_asset_prices_with_covariance_rebalance_sectors.py](../examples/index_tracking_from_asset_prices_with_covariance_rebalance_sectors.py):

```python
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

```