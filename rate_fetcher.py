import aiohttp
import logging
from typing import Dict

log = logging.getLogger(__name__)

CURRENCY_PAIRS = ["USD/CNY", "EUR/CNY", "GBP/CNY", "USD/EUR", "USD/JPY"]
API_URL = "https://api.exchangerate-api.com/v4/latest/{base}"

class RateFetcher:
    def __init__(self):
        self.last_rates: Dict[str, float] = {}

    async def fetch_all(self) -> Dict[str, float]:
        results = {}
        async with aiohttp.ClientSession() as session:
            for pair in CURRENCY_PAIRS:
                base, quote = pair.split("/")
                try:
                    async with session.get(API_URL.format(base=base), timeout=aiohttp.ClientTimeout(total=10)) as resp:
                        data = await resp.json()
                        rate = data["rates"].get(quote)
                        if rate:
                            results[pair] = round(rate, 4)
                except Exception as e:
                    log.error(f"Failed to fetch {pair}: {e}")
        self.last_rates = results
        return results