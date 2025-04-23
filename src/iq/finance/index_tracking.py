import numpy as np

from iq.api import iqrestapi
from iq.api import validate


def build_matrix_of_sector_restrictions(
    asset_names: np.ndarray,
    sectorial_weights: dict,
    sectorial_distribution: dict,
    sectorial_weight_tolerance: float
):
    sectors = np.array(list(sectorial_weights.keys()))
    num_sectors = sectors.size
    num_assets = asset_names.size

    # Make matrix of belongings.
    matrix_of_belongings = np.zeros((num_sectors, num_assets), dtype=np.double)
    for i, ticker in enumerate(asset_names):
        if ticker not in sectorial_distribution:
            raise ValueError(f"The ticker {ticker} is in the assets of the assets utility matrix but is not included in the tickers of the sector restrictions.")
        sector = sectorial_distribution[ticker]
        ix_of_sector = np.where(sectors == sector)[0][0]
        matrix_of_belongings[ix_of_sector, i] = 1.0

    np_sectorial_weights = np.zeros(num_sectors)
    for i, sector in enumerate(sectors):
        np_sectorial_weights[i] = sectorial_weights[sector]

    # Write restrictions in matrix vector form.
    r = np.concatenate((matrix_of_belongings, -matrix_of_belongings), axis=0)
    r_min = np.zeros(2 * num_sectors)
    # 1: weights must be higher than, e.g, 95% of the current weight.
    r_min[:num_sectors] = np_sectorial_weights * (1 - sectorial_weight_tolerance)
    # 2: weights must be lower than, e.g, 105% of the current weight.
    r_min[num_sectors:] = - np_sectorial_weights * (1 + sectorial_weight_tolerance)

    return r, r_min


