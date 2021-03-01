from datetime import date
from typing import List

import pandas as pd

from portfolio.services import fetch_assets_prices


def percentage(p, x):
    return p / 100 * x


async def get_symbols_data(symbols, initial_balance: int, date_from: date=None,
                           date_to: date = None, limit: int=1000) -> str:
    prices = await fetch_assets_prices(
        [e.name for e in symbols], date_from=date_from,
        date_to=date_to, limit=limit
    )
    df = pd.DataFrame([e for e in prices], columns=['symbol', 'date', 'close'])
    df['shares'] = 0
    df['sell_value'] = 0
    df.sort_values(by=['date'])
    # TODO: cleanup code once we have graph
    purchase_prices = {
        e['symbol']: e['close'] for e in df\
        .groupby(by=['symbol'], as_index=False)\
        .last().to_dict('records')}
    sell_prices = {
        e['symbol']: e['close'] for e in df\
        .groupby(by=['symbol'], as_index=False)\
        .first().to_dict('records')}
    num_of_shares = {}
    sell_value = {}
    for s in symbols:
        stock_cost = purchase_prices[s.name]
        shares = percentage(s.allocation, initial_balance) / stock_cost
        sell_value[s.name] = sell_prices[s.name] * shares
        df.loc[df['symbol'] == s.name, 'shares'] = shares
    df['sell_value'] = df['close'] * df['shares']
    timegraph = {}
    for s in symbols:
        timegraph[s.name] = df.loc[df['symbol'] == s.name, 'sell_value'].tolist()
    return {
        "portfolio_worth": sum([e for e in sell_value.values()]),
        "symbol_worth": sell_value,
        "timegraph": timegraph
        }

