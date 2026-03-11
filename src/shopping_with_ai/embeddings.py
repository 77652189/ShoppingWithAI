from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np

from .config import Settings, load_settings
from .llm import make_client


@dataclass(frozen=True)
class EmbedIndex:
	vectors: np.ndarray
	texts: List[str]


def embed_texts(texts: List[str], settings: Settings) -> np.ndarray:
	"""Embed texts using Qwen embedding model (OpenAI-compatible).

	DashScope embedding API limits batch size; we chunk to10.
	"""
	client = make_client(settings)
	all_vecs: List[List[float]] = []
	for i in range(0, len(texts),10):
		batch = texts[i : i +10]
		resp = client.embeddings.create(
			model=settings.embedding_model,
			input=batch,
		)
		all_vecs.extend([d.embedding for d in resp.data])
	return np.asarray(all_vecs, dtype=np.float32)


def load_docs(docs_path: Path) -> List[str]:
	if not docs_path.exists():
		return []
	return [
		line.strip()
		for line in docs_path.read_text(encoding="utf-8").splitlines()
		if line.strip()
	]


def save_index(index_path: Path, meta_path: Path, vectors: np.ndarray, texts: List[str]) -> None:
	index_path.parent.mkdir(parents=True, exist_ok=True)
	# save vectors as .npy for simplicity
	with open(index_path, "wb") as f:
		np.save(f, vectors)
	meta_path.write_text(json.dumps({"texts": texts}, ensure_ascii=False, indent=2), encoding="utf-8")


def load_index(index_path: Path, meta_path: Path) -> EmbedIndex | None:
	if not index_path.exists() or not meta_path.exists():
		return None
	with open(index_path, "rb") as f:
		vectors = np.load(f)
	meta = json.loads(meta_path.read_text(encoding="utf-8"))
	texts = list(meta.get("texts", []))
	return EmbedIndex(vectors=vectors, texts=texts)


def build_index(docs_path: Path, index_path: Path, meta_path: Path, settings: Settings) -> EmbedIndex:
	texts = load_docs(docs_path)
	if not texts:
		return EmbedIndex(vectors=np.zeros((0, 1), dtype=np.float32), texts=[])
	vectors = embed_texts(texts, settings)
	save_index(index_path, meta_path, vectors, texts)
	return EmbedIndex(vectors=vectors, texts=texts)


def get_or_build_index(docs_path: Path, index_path: Path, meta_path: Path) -> EmbedIndex:
	idx = load_index(index_path, meta_path)
	if idx is not None:
		return idx
	settings = load_settings()
	return build_index(docs_path, index_path, meta_path, settings)
