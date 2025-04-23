# 3. Index Tracking SDK

The **Inspiration-Q SDK** simplifies interactions with the API by abstracting low-level API calls, making it easier to create computations and retrieve results.

## 3.1. Installing a Python Environment

To ensure a clean and isolated development environment, create a Python virtual environment named `iq-index-tracking` and install the required dependencies (`numpy` and `requests`). Below are multiple ways to set up the environment:

### 1. Using `conda`
```bash
conda create --name iq-index-tracking python=3.11 numpy requests pandas
conda activate iq-index-tracking
```

### 2. Using `virtualenv`
```bash
pip install virtualenv  # If not installed
virtualenv iq-index-tracking
source iq-index-tracking/bin/activate  # On macOS/Linux
# On Windows: iq-index-tracking\Scripts\activate
pip install numpy requests
```

### 3. Using `venv` (Standard Library)
```bash
python -m venv iq-index-tracking
source iq-index-tracking/bin/activate  # On macOS/Linux
# On Windows: iq-index-tracking\Scripts\activate
pip install numpy requests
```

### 4. Using `pipenv`
```bash
pip install pipenv  # If not installed
pipenv --python 3.9
pipenv install numpy requests
pipenv shell
```

### 5. Using `poetry`
```bash
pip install poetry  # If not installed
poetry new iq-index-tracking && cd iq-index-tracking
poetry add numpy requests
poetry shell
```

## 3.2. SDK Setup

There are three ways to install the **Inspiration-Q SDK**:

### 1. Using `make install`
If you have `make` installed, you can simply run:
```bash
make install
```
#### Installing `make`
- **macOS** (comes pre-installed with Xcode Command Line Tools):
  ```bash
  xcode-select --install
  ```
- **Ubuntu/Linux**:
  ```bash
  sudo apt update && sudo apt install make
  ```
- **Windows** (via Chocolatey):
  ```powershell
  choco install make
  ```

### 2. Using `pip install .`
If you are inside the SDK directory, you can install it using:
```bash
pip install .
```

### 3. Using `pip install -r requirements.txt`
To install dependencies from a `requirements.txt` file, assuming you have already created a Python environment as explained in **[Installing a Python Environment](#31-installing-a-python-environment)**:
```bash
pip install -r requirements.txt
```

## 3.3. Examples with the SDK

Here is how you can use the SDK to perform index tracking computations:

```python
import numpy as np
import iq.api.iqrestapi
import iq.finance.index_tracking

iq.api.iqrestapi.initialize_credentials("YOUR_API_KEY")

# Define input values from the previous example
assets_utility_matrix = np.array([
    [3.5717, -0.7955, 0.1256, 1.0639, -0.4019, 0.6864, -0.1395, 0.1712, 0.6755, 2.5129],
    [-0.7955, 5.4155, -2.0174, 0.0304, 2.5502, 0.5643, -1.2933, -0.5751, 3.5942, 1.8957],
    [0.1256, -2.0174, 6.3653, 2.2579, -3.6580, -0.4503, -1.0273, -0.2157, -0.3865, -1.5332],
    [1.0639, 0.0304, 2.2579, 3.9943, -1.7805, 0.5688, -1.1084, -0.1515, -2.5177, 1.0882],
    [-0.4019, 2.5502, -3.6580, -1.7805, 8.3905, 2.2223, -1.7717, -1.3493, 3.4486, 0.0299],
    [0.6864, 0.5643, -0.4503, 0.5688, 2.2223, 4.4492, -2.7139, -0.8300, -0.7273, -0.3117],
    [-0.1395, -1.2933, -1.0273, -1.1084, -1.7717, -2.7139, 4.0927, 2.3976, 0.2705, -0.2959],
    [0.1712, -0.5751, -0.2157, -0.1515, -1.3493, -0.8300, 2.3976, 3.8646, -0.2605, -1.9647],
    [0.6755, 3.5942, -0.3865, -2.5177, 3.4486, -0.7273, 0.2705, -0.2605, 9.0839, 1.4491],
    [2.5129, 1.8957, -1.5332, 1.0882, 0.0299, -0.3117, -0.2959, -1.9647, 1.4491, 5.4074]
])

assets_to_benchmark_utility_vector = np.array([0.0518, -0.3357, 0.3207, 0.4175, 0.3314, -0.1354, -0.4340, 0.2906, 0.1588, -0.4411])
portfolio_size = 8
asset_names = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
random_number_generator_seed = 359133650

def solve_portfolio():
    portfolio, status, error_description = iq.finance.index_tracking.solve_index_tracking(
        description="Index Tracking Example",
        assets_utility_matrix=assets_utility_matrix,
        assets_to_benchmark_utility_vector=assets_to_benchmark_utility_vector,
        portfolio_size=portfolio_size,
        asset_names=asset_names,
        minimum_weight=0.02,
        maximum_weight=0.55,
        previous_portfolio=None,
        max_companies_rotation=None,
        max_sales_rotation=None
    )
    portfolio = {asset : round(100 * weight, 4) for asset, weight in portfolio.items()}
    print("Optimal Portfolio Weights:", portfolio)
    if status == "Ok":
        print("✅ No errors encountered.")
    elif error_description:
        print(f"❌ Error: {error_description}")

solve_portfolio()
```

This script initializes the SDK, sets up input data, and calls `solve_index_tracking` to compute the optimal portfolio weights.

You can find more examples in the [Examples Folder](../examples/). The specific example shown here is in [index_tracking_sdk.py](../examples/index_tracking_sdk.py).

