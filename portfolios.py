import asset
import portfolio
import matplotlib.pyplot as plt


def find_best_portfolios(
        assets: 'list[asset.Asset]',
        num_weights: int) -> 'tuple[dict[float, float], dict[float, list[float]]]':
    num_asset = len(assets)
    weights = [.0 for _ in range(num_asset)]
    pf = portfolio.Portfolio()
    pf.add_assets(assets, weights)

    returns, risks = [], []
    return_to_risk: 'dict[float, float]' = {}
    return_to_weights: 'dict[float, list[float]]' = {}

    def dfs(ith_asset: int, weight_available: int) -> None:
        if ith_asset == num_asset - 1:
            weights[ith_asset] = weight_available / num_weights
            rk = pf.risk(asset.Duration.YEAR)
            rt = int(100 * pf.expected_return(asset.Duration.YEAR)) / 100
            risks.append(rk)
            returns.append(rt)
            if rt not in return_to_risk or return_to_risk[rt] > rk:
                return_to_risk[rt] = rk
                return_to_weights[rt] = weights.copy()
            return

        for assignment in range(0, weight_available + 1):
            weights[ith_asset] = assignment / num_weights
            dfs(ith_asset + 1, weight_available - assignment)

    dfs(0, num_weights)
    return (return_to_risk, return_to_weights)


def plot_portfolios(assets: 'list[asset.Asset]', num_weights: int) -> None:
    num_asset = len(assets)
    weights = [.0 for _ in range(num_asset)]
    pf = portfolio.Portfolio()
    pf.add_assets(assets, weights)

    returns, risks = [], []

    def dfs(ith_asset: int, weight_available: int) -> None:
        if ith_asset == num_asset - 1:
            weights[ith_asset] = weight_available / num_weights
            risks.append(pf.risk(asset.Duration.YEAR))
            returns.append(pf.expected_return(asset.Duration.YEAR))
            return

        for assignment in range(0, weight_available + 1):
            weights[ith_asset] = assignment / num_weights
            dfs(ith_asset + 1, weight_available - assignment)

    dfs(0, num_weights)
    plt.scatter(risks, returns)
    plt.xlabel('Risk')
    plt.ylabel('Return')
    plt.show()


def num_portfolio_combinations(num_asset: int, num_weights: int) -> int:
    dp = [[0 for _ in range(num_weights + 1)] for _ in range(2)]
    # init
    for i in range(len(dp[0])):
        dp[0][i] = 1
    # dp[i][j] = sum dp[i-1][k] for k in range(0, j+1)
    for i in range(1, num_asset + 1):
        for j in range(num_weights + 1):
            dp[1][j] = sum(dp[0][:j + 1])
        tmp = dp[0]
        dp[0] = dp[1]
        dp[1] = tmp
    return dp[0][-1]