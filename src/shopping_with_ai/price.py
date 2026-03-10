from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PriceQuote:
 query: str
 price: Optional[float]
 currency: str = "USD"
 source: str = "stub"


def lookup_price(query: str) -> PriceQuote:
 """Stub price lookup.

 Replace with a real API (Amazon, Walmart, SerpAPI, etc.) later.
 """
 # Simple placeholder behavior.
 return PriceQuote(query=query, price=None)
