from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np

from .config import load_settings
from .embeddings import embed_texts, save_index, load_index


@dataclass(frozen=True)
class DeviceRecord:
	id: str
	name: str
	category: str
	price_range: str
	persona: List[str]
	features: List[str]
	tags: List[str]


@dataclass(frozen=True)
class DeviceIndex:
	vectors: np.ndarray
	devices: List[DeviceRecord]


def _devices_path() -> Path:
	root = Path(__file__).resolve().parents[2]
	return root / "data" / "devices.json"


def _index_paths() -> tuple[Path, Path]:
	root = Path(__file__).resolve().parents[2] / "data"
	return root / "devices.npy", root / "devices.meta.json"


def _load_devices() -> List[DeviceRecord]:
	p = _devices_path()
	data = json.loads(p.read_text(encoding="utf-8"))
	out: List[DeviceRecord] = []
	for d in data:
		out.append(
			DeviceRecord(
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


def _device_text(d: DeviceRecord) -> str:
	return (
		f"{d.name} {d.category}价格{d.price_range} "
		f"人群:{' '.join(d.persona)} 标签:{' '.join(d.tags)} "
		f"特性:{' '.join(d.features)}"
	)


def build_device_index() -> DeviceIndex:
	devices = _load_devices()
	if not devices:
		return DeviceIndex(vectors=np.zeros((0,1), dtype=np.float32), devices=[])
	settings = load_settings()
	texts = [_device_text(d) for d in devices]
	vectors = embed_texts(texts, settings)
	index_path, meta_path = _index_paths()
	save_index(index_path, meta_path, vectors, [d.id for d in devices])
	return DeviceIndex(vectors=vectors, devices=devices)


def load_device_index() -> DeviceIndex | None:
	index_path, meta_path = _index_paths()
	idx = load_index(index_path, meta_path)
	if idx is None:
		return None
	devices = _load_devices()
	id_to_dev = {d.id: d for d in devices}
	ordered = [id_to_dev[i] for i in idx.texts if i in id_to_dev]
	return DeviceIndex(vectors=idx.vectors, devices=ordered)


def get_or_build_device_index() -> DeviceIndex:
	idx = load_device_index()
	if idx is not None:
		return idx
	return build_device_index()
