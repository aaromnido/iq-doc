# 1. Index Tracking Test

## 1.1. The Index Tracking Problem

The **index tracking problem** involves selecting a portfolio of $k$ assets from a benchmark index such that the portfolio's returns closely track the returns of the index. This closeness is measured using the **tracking error (TE)**, which is defined as the standard deviation of the difference between the returns of the index and the portfolio:

$$
\mathrm{TE}^2 = \textrm{Var}\left[r_I(t) - r_p(t)\right],
$$

where $r_I(t)$ and $r_p(t)$ represent the returns of the index and portfolio, respectively, over a given time window.

A **tracker portfolio** is represented by a vector of weights $\vec{\omega}$, where each element $\omega_i$ denotes the allocation weight of asset $i$ in the portfolio. Using this notation, the **tracking error** can be rewritten as:

$$
\textrm{TE}^2 = \sigma_I^2 - 2 \vec{\omega}\,\vec{g} + \vec{\omega}\,\sigma\,\vec{\omega},
$$

where:
- $\sigma_I^2$ is the variance of the index's returns,
- $\vec{g}$ is the vector of covariances between asset returns and index returns,
- $\sigma$ is the covariance matrix of asset returns.

## 1.2. Definition of tracking error
The Tracking Error (TE) of a tracker portfolio with respect to a benchmark index is defined as the standard deviation of the difference between the returns of the index $r_I(t)$ and of the portfolio $r_p(t)$ during some time window $\Delta T$:

$$
\textrm{TE} = \textrm{Std}\left[ r_I(t) - r_p(t) \right]_{t \in \Delta T} = 
$$

$$
= \sqrt{\textrm{Var}\left[ r_I(t) - r_p(t) \right]_{t \in \Delta T}}.
$$

Because the tracking error is always greater or equal to zero, we know that the portfolio that minimizes the squared tracking error will also minimize the tracking error. Thus, we select the squared tracking error as the function that we want to minimize

$$
\textrm{TE}^2 = \textrm{Var}\left[ r_I(t) - r_p(t) \right],
$$

where we do not specify the time window $\Delta T$ for the sake of simplicity. We can decompose this variance into a sum of two volatilities minus a covariance between the index and portfolio returns. We will temporarily not write the $(t)$ terms for clarity:

$$
\begin{split}
    \textrm{TE}^2 &= \textrm{Var}\left[ r_I - r_p \right] \\
    &= \textrm{E}\left[ \left(r_I - r_p - \textrm{E}\left[ r_I - r_p\right]\right)^2 \right] \\
    &= \textrm{E}\left[ \left(r_I - r_p - \textrm{E}\left[ r_I \right] + \textrm{E}\left[ r_p\right]\right)^2 \right] \\
    &= \textrm{E}\Big[ r_I^2 + r_p^2 + \textrm{E}\left[ r_I \right]^2 + \textrm{E}\left[ r_p\right]^2 \\
    &\quad  - 2r_I r_p - 2r_I\textrm{E}\left[ r_I \right] + 2r_I\textrm{E}\left[ r_p \right] \\
    &\quad + 2r_p\textrm{E}\left[ r_I \right] - 2r_p\textrm{E}\left[ r_p \right] - 2\textrm{E}\left[ r_I \right] \textrm{E}\left[ r_p \right] \Big]
\end{split}
$$

Using the fact that $\textrm{E}\Big[ x\, \textrm{E}\left[ y \right]\Big] = \textrm{E}\left[ x \right]\textrm{E}\left[ y \right]$, the tracking error becomes:

$$
\textrm{TE}^2 = \textrm{Var}\left[ r_I(t)\right] + \textrm{Var}\left[ r_p(t)\right] - 2\,\textrm{Cov}\left[ r_I(t), r_p(t)\right].
$$

Thus, we can write the tracking error as the sum of the volatilities of the index and the tracker minus the covariance of both returns.

If the portfolio is composed of a series of assets with some defined allocation weights inside the portfolio, then we can decompose the returns of the portfolio in terms of the returns of the assets inside the index

$$
    r_p(t) = \sum_i \omega_i(t) r_i(t),
$$

with $\omega_i(t)$ and $r_i(t)$ the allocation weight and return of asset $i$ at time $t$, respectively. In practice, one assumes that the allocation weights are kept constant during the in-sample period

$$
    r_p(t) = \sum_i \omega_i r_i(t).
$$

Therefore, the tracking error is

$$
    \textrm{TE}^2 = \textrm{Var}\left[ r_I(t)\right] + \textrm{Var}\left[ \sum_i \omega_i r_i(t)\right] - 2\,\textrm{Cov}\left[ r_I(t), \sum_i \omega_i r_i(t)\right].
$$

Because the returns of the portfolio are a linear combination of the returns of the assets, we can further decompose the volatility of the portfolio and the covariance into covariances of the assets returns

$$
    \begin{split}
        \textrm{Cov}\left[ r_I, \sum_i \omega_i r_i\right] &= \sum_i \omega_i \textrm{Cov}\left[ r_I(t), r_i(t)\right],
    \end{split}
$$

and similarly for the variance of the portfolio

$$
    \textrm{Var}\left[ \sum_i \omega_i r_i\right] = \sum_{ij} \omega_i \omega_j \textrm{Cov}\left[ r_i(t), r_j(t)\right].
$$

Thus, we can write the tracking error as

$$
    \textrm{TE}^2 = \textrm{Var}\left[ r_I(t) \right] - 2 \sum_i \omega_i \textrm{Cov}\left[ r_I(t), r_i(t) \right] + \sum_{ij} \omega_i \omega_j \textrm{Cov}\left[ r_i(t), r_j(t) \right].
$$

We can join these terms defining a vector $\vec{g}$ of covariances between the index' and assets' returns

$$
    g_i = \textrm{Cov}\left[ r_I(t), r_i(t) \right]
$$

and the covariance matrix of the assets' returns $\sigma$

$$
    \sigma_{ij} = \textrm{Cov}\left[ r_i(t), r_j(t) \right].
$$

Thus, the squared tracking error is

$$
    \textrm{TE}^2 = \textrm{Var}\left[ r_I(t) \right] - 2 \vec{g}^T \vec{\omega} + \vec{\omega}^T \sigma \vec{\omega}.
$$

### Interpretation of the Tracking Error

The above definition of the squared tracking error contains the sum of two volatilities. This expression can be interpreted as:

1. The volatility of the index is just a constant term that does not play any role when minimizing the tracking error.
2. The term $-\vec{g}^T \vec{\omega}$ makes that the tracker portfolio will try to have assets with a good correlation with the index.
3. The term $\vec{\omega}^T \sigma \vec{\omega}$ makes that the tracker portfolio will try to lower its risk or volatility by diversifying its allocation weights into uncorrelated assets.



## 1.3. Constraints in index tracking
A portfolio manager must comply with specific constraints while constructing a tracker portfolio, considering both **transaction cost reduction** and **weight allocation** constraints. **iQ-Finance** provides the following constraints:

### 1. Constraints for Reducing Transaction Costs
These constraints aim to minimize costs when rebalancing a portfolio by considering the previous portfolio (`previous_portfolio` in the API):
- **Ticker rotation**: Limits the number of assets that can leave the portfolio in a rebalance, defined as `max_companies_rotation`.
- **Turnover rotation**: Limits the weight of assets sold during rebalancing, defined as `max_sales_rotation`. Mathematically,

$$
\frac{1}{2} \sum_i |w_i(t) - w_i(t-1)| \leq \text{max sales rotation}.
$$

### 2. Constraints for Weight Allocation
- **`maximum_weight`** and **`minimum_weight`**: Define the maximum and minimum allocation weight of each asset in the portfolio. These values range from `0` to `1` (e.g., an 8% allocation is written as `0.08`).



## 1.4. Index Tracking API

The **Inspiration-Q Index Tracking API** enables users to create and monitor index tracking computations for portfolio management. It is available at:

