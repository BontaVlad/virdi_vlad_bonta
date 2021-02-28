from datetime import date
from typing import List
import asyncio


from httpx import AsyncClient

import conf


async def request(client: AsyncClient, url: str) -> dict:
    response = await client.get(url)
    response.raise_for_status()
    return response.json()


async def fetch_assets_prices(symbols: List[str], date_from: date=None, date_to: date = None, limit: int=1000):
    symbols_formated = ",".join(symbols)
    url = f"{conf.MARKETSTACK_API_URL}?access_key={conf.MARKETSTACK_API_KEY}&symbols={symbols_formated}&limit={limit}"
    if date_from:
        url += f"&date_from={date_from}"
    if date_to:
        url += f"&date_to={date_to}"

    async with AsyncClient() as client:
        result = await client.get(url)
        result.raise_for_status()
        symbols_data = result.json()
        # we got all the data in one page
        pagination_total = symbols_data['pagination']['total']
        if pagination_total == symbols_data['pagination']['count']:
            return [symbols_data['data'], ]

        # we need to fetch more pages
        pages = []
        for offset in range(0, pagination_total, limit):
            pages.append(f"{url}&offset={offset}")

        tasks = [request(client, page) for page in pages]
        results = await asyncio.gather(*tasks)
        result = []
        for e in results:
            result += e['data']
        return result
