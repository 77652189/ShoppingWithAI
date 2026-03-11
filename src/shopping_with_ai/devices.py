from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Device:
	id: str
	name: str
	category: str
	price_range: str
	persona: List[str]
	features: List[str]
	tags: List[str]


def _devices_path() -> Path:
	# Project root = .../ShoppingWithAI
	root = Path(__file__).resolve().parents[2]
	return root / "data" / "devices.json"


def _load_devices() -> List[Device]:
	p = _devices_path()
	if not p.exists():
		return []
	data = json.loads(p.read_text(encoding="utf-8"))
	out: List[Device] = []
	for d in data:
		out.append(
			Device(
				id=str(d.get("id", "")),
				name=str(d.get("name", "")),
				category=str(d.get("category", "phone")),
				price_range=str(d.get("price_range", "")),
				persona=list(d.get("persona", []) or []),
				features=list(d.get("features", []) or []),
				tags=list(d.get("tags", []) or []),
			)
		)
	return out


def recommend_devices(query: str, k: int = 3) -> List[Device]:
	"""Recommend devices from local mock database.

	Deterministic for the same query.
	"""
	devices = _load_devices()
	if not devices:
		return []

	q = (query or "").lower()

	def score(dev: Device) -> int:
		s = 0
		for t in dev.tags + dev.persona:
			if t and str(t).lower() in q:
				s += 1
		return s

	scored = [(score(d), d) for d in devices]
	candidates = [d for s, d in scored if s > 0]
	if not candidates:
		candidates = devices[:]

	seed = sum(ord(c) for c in q) or 1
	rng = random.Random(seed)
	rng.shuffle(candidates)
	return candidates[: min(k, len(candidates))]