```
https://www.inspiration-q.com/api/v1/iq-finance/index-tracking
```

For detailed usage instructions, refer to **[Accessing the API](doc/2-accessing-the-api.md)**. Below is an overview of the API's input and output data.

### Overview of API Input and Output

The API constructs an optimized portfolio that tracks a benchmark index while adhering to defined constraints. The optimization process minimizes the **tracking error** between the portfolio and index. Users provide input parameters (such as covariance data and constraints), and the API returns results detailing the optimized portfolio composition.

### Input Parameters: `IndexTracking`

| Field Name | Type | Description |
|------------|------|-------------|
| `description` | string | Brief description of the portfolio. |
| `assets_utility_matrix` | array | The quadratic utility matrix of the assets in the look back window. For example, it could be a covariance matrix or a quadratic distance matrix. |
| `assets_to_benchmark_utility_vector` | array | The quadratic utility vector between the assets and the benchmark in the look back window. For example, it could be a covariance matrix or a quadratic distance matrix. |
| `asset_names` | array | List of asset names or identifiers. |
| `portfolio_size` | integer | Number of assets in the portfolio (1-2047). |
| `minimum_weight` | number (optional) | Minimum weight per asset (default: `0`). |
| `maximum_weight` | number (optional) | Maximum weight per asset (default: `1`). |
| `linear_constraints_matrix` | array (optional) | Matrix of linear constraints. |
| `lower_bounds_vector` | array (optional) | Lower bounds for constraints. |
| `upper_bounds_vector` | array (optional) | Upper bounds for constraints. |
| `previous_portfolio` | object (optional) | Mapping of asset weights in the previous portfolio. |
| `max_companies_rotation` | integer (optional) | Max number of assets changing from the previous portfolio. |
| `max_sales_rotation` | number (optional) | Maximum allowed turnover percentage. |
| `sectorial_weights` | object (optional) | Sector weight distribution for the portfolio. |
| `sectorial_distribution` | object (optional) | Asset-to-sector mapping. |
| `sectorial_weight_tolerance` | number (optional) | Allowed deviation from sector weight constraints. |
| `sum_of_portfolio_weights` | number (optional) | Expected total weight of portfolio assets. |
| `random_number_generator_seed` | integer (optional) | Seed for the random number generator. |

### Output Parameters: `ComputationResult`

| Field | Type | Description |
|--------|------|-------------|
| `computationId` | string | Unique identifier for the computation. |
| `type` | string | Type of computation performed. |
| `description` | string | Description of the computation. |
| `status` | string | Current computation status (`Pending`, `Computing`, `Failed`, `Ok`). |
| `progress` | integer | Percentage progress of the computation. |
| `computationTime` | number | Time taken for computation (in seconds). |
| `computationStartTime` | string (date-time) | Start time of computation. |
| `computationStoreTime` | string (date-time) | Time when computation was stored. |
| `solution` | array | Optimized portfolio weights. |
| `named_solution` | object | Solution mapped to asset names. |
| `info` | number | Solver status code (`0` = No issues). |
| `cost` | number (optional) | Minimum cost function value. |
| `weights` | array (optional) | Final asset weights. |

---

## 1.5. Example API Response

### Initial API Response (Computation in Progress)
Upon submission, the API immediately responds with a computation ID and status:

```json
{
    "computationId": "a3984c72-3ae9-4bdf-adee-005b65c1bc9e",
    "status": "Computing",
    "computationStoreTimeUtc": "2025-03-04T12:34:56.8317536Z"
}
```

### Final Computation Result (Optimized Portfolio)
Once the computation completes, the API returns the optimized portfolio weights:

```json
{
    "computationId": "f03efc3c-cd8f-4341-a84e-000caa380f89",
    "status": "Ok",
    "computationTimeInSeconds": 6.0413,
    "named_solution": {
        "a": 0.0724,
        "b": 0.0,
        "c": 0.1821,
        "d": 0.1716,
        "e": 0.2064,
        "f": 0.0253,
        "g": 0.0,
        "h": 0.2588,
        "i": 0.0492,
        "j": 0.0343
    },
    "info": 0
}
```

