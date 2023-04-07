"""A portfolio represent a combination of several assets from China A-share stock market."""

import asset
import numpy as np


class Portfolio(object):
    """A portfolio is composed of several assets, each with a weight that sums up to 1.
    
    Attributes:
        assets: A list of assets in China A-share.
        weights: A list of floats indicating the weight of each asset in this portofolio.
    """

    def __init__(self) -> None:
        self._assets: 'list[asset.Asset]' = []
        self._weights: 'list[float]' = []

    def add_assets(self, assets: 'list[asset.Asset]',
                   weights: 'list[float]') -> None:
        """Adds assets to this portfolio.

        Raises:
            AssertError when the length of assets and weights is not equal.
        """
        if len(assets) != len(weights):
            raise AssertionError(
                'Length of assets and weights should be equal, but was %d, %d'.
                format(len(assets), len(weights)))
        self._assets = assets.copy()
        self._weights = weights

    def update_weights(self, weights: 'list[float]') -> None:
        if len(weights) != len(self._weights):
            raise AssertionError(
                'Length of assets and weights should be equal, but was %d, %d'.
                format(len(self._assets), len(weights)))
        self._weights = weights

    def expected_return(self, duration: asset.Duration) -> float:
        """Returns the expected return of this portfolio.

        The composition is calculated following E[aX + bY] = aEX + bEY
        """
        return sum([
            self._assets[i].expected_return(duration) * self._weights[i]
            for i in range(len(self._assets))
        ])

    def risk(self, duration: asset.Duration) -> float:
        """Returns the risk (standard deviation) of this portfolio.

        It is calculated as follows:
            D[aX+bY+cZ] = E[(aX+bY+cZ)(aX+bY+cZ) - (aEX+bEY+cEZ)*(aEX+bEY+cEZ)]
            = aaDX + bbDY + ccDZ + 2abCOV(X,Y) + 2bcCOV(Y, Z) + 2acCOV(X,Z)

            COV(X,Y) = phio * (DX * DY)^0.5 
        """
        deviations = [a.risk(duration)**2 for a in self._assets]
        num_assets = len(self._assets)
        dev = sum(
            [self._weights[i]**2 * deviations[i] for i in range(num_assets)])
        for i in range(num_assets):
            for j in range(i + 1, num_assets):
                dev += 2 * self._weights[i] * self._weights[j] * self._assets[
                    i].correlation_coefficient(
                        self._assets[j]) * (deviations[i] * deviations[j])**0.5
        return dev**0.5

    def _weighted_value_changes(self) -> 'np.ndarray':
        changes = [
            np.array(asset.price_changes()) * weight
            for (asset, weight) in zip(self._assets, self._weights)
        ]

        return np.sum(changes, axis=0)
