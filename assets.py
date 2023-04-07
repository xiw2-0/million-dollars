import csv
import datetime
import asset


def get_assets() -> 'dict[str, asset.Asset]':
    """Returns all assets available.
    """
    assets = _get_china_a_share_assets(
        'data/china-a-share-1.csv') + _get_china_a_share_assets(
            'data/china-a-share-2.csv') + _get_nasdaq(
                'data/ndx.csv') + _get_sap('data/sap500.csv')
    return {a.id: a for a in assets}


def _get_china_a_share_assets(path: str) -> 'list[asset.Asset]':
    date_idx, id_idx, name_idx, price_idx = 0, 1, 4, 9

    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        id_to_names: 'dict[str, str]' = {}
        id_to_dates: 'dict[str, list[datetime.date]]' = {}
        id_to_prices: 'dict[str, list[float]]' = {}
        for i, line in enumerate(csv_reader):
            try:
                market_date = datetime.datetime.strptime(
                    line[date_idx], '%Y%m%d').date()
            except ValueError as e:
                print(f'Got an error: {e}, skipping line {i}')
                continue

            id = line[id_idx]
            id_to_names[id] = line[name_idx]
            if id not in id_to_dates:
                id_to_dates[id] = []
            id_to_dates[id].append(market_date)
            if id not in id_to_prices:
                id_to_prices[id] = []
            id_to_prices[id].append(float(line[price_idx]))

        assets: 'list[asset.Asset]' = []
        for id, name in id_to_names.items():
            a = asset.Asset(id, name)
            a.add_quote_history(id_to_prices[id], id_to_dates[id])
            assets.append(a)
    return assets


def _get_nasdaq(path: str) -> 'list[asset.Asset]':
    date_idx, price_idx = 0, 1

    id, name = '.NDX', 'NASDAQ 100'
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        dates: 'list[datetime.date]' = []
        prices: 'list[float]' = []
        for i, line in enumerate(csv_reader):
            try:
                market_date = datetime.datetime.strptime(
                    line[date_idx], '%m/%d/%Y').date()
            except ValueError as e:
                print(f'Got an error: {e}, skipping line {i}')
                continue

            dates.append(market_date)
            prices.append(float(line[price_idx]))

        ndx = asset.Asset(id, name)
        ndx.add_quote_history(prices, dates)
    return [ndx]


def _get_sap(path: str) -> 'list[asset.Asset]':
    date_idx, price_idx = 0, 1

    id, name = '.SAP', 'S&P 500'
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        dates: 'list[datetime.date]' = []
        prices: 'list[float]' = []
        for i, line in enumerate(csv_reader):
            try:
                market_date = datetime.datetime.strptime(
                    line[date_idx], '%Y/%m/%d').date()
            except ValueError as e:
                print(f'Got an error: {e}, skipping line {i}')
                continue

            dates.append(market_date)
            prices.append(float(line[price_idx]))

        sap = asset.Asset(id, name)
        sap.add_quote_history(prices, dates)
    return [sap]