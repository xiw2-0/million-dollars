import asset
import unittest
import datetime


class AssetTest(unittest.TestCase):

    def test_expected_return_annual_return_of_two_years(self):
        dummy_asset = asset.Asset('id', 'name')
        dummy_asset.add_quote_history(
            [100., 150.],
            [datetime.date(2000, 5, 1),
             datetime.date(2001, 1, 1)])

        self.assertAlmostEqual(
            dummy_asset.expected_return(asset.Duration.YEAR), 0.5)

    def test_expected_return_month_return_of_two_months(self):
        dummy_asset = asset.Asset('id', 'name')
        dummy_asset.add_quote_history(
            [100., 150.],
            [datetime.date(2000, 5, 1),
             datetime.date(2000, 6, 1)])

        self.assertAlmostEqual(
            dummy_asset.expected_return(asset.Duration.MONTH), 0.5)

    def test_expected_return_return_caches(self):
        dummy_asset = asset.Asset('id', 'name')
        dummy_asset.add_quote_history(
            [100., 150.],
            [datetime.date(2000, 5, 1),
             datetime.date(2000, 6, 1)])
        dummy_asset.expected_return(asset.Duration.MONTH)
        dummy_asset.risk(asset.Duration.MONTH)

        self.assertAlmostEqual(
            dummy_asset.expected_return(asset.Duration.MONTH), 0.5)

    def test_risk_annual_risk_two_years(self):
        dummy_asset = asset.Asset('id', 'name')
        dummy_asset.add_quote_history([100., 150., 120.], [
            datetime.date(2000, 5, 1),
            datetime.date(2001, 1, 1),
            datetime.date(2002, 1, 2)
        ])

        self.assertAlmostEqual(dummy_asset.risk(asset.Duration.YEAR), 0.35)
    
    def test_risk_annual_risk_cache(self):
        dummy_asset = asset.Asset('id', 'name')
        dummy_asset.add_quote_history([100., 150., 120.], [
            datetime.date(2000, 5, 1),
            datetime.date(2001, 1, 1),
            datetime.date(2002, 1, 2)
        ])
        dummy_asset.expected_return(asset.Duration.YEAR)
        dummy_asset.risk(asset.Duration.YEAR)

        self.assertAlmostEqual(dummy_asset.risk(asset.Duration.YEAR), 0.35)


if __name__ == '__main__':
    unittest.main()