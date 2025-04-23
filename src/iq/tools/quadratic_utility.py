import pandas as pd
import numpy as np


def compute_quadratic_utility(
    assets_index_prices : pd.DataFrame,
    benchmark_column: str,
    str_cost_function : str,
    date_from : str | pd.Timestamp,
    date_to : str | pd.Timestamp,
    EMWA_halflife : int = 252,
    maximum_missing_data_ratio_allowed : float = 0.0,
    l2_regularization : float = 0.0
):
    if str_cost_function not in ["covariance", "quadratic_distance"]:
        raise ValueError(f"Cost function '{str_cost_function}' is not valid. Possible values are 'covariance' or 'quadratic_distance'.")
    
    if benchmark_column not in assets_index_prices.columns:
        raise ValueError(f"Benchmark column '{benchmark_column}' is not in the provided DataFrame.")
    
    # Move benchmark column to the last position
    assets_index_prices = assets_index_prices[[col for col in assets_index_prices.columns if col != benchmark_column] + [benchmark_column]]
    

    # Make sure that the prices dataset is ordered from earliest (top row)
    # to latest date (bottom row).
    assets_index_prices = assets_index_prices.sort_index(ascending=True)
    assets_index_prices = assets_index_prices.loc[date_from:date_to]

    tickers = assets_index_prices.columns
    num_samples = assets_index_prices.shape[0]
    num_assets = assets_index_prices.shape[1] - 1

    # Filter out tickers with more than some percentage of missing data.
    if maximum_missing_data_ratio_allowed > 1 or maximum_missing_data_ratio_allowed < 0:
        raise ValueError(f"The maximum ratio of allowed missing data: {maximum_missing_data_ratio_allowed} is out of bounds [0,1].")
    missing_data_ratio_per_ticket = (
        1 - assets_index_prices.count(axis=0) / num_samples
    ).to_numpy()
    ix_tickers_without_missing_data = np.where(
        missing_data_ratio_per_ticket <= maximum_missing_data_ratio_allowed
    )[0]
    # Add to tickers without missing data any with the latest price removed.
    if str_cost_function == "quadratic_distance":
        np_latest_prices = assets_index_prices.iloc[-1].to_numpy()
        b_any_price_in_lowest_row_is_nan = np.any(np.isnan(np_latest_prices))
        if b_any_price_in_lowest_row_is_nan:
            ix_tickers_with_nan = np.where(np.isnan(np_latest_prices))[0]
            for ix_ticker in ix_tickers_with_nan:
                if ix_ticker in ix_tickers_without_missing_data:
                    ix_in_array = np.where(ix_tickers_without_missing_data == ix_ticker)
                    ix_tickers_without_missing_data = np.delete(
                        ix_tickers_without_missing_data, ix_in_array
                    )
    ix_tickers_with_missing_data = np.delete(
        np.arange(num_assets + 1),
        ix_tickers_without_missing_data
    )
    # Remove assets with missing data.
    assets_index_prices = assets_index_prices.iloc[:, ix_tickers_without_missing_data]

    # Prepare the data to compute either the covariance or the quadratic distance.
    if str_cost_function == "covariance":
        data_points = 100 * assets_index_prices.pct_change(fill_method=None)
        data_points.dropna(axis="index", how="all", inplace=True)
    elif str_cost_function == "quadratic_distance":
        np_latest_prices = assets_index_prices.iloc[-1].to_numpy()
        b_any_price_in_lowest_row_is_nan = np.any(np.isnan(np_latest_prices))
        if b_any_price_in_lowest_row_is_nan:
            ix_tickers_with_nan = np.where(np.isnan(np_latest_prices))[0]
            tickers_with_nan = tickers[ix_tickers_without_missing_data[ix_tickers_with_nan]].tolist()
            for ticker in tickers_with_nan:
                print(assets_index_prices[ticker])
            raise Exception(
                f"At {assets_index_prices.index[-1]}, the tickers: {tickers_with_nan} have a missing value in the price.\nTherefore, the quadratic distance cannot be computed."
            )
        data_points = assets_index_prices / assets_index_prices.iloc[-1]

    # Compute cost function of the data.
    np_data = data_points.to_numpy()
    b_remove_mean = str_cost_function == "covariance"
    np_cost_function_without_nan = compute_EWMA_cost_function(
        np_data, EMWA_halflife, b_remove_mean=b_remove_mean
    )
    # Add L2 regularization to the cost function.
    np_cost_function_without_nan += l2_regularization * np.eye(np_cost_function_without_nan.shape[0])
    # Fill only the cost function entries that correspond to assets 
    # with sufficient values.
    np_cost_function = np.zeros((num_assets + 1, num_assets + 1))
    # Create two lists of indices, one for the rows and one for the columns, of
    # all matrix elements without missing data.
    I, J = np.meshgrid(ix_tickers_without_missing_data, ix_tickers_without_missing_data)
    np_cost_function[I, J] = np_cost_function_without_nan

    # Fill with 0 the rows and columns of the cost function matrix
    # that correspond to assets with missing data and -1 in their
    # diagonal entries.
    for ix in ix_tickers_with_missing_data:
        np_cost_function[ix, :] = 0
        np_cost_function[:, ix] = 0
        np_cost_function[ix, ix] = -1

    cost_function_matrix = pd.DataFrame(
        np_cost_function,
        index=tickers,
        columns=tickers
    )
    cost_matrix = cost_function_matrix.iloc[:-1, :-1].to_numpy()
    benchmark_cost_vector = cost_function_matrix.iloc[:-1, -1].to_numpy()

    # We do not include the benchmark_column, the last one after the reordering, in the tickers list that we return
    return cost_matrix, benchmark_cost_vector, tickers[:-1].to_list()


