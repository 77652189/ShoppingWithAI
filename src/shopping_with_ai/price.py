from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass(frozen=True)
class PriceQuote:
	query: str
	price: Optional[float]
	currency: str = "USD"
	source: str = "stub"
	note: str = ""
	url: str = ""


def lookup_price(query: str) -> PriceQuote:
	"""Price lookup via Serper (Google Shopping search) if configured.

	To enable:
	- set SERPER_API_KEY in .env

	This returns a best-effort quote. If no key configured, returns stub.
	"""
	api_key = os.getenv("SERPER_API_KEY")
	if not api_key:
		return PriceQuote(
			query=query,
			price=None,
			source="stub",
			note="SERPER_API_KEY not set; price lookup is disabled.",
		)

	url = "https://google.serper.dev/shopping"
	headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
	payload = {"q": query, "gl": "us", "hl": "zh-cn"}

	try:
		with httpx.Client(timeout=15) as client:
			r = client.post(url, headers=headers, content=json.dumps(payload))
			r.raise_for_status()
			data = r.json()
		items = data.get("shopping") or []
		if not items:
			return PriceQuote(query=query, price=None, source="serper", note="No shopping results")

		# pick first item that has a price
		for it in items[:5]:
			p = it.get("price")
			link = it.get("link") or ""
			# Serper usually returns price as string like "$199.99" or "199.99"
			if p:
				# extract number
				import re

				m = re.search(r"([0-9]+(?:\.[0-9]+)?)", str(p).replace(",", ""))
				val = float(m.group(1)) if m else None
				cur = "USD" if "$" in str(p) else "USD"
				return PriceQuote(query=query, price=val, currency=cur, source="serper", url=link)

		return PriceQuote(query=query, price=None, source="serper", note="Results found but no parseable price")
	except Exception as e:
		return PriceQuote(query=query, price=None, source="serper", note=f"Error: {e}")
