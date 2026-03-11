from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np

try:
	import faiss # type: ignore
except Exception: # pragma: no cover
	faiss = None

from .embeddings import get_or_build_index, embed_texts
from .config import load_settings


@dataclass(frozen=True)
class RagHit:
	doc_id: str
	text: str
	score: float


def _paths(docs_path: Path | str) -> tuple[Path, Path, Path]:
	p = Path(docs_path)
	if not p.is_absolute():
		p = Path(__file__).resolve().parents[2] / p
	index_path = p.parent / "docs.npy"
	meta_path = p.parent / "docs.meta.json"
	return p, index_path, meta_path


def rag_search(query: str, docs_path: Path | str = "data/docs.txt", k: int =3) -> List[RagHit]:
	"""RAG with embeddings + FAISS (if available)."""
	p, index_path, meta_path = _paths(docs_path)
	if not p.exists():
		return []

	# load/build index
	idx = get_or_build_index(p, index_path, meta_path)
	texts = idx.texts
	if not texts:
		return []

	settings = load_settings()
	qv = embed_texts([query], settings)
	dv = idx.vectors

	if faiss is not None and dv.size >0:
		index = faiss.IndexFlatIP(dv.shape[1])
		# normalize vectors for cosine similarity
		dv_norm = dv / (np.linalg.norm(dv, axis=1, keepdims=True) +1e-8)
		qv_norm = qv / (np.linalg.norm(qv, axis=1, keepdims=True) +1e-8)
		index.add(dv_norm)
		scores, idxs = index.search(qv_norm, min(k, len(texts)))
		return [RagHit(doc_id=str(j), text=texts[j], score=float(s)) for s, j in zip(scores[0], idxs[0])]

	# fallback: dot product
	qv_norm = qv / (np.linalg.norm(qv, axis=1, keepdims=True) +1e-8)
	dv_norm = dv / (np.linalg.norm(dv, axis=1, keepdims=True) +1e-8)
	sims = (dv_norm @ qv_norm[0]).tolist()
	top = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[: min(k, len(texts))]
	return [RagHit(doc_id=str(j), text=texts[j], score=float(s)) for j, s in top]
