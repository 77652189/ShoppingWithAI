from __future__ import annotations

import hashlib
import os
import random
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PriceQuote:
	query: str
	price: Optional[float]
	currency: str = "USD"
	source: str = "mock"
	note: str = ""
	url: str = ""


def _seed_from_query(query: str) -> int:
	# Stable across runs: use sha256
	digest = hashlib.sha256(query.strip().lower().encode("utf-8")).digest()
	return int.from_bytes(digest[:8], "big", signed=False)


def _guess_category(query: str) -> str:
	q = query.lower()
	if any(x in q for x in ["手机", "phone", "iphone", "android"]):
		return "phone"
	if any(x in q for x in ["耳机", "headphone", "earbud", "airpods", "sony", "bose"]):
		return "audio"
	if any(x in q for x in ["电脑", "laptop", "macbook", "thinkpad", "desktop"]):
		return "computer"
	if any(x in q for x in ["平板", "tablet", "ipad"]):
		return "tablet"
	if any(x in q for x in ["土豆", "potato"]):
		return "grocery"
	return "general"


def lookup_price(query: str) -> PriceQuote:
	"""Mock price lookup (no external API).

	This project is about the agent flow; price lookup is not the focus.
	We generate deterministic demo prices so the pipeline can be tested.

	Optional: set PRICE_MODE=stub to always return None.
	"""
	mode = os.getenv("PRICE_MODE", "mock").lower()
	if mode in {"stub", "none", "off"}:
		return PriceQuote(query=query, price=None, source="stub", note="PRICE_MODE disables price lookup")

	seed = _seed_from_query(query)
	rng = random.Random(seed)
	cat = _guess_category(query)

	# Rough demo ranges (USD)
	ranges = {
		"phone": (149.0,999.0),
		"audio": (19.0,399.0),
		"computer": (399.0,2499.0),
		"tablet": (199.0,1299.0),
		"grocery": (0.79,6.99),
		"general": (9.0,199.0),
	}
	lo, hi = ranges.get(cat, ranges["general"])
	val = rng.uniform(lo, hi)

	# price precision
	if cat == "grocery":
		val = round(val,2)
	else:
		val = round(val,0) -0.01 # looks like retail pricing

	return PriceQuote(
		query=query,
		price=float(val),
		currency="USD",
		source="mock",
		note=f"Demo price (category={cat}, deterministic by query)",
		url="",
	)
