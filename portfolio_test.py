import unittest
import portfolio
import asset
import datetime


class PortfolioTest(unittest.TestCase):

    def test_expected_return_single_asset(self):
        dummy_asset = asset.Asset('id', 'name')
        dummy_asset.add_quote_history(
            [100., 200.],
            [datetime.date(2000, 1, 1),
             datetime.date(2001, 2, 1)])
        pf = portfolio.Portfolio()
        pf.add_assets([dummy_asset], [.5])

        self.assertAlmostEqual(pf.expected_return(asset.Duration.YEAR), 0.5)

    def test_expected_return_two_assets(self):
        asset_1 = asset.Asset('id1', 'name1')
        asset_1.add_quote_history(
            [100., 200.],
            [datetime.date(2000, 1, 1),
             datetime.date(2001, 2, 1)])
        asset_2 = asset.Asset('id2', 'name2')
        asset_2.add_quote_history(
            [100., 80.],
            [datetime.date(2002, 1, 1),
             datetime.date(2003, 2, 1)])
        pf = portfolio.Portfolio()
        pf.add_assets([asset_1, asset_2], [.5, .5])

        self.assertAlmostEqual(pf.expected_return(asset.Duration.YEAR), 0.4)


if __name__ == '__main__':
    unittest.main()