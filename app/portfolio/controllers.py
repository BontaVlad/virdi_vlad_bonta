from datetime import date
from typing import List

import pandas as pd

from portfolio.services import fetch_assets_prices


async def get_symbols_data(symbols, initial_balance: int, date_from: date=None,
                           date_to: date = None, limit: int=1000) -> str:
    prices = await fetch_assets_prices(
        [e.name for e in symbols], date_from=date_from,
        date_to=date_to, limit=limit
    )
    df = pd.DataFrame([e for e in prices], columns=['symbol', 'date', 'close'])
    return df\
        .sort_values(by=['date'])\
        .groupby('symbol')\
        .last()\
        .to_dict('records')
