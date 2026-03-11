from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np

try:
	import faiss # type: ignore
except Exception: # pragma: no cover
	faiss = None

from .device_embeddings import get_or_build_device_index
from .embeddings import embed_texts
from .config import load_settings


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


def recommend_devices(query: str, k: int =3) -> List[Device]:
	"""Recommend devices using embedding similarity.

	Falls back to random sample if embeddings not available.
	"""
	idx = get_or_build_device_index()
	if not idx.devices or idx.vectors.size ==0:
		return []

	settings = load_settings()
	qv = embed_texts([query], settings)
	dv = idx.vectors

	if faiss is not None:
		index = faiss.IndexFlatIP(dv.shape[1])
		# normalize for cosine
		dv_norm = dv / (np.linalg.norm(dv, axis=1, keepdims=True) +1e-8)
		qv_norm = qv / (np.linalg.norm(qv, axis=1, keepdims=True) +1e-8)
		index.add(dv_norm)
		scores, idxs = index.search(qv_norm, min(k, len(idx.devices)))
		return [idx.devices[j] for j in idxs[0].tolist()]

	# fallback: dot product
	qv_norm = qv / (np.linalg.norm(qv, axis=1, keepdims=True) +1e-8)
	dv_norm = dv / (np.linalg.norm(dv, axis=1, keepdims=True) +1e-8)
	sims = (dv_norm @ qv_norm[0]).tolist()
	top = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[: min(k, len(idx.devices))]
	return [idx.devices[j] for j, _ in top]