This structured output provides insights into the computation and its results.

### The main components of the input: creating a new portfolio
The Index Tracking API is designed to be flexible, allowing users to specify only the necessary parameters for their specific use case. While many parameters are optional and can be used to impose constraints or refine the optimization, there are a few mandatory parameters that must always be provided, whether you are creating a new portfolio from scratch or rebalancing an existing one.

The following parameters are always required for a valid computation request:

- assets_utility_matrix: The covariance matrix of assets, representing the risk and correlation between them.
- assets_to_benchmark_utility_vector: The covariance vector between assets and the index, used to measure how each asset relates to the index.
- portfolio_size: The number of assets to be included in the portfolio (ranging from 1 to 2047).
- asset_names: An array of asset identifiers or names, providing a reference for interpreting the results.

Additionally, while not strictly mandatory, it is always helpful to include:
- description: A brief description of the computation, aiding in tracking and identifying different requests.

A valid request with only the mandatory parameters (plus a description for clarity) might look like this:

```json
{
  "assets_utility_matrix": [
    [3.571705619883564, -0.7955365555749586, 0.12557964034596986, 1.0639482728918976, -0.40191777016183283, 0.6863605725971405, -0.13949908918445247, 0.1711775516765147, 0.6755160399639315, 2.51293081246698],
    [-0.7955365555749586, 5.415520138923123, -2.0174005804761763, 0.030388266205496173, 2.550222403729447, 0.5643289518319003, -1.293304939459475, -0.5751123806041349, 3.594236909963808, 1.8956893890593007],
    [0.12557964034596986, -2.0174005804761763, 6.365322954156529, 2.257879191752247, -3.658046606965999, -0.45033274824515956, -1.0273304859751011, -0.21571777326705427, -0.3865083786928926, -1.533229084930434],
    [1.0639482728918976, 0.030388266205496173, 2.257879191752247, 3.9943121946674895, -1.78048417102389, 0.5687925714650388, -1.1084218725187323, -0.1515180112312195, -2.5176791064421384, 1.088241626988272],
    [-0.40191777016183283, 2.550222403729447, -3.658046606965999, -1.78048417102389, 8.390493238417324, 2.2223130935800453, -1.77173431354756, -1.3492997496155428, 3.448640251236081, 0.0298926428035794],
    [0.6863605725971405, 0.5643289518319003, -0.45033274824515956, 0.5687925714650388, 2.2223130935800453, 4.449214575445028, -2.713857481152314, -0.8300224805092693, -0.727328631285821, -0.3117075238989559],
    [-0.13949908918445247, -1.293304939459475, -1.0273304859751011, -1.1084218725187323, -1.77173431354756, -2.713857481152314, 4.0926798019898545, 2.3976179895459238, 0.27049000177733207, -0.29585690145164956],
    [0.1711775516765147, -0.5751123806041349, -0.21571777326705427, -0.1515180112312195, -1.3492997496155428, -0.8300224805092693, 2.3976179895459238, 3.864597206599372, -0.2604720356119854, -1.9647359528399329],
    [0.6755160399639315, 3.594236909963808, -0.3865083786928926, -2.5176791064421384, 3.448640251236081, -0.727328631285821, 0.27049000177733207, -0.2604720356119854, 9.083901928836333, 1.4490996023473937],
    [2.51293081246698, 1.8956893890593007, -1.533229084930434, 1.088241626988272, 0.0298926428035794, -0.3117075238989559, -0.29585690145164956, -1.9647359528399329, 1.4490996023473937, 5.4073509688190695]
  ],
  "assets_to_benchmark_utility_vector": [0.05177358659202069, -0.3356720686060817, 0.3206831344776768, 0.41750733093212566, 0.3313631827597856, -0.13542997653680122, -0.43400507867532734, 0.29062468284108733, 0.15880933369691574, -0.441086589088471],
  "portfolio_size": "8",
  "description": "Creating a new basic portfolio",
  "asset_names": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
}
```