def solve_index_tracking(
    assets_utility_matrix,
    assets_to_benchmark_utility_vector,
    portfolio_size,
    asset_names,
    minimum_weight=0.0, maximum_weight=1.0,
    linear_constraints_matrix=None, lower_bounds_vector=None, upper_bounds_vector=None,
    previous_portfolio=None,
    max_companies_rotation=-1,
    max_sales_rotation=-1.0,
    sectorial_weights=None,
    sectorial_distribution=None,
    sectorial_weight_tolerance=None,
    sum_of_portfolio_weights=1.0,
    random_number_generator_seed=123321,
    description=""
):
    """Solve the index tracking (IT) problem using population annealing.

    The IT problem tries to minimize the tracking error, which
    measures the standard deviation between the differences in
    the returns between the index and tracker portfolio

        TE**2 = Var( r_I - r_p) = Var(r_I) - 2 sum_i Cov(r_I, r_i) w_i
                + sum_ij w_i Cov(r_i, r_j) w_j
              = Var(r_I) - 2 sum_i g_i w_i + sum_ij w_i cov_ij w_j

    with w the weights that define the tracker portfolio.

    The solver accepts several constraints:
    1. linear_constraints_matrix minimum return constraint:
        r @ w >= r_min
    2. linear_constraints_matrix maximum price constraint:
        p @ w <= p_max
        This constraint can be set with r = -p and r_min = -p_max.
    3. In general, any set of linear inequality constraints of the form:
        linear_constraints_matrix @ w >= a_min
    with linear_constraints_matrix a matrix where every row is a different constraint and a_min is a vector.
    4. linear_constraints_matrix maximum norm-0 rotation constraint:
        count( previous_portfolio_i != 0 and w_i == 0 ) <= max_companies_rotation
    5. linear_constraints_matrix maximum norm-1 rotation constraint:
        np.linalg.norm(previous_portfolio - w, ord=1) <= max_sales_rotation

    To solve the IT problem we write it as an MIQP problem:

    min_w   w @ assets_utility_matrix @ w - assets_to_benchmark_utility_vector @ w + Var(r_I)
    with    w_i either a real number or zero
    s.t.    count( w_i != 0) = portfolio_size
            minimum_weight <= w_i <= maximum_weight
            sum_i w_i = 1

    if also `r` is not None, then solve with the additional condition

    s.t.    sum_i w_i * r_i >= r_min

    if `max_companies_rotation` is not None, then solve also with

    s.t.    count( previous_portfolio_i != 0 and w_i == 0 ) <= max_companies_rotation

    if `max_sales_rotation` is not None, then solve also with

    s.t.    np.sum(np.abs(previous_portfolio - w)) / 2 <= max_sales_rotation

    Parameters
    ----------
    assets_utility_matrix : ndarray[(num_assets, num_assets), dtype=np.double]
        Quadratic utility matrix between all assets. If some assets contain missing
        data and they should be excluded from the tracker portfolio, they
        will have a -1 a the corresponding diagonal elements and 0's in their
        corresponding rows and columns.
    assets_to_benchmark_utility_vector : ndarray[(num_assets,), dtype=np.double]
        Quadratic utility vector between the index and assets' returns. If some assets
        contain missing data and they should be excluded from the tracker
        portfolio, they will have a 0 in their corresponding elements.
    portfolio_size : int
        Number of allowed nonzero weigths in the solution portfolio.
    asset_names : ndarray[(num_assets,), dtype=str]
        List with the ticker names of the assets of the assets utility matrix. It is
        assumed that this list coincides with the tickers of the
        assets_to_benchmark_utility_vector and of the r matrix if it is given.
    minimum_weight : float, default=0.0
        Lower bound for the elements of the solution portfolio.
    maximum_weight : float, default=1.0
        Upper bound for the elements of the solution portfolio.
    linear_constraints_matrix : ndarray[(num_inequality_constraints, num_assets), dtype=np.double], default=None
        Matrix of linear inequality constraints.
    lower_bounds_vector : ndarray[(num_inequality_constraints), dtype=np.double], default=None
        Vector with the minimum values of the linear inequality constraints.
    upper_bounds_vector : ndarray[(num_inequality_constraints), dtype=np.double], default=None
        Vector with the maximum values of the linear inequality constraints.
    previous_portfolio : dict, default=None
        Vector to impose a maximum change constraint. See above for description.
    max_companies_rotation : int, default=-1
        Maximum number of weights that were not zero in the previous portfolio
        and might be zero in the optimal portfolio. If negative, then this
        constraint is not active.
    max_sales_rotation : int, default=-1.0
        Maximum total weights that is sold from the previous portfolio to build the
        optimal portfolio. If negative, then this constraint is not active.
    sectorial_weights : dict, optional, default=None
        Dictionary of weight inside the benchmark index of each sector.
    sectorial_distribution : dict, optional, default=None
        Dictionary of sector belonging for each asset. E.g. {"APPL": "Technology",
        "CXO": "Industry", "MSFT": "Technology"}.
    sectorial_weight_tolerance : float, optional, default=None
        Maximum relative weight deviation of the sector weight in the portfolio
        from the sector weight in the index.
    random_number_generator_seed : int, optional, default=123321
        Random number generator seed for Monte Carlo
    description : str, optional, default=""
        Small descriptive name for this computation.

    Returns
    -------
    w_opt : ndarray[(num_assets,), dtype=np.double]
        Optimal solution vector.

    status : str, {"Ok", "Failed"}
        Status of the computation. 

    error_description : str
        Detailed description of the error that happened, if any.

    """

    # Initial error codes.
    status = "Ok"
    error_description = None
    # Placeholder if computation fails.
    optimal_portfolio = {"No assets": -1.0}

    # Array and input arguments validation.
    try:
        MAX_ARRAY_DIM = 2048

        num_assets = assets_utility_matrix.shape[0]
        # Do a check of the utility matrix without the semidefinite positive check,
        # because missing data makes it non semidefinite positive.
        validate.validate_matrix(
            assets_utility_matrix, "assets_utility_matrix",
            MAX_ARRAY_DIM, MAX_ARRAY_DIM,
            b_A_must_be_square=True,
            b_A_must_be_symmetric=True,
            b_A_must_be_semidefinite_positive=False
        )
        validate.validate_vector(
            assets_to_benchmark_utility_vector, "assets_to_benchmark_utility_vector",
            num_assets,
            b_size_of_a_must_be_eq_to_max_size=True,
            name_of_variable_with_equivalent_size=f"the dimensions of the assets utility matrix"
        )
        asset_names = validate.validate_vector(
            asset_names, "asset_names",
            num_assets,
            b_size_of_a_must_be_eq_to_max_size=True,
            name_of_variable_with_equivalent_size=f"the dimensions of the assets utility matrix"
        )

        # Remove assets with missing data. These are the ones that have -1 in the
        # diagonal elements of the assets_utility_matrix.
        ix_of_assets_without_missing_data = np.where(np.diag(assets_utility_matrix) != -1)[0]
        num_assets_without_missing_data = ix_of_assets_without_missing_data.size
        I, J = np.meshgrid(ix_of_assets_without_missing_data, ix_of_assets_without_missing_data)
        assets_utility_matrix_without_missing_data = np.ascontiguousarray(assets_utility_matrix[I, J])

        # Check again that the remainding matrix is semidefinite positive.
        validate.validate_matrix(
            assets_utility_matrix_without_missing_data, "assets_utility_matrix_without_missing_data",
            MAX_ARRAY_DIM, MAX_ARRAY_DIM,
            b_A_must_be_square=True,
            b_A_must_be_symmetric=True,
            b_A_must_be_semidefinite_positive=True
        )

        b_there_are_linear_inequalities = linear_constraints_matrix is not None
        if b_there_are_linear_inequalities:
            if lower_bounds_vector is None and upper_bounds_vector is None:
                raise ValueError("There is a matrix of linear inequalities 'linear_constraints_matrix', but both 'lower_bounds_vector' and 'upper_bounds_vector' are None.")

            linear_constraints_matrix = validate.validate_matrix(linear_constraints_matrix, "linear_constraints_matrix", MAX_ARRAY_DIM, MAX_ARRAY_DIM)
            number_of_linear_inequalities = linear_constraints_matrix.shape[0]
            if linear_constraints_matrix.shape[1] != num_assets:
                raise ValueError(f"The linear inequalities in the matrix linear_constraints_matrix, linear_constraints_matrix.shape[1]={linear_constraints_matrix.shape[1]}, do not have the same size as the dimensions of the assets utility matrix.")

            lower_bounds_vector = validate.validate_vector(
                lower_bounds_vector, "lower_bounds_vector",
                number_of_linear_inequalities,
                b_size_of_a_must_be_eq_to_max_size=True,
                name_of_variable_with_equivalent_size="the number of linear inequalities"
            )
            upper_bounds_vector = validate.validate_vector(
                upper_bounds_vector, "upper_bounds_vector",
                number_of_linear_inequalities,
                b_size_of_a_must_be_eq_to_max_size=True,
                name_of_variable_with_equivalent_size="the number of linear inequalities"
            )
    except Exception as error_description:
        status = "Failed"
        error_description = "Validation: " + repr(error_description)
        return optimal_portfolio, status, error_description

    if portfolio_size <= 0 or portfolio_size >= num_assets_without_missing_data:
        status = "Failed"
        error_description = f"Feasibility: Portfolio_size={portfolio_size} is not valid. It must be in the range: 0 < portfolio_size < {num_assets_without_missing_data}, with {num_assets_without_missing_data} the number of assets in the utility matrix without missing data."
        return optimal_portfolio, status, error_description

    try:

        json_args={
            "assets_utility_matrix": assets_utility_matrix.tolist(),
            "assets_to_benchmark_utility_vector": assets_to_benchmark_utility_vector.tolist(),
            "portfolio_size": validate.integer(portfolio_size, 1, num_assets-1),
            "asset_names": asset_names.tolist(),
            "minimum_weight": validate.real(minimum_weight),
            "maximum_weight": validate.real(maximum_weight),
            "sum_of_portfolio_weights": validate.real(sum_of_portfolio_weights),
            "random_number_generator_seed": validate.integer(random_number_generator_seed, 0, 0xfffffff),
            "description": validate.string(description)
        }

        if b_there_are_linear_inequalities:
            json_args |= { "linear_constraints_matrix": linear_constraints_matrix.tolist() }
            json_args |= { "lower_bounds_vector": lower_bounds_vector.tolist() }
            json_args |= { "upper_bounds_vector": upper_bounds_vector.tolist() }

        if previous_portfolio is not None:
            validate.dictionary(previous_portfolio)
            json_args |= { "previous_portfolio": previous_portfolio}
            json_args |= { "max_companies_rotation": validate.integer(max_companies_rotation, -1, np.inf)}
            json_args |= { "max_sales_rotation": validate.real(max_sales_rotation) }

        if sectorial_distribution is not None:
            if sectorial_weight_tolerance is None or sectorial_weights is None:
                raise ValueError("The parameter 'sectorial_distribution' was introduced, but either 'sectorial_weight_tolerance' and/or 'sectorial_weights' are None.")
            validate.dictionary(sectorial_distribution)
            validate.dictionary(sectorial_weights)
            json_args |= { "sectorial_distribution": sectorial_distribution }
            json_args |= { "sectorial_weights": sectorial_weights }
            json_args |= { "sectorial_weight_tolerance": validate.real(sectorial_weight_tolerance) }
    except Exception as error:
        status = "Failed"
        error_description = "Validation: ", repr(error)
        return optimal_portfolio, status, error_description

    r_post = iqrestapi.post(
        "v1/iq-finance/index-tracking",
        json= json_args,
    )
    if "error_description" in r_post:
        error_description = r_post["error_description"]
    return r_post["named_solution"], r_post["status"], error_description