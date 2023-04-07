"""An asset that is from China A-share stock market."""
from enum import Enum
import datetime
import math
import numpy as np


class Duration(Enum):
    """Frequency of the quote of an asset."""
    DAY = 1
    WEEK = 2
    MONTH = 3
    YEAR = 4


class Asset(object):
    """An asset that is from China A-share stock market.

    Attributes:
        id: Identifier of the asset.
        name: Name of this asset.
    """

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name
        self._return_cache: 'dict[Duration, float]' = {}
        self._risk_cache: 'dict[Duration, float]' = {}
        self._corr_cache: 'dict[str, float]' = {}

    def add_quote_history(self, prices: 'list[float]',
                          dates: 'list[datetime.date]') -> None:
        if len(prices) != len(dates):
            raise ValueError(
                'Length of prices ({}) is not equal to dates ({})'.format(
                    len(prices), len(dates)))

        self._prices = prices.copy()
        self._dates = dates.copy()

    def correlation_coefficient(self, asset: 'Asset') -> float:
        """Computes the correlation coefficient of two assets.
        """
        if asset.id in self._corr_cache:
            return self._corr_cache[asset.id]

        date_to_price_l = {
            d: self._prices[i]
            for i, d in enumerate(self._dates)
        }
        date_to_price_r = {
            d: asset._prices[i]
            for i, d in enumerate(asset._dates)
        }

        common_dates = sorted(
            set(date_to_price_l.keys()).intersection(date_to_price_r.keys()))
        prices_l = [date_to_price_l[d] for d in common_dates]
        prices_r = [date_to_price_r[d] for d in common_dates]

        cov_matrix = np.cov(np.stack([prices_l, prices_r]))
        self._corr_cache[asset.id] = cov_matrix[0][1] / math.sqrt(
            cov_matrix[0][0] * cov_matrix[1][1])
        return self._corr_cache[asset.id]

    def expected_return(self, duration: Duration) -> float:
        if duration in self._return_cache:
            return self._return_cache[duration]
        self._return_cache[duration] = np.array(
            self._price_changes(duration)).mean()
        return self._return_cache[duration]

    def risk(self, duration: Duration) -> float:
        if duration in self._risk_cache:
            return self._risk_cache[duration]
        self._risk_cache[duration] = np.array(
            self._price_changes(duration)).std()
        return self._risk_cache[duration]

    def _price_changes(self, duration: Duration) -> 'list[float]':
        date_to_prices = {
            self._get_date_string(self._dates[i], duration): p
            for i, p in enumerate(self._prices)
        }
        dates = sorted(date_to_prices.keys())
        changes = []
        for i in range(1, len(dates)):
            changes.append(date_to_prices[dates[i]] /
                           date_to_prices[dates[i - 1]] - 1)
        return changes

    def _get_date_string(self, date: datetime.date, duration: Duration) -> str:
        if duration == Duration.DAY:
            return date.strftime("%Y%m%d")
        elif duration == Duration.WEEK:
            return f'{date.year}{date.month}-{date.day // 7}'
        elif duration == Duration.MONTH:
            return f'{date.year}{date.month}'
        return f'{date.year}'
