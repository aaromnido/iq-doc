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