def compute_covariance_matrix(
    assets_index_prices : pd.DataFrame,
    benchmark_column: str,
    date_from : str | pd.Timestamp,
    date_to : str | pd.Timestamp,
    EMWA_halflife : int = 252,
    maximum_missing_data_ratio_allowed : float = 0.25,
    l2_regularization : float = 0.0
):
    """
    Compute the covariance matrix for asset returns using exponentially weighted moving average (EWMA).

    Parameters
    ----------
    assets_index_prices : pandas.DataFrame
        DataFrame containing asset price time series data. Each column should represent
        an asset's prices indexed by dates.
    benchmark_column : str
        The name of the column in the assets_index_prices that corresponds to the benchmark to follow.
    date_from : str or pandas.Timestamp
        Start date for the covariance calculation period.
    date_to : str or pandas.Timestamp
        End date for the covariance calculation period.
    EMWA_halflife : int, default=252
        Half-life parameter for the exponential weighting, specified in trading days.
        Default is 252 (one trading year).
    maximum_missing_data_ratio_allowed : float, default=0.25
        Maximum allowed ratio of missing data points to total observations.
        Must be between 0 and 1. Default is 0.25 (25%).
    l2_regularization : float, default=0.0
        Norm-2 regularization strength to add to the diagonal elements of the 
        covariance matrix.

    Returns
    -------
    cost_matrix (numpy.ndarray): A square matrix representing the covariance between assets, excluding the benchmark asset.

    benchmark_cost_vector (numpy.ndarray): A vector containing the covariance values of each asset with the benchmark asset.

    tickers (list[str]): A list of asset tickers excluding the benchmark asset.

    """
    covariance_matrix, covariance_vector, tickers = compute_quadratic_utility(
        assets_index_prices=assets_index_prices,
        benchmark_column=benchmark_column,
        str_cost_function="covariance",
        date_from=date_from, 
        date_to=date_to,
        EMWA_halflife=EMWA_halflife,
        maximum_missing_data_ratio_allowed=maximum_missing_data_ratio_allowed,
        l2_regularization=l2_regularization
    )
    return covariance_matrix, covariance_vector, tickers


def compute_cumulative_returns_distance_matrix(
    assets_index_prices : pd.DataFrame,
    benchmark_column: str,
    date_from : str | pd.Timestamp,
    date_to : str | pd.Timestamp,
    EMWA_halflife : int = 252,
    maximum_missing_data_ratio_allowed : float = 0.25,
    l2_regularization : float = 0.0
):
    """
    Compute the quadratic distance matrix for asset returns using exponentially weighted moving average (EWMA).

    Parameters
    ----------
    assets_index_prices : pandas.DataFrame
        DataFrame containing asset price time series data. Each column should represent
        an asset's prices indexed by dates.
    benchmark_column : str
        The name of the column in the assets_index_prices that corresponds to the benchmark to follow.
    date_from : str or pandas.Timestamp
        Start date for the quadratic distance calculation period.
    date_to : str or pandas.Timestamp
        End date for the quadratic distance calculation period.
    EMWA_halflife : int, default=252
        Half-life parameter for the exponential weighting, specified in trading days.
        Default is 252 (one trading year).
    maximum_missing_data_ratio_allowed : float, default=0.25
        Maximum allowed ratio of missing data points to total observations.
        Must be between 0 and 1. Default is 0.25 (25%).
    l2_regularization : float, default=0.0
        Norm-2 regularization strength to add to the diagonal elements of the 
        cumulative returns distance matrix.

    Returns
    -------
    cost_matrix (numpy.ndarray): A square matrix representing the quadratic distance between assets, excluding the benchmark asset.

    benchmark_cost_vector (numpy.ndarray): A vector containing the quadratic distance values of each asset with the benchmark asset.

    tickers (list[str]): A list of asset tickers excluding the benchmark asset.

    """
    distance_matrix, distance_vector, tickers = compute_quadratic_utility(
        assets_index_prices=assets_index_prices,
        benchmark_column=benchmark_column,
        str_cost_function="quadratic_distance",
        date_from=date_from, 
        date_to=date_to,
        EMWA_halflife=EMWA_halflife,
        maximum_missing_data_ratio_allowed=maximum_missing_data_ratio_allowed,
        l2_regularization=l2_regularization
    )
    return distance_matrix, distance_vector, tickers


def compute_EWMA_cost_function(data, halflife, b_remove_mean):
    """Compute the Exponentially Weigthed Moving Average of a set of data samples.

    Parameters
    ----------
    data : np.ndarray[(n_samples, n_assets), dtype=np.double]
        Matrix of data samples. Each row contains one sample.
    halflife : float
        Half-life of the exponential weights.
    b_remove_mean : bool
        If True, then remove the mean of all features before computing
        the EMWA.

    Returns
    -------
    cost : np.ndarray[(n_assets, n_assets), dtype=np.double]
        EWMA of the matrix of samples.

    """
    T = data.shape[0]  # Number of time periods.

    # Exponential weights.
    exp_weights = 2.0 ** ( - np.flipud(np.arange(T)) / halflife )

    if b_remove_mean:
        means = np.nanmean(data, axis=0, keepdims=True)
        data = data - means

    # Boolean matrix with missing data marked as 0 and non-missing as 1.
    b_data = np.ones_like(data)
    b_data[np.isnan(data)] = 0
    # Fill missing data values in the sample matrix to 0.
    data = np.nan_to_num(data, nan=0)

    # Estimate the cost function matrix. The entries that had a missing value
    # have been replaced with 0, so they will modify the cost function.
    cost = np.einsum('ti,t,tj->ij', data, exp_weights, data)
    normalization = np.einsum('ti,t,tj->ij', b_data, exp_weights, b_data)
    cost = cost / normalization
    return cost
