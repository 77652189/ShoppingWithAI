from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np

try:
	import faiss # type: ignore
except Exception: # pragma: no cover
	faiss = None


@dataclass(frozen=True)
class RagHit:
	doc_id: str
	text: str
	score: float


def _embed_stub(texts: List[str]) -> np.ndarray:
	"""Very small stub embedder.

	For real use, replace with an embedding model and store vectors.
	"""
	# Deterministic pseudo-embedding: bag-of-chars hashed into64 dims
	dim =64
	vecs = np.zeros((len(texts), dim), dtype=np.float32)
	for i, t in enumerate(texts):
		for ch in t:
			idx = (ord(ch) *1315423911) % dim
			vecs[i, idx] +=1.0
	# normalize
	norms = np.linalg.norm(vecs, axis=1, keepdims=True) +1e-8
	return vecs / norms


def rag_search(query: str, docs_path: Path | str = "data/docs.txt", k: int =3) -> List[RagHit]:
	"""Tiny local RAG over a newline-delimited docs file.

	Uses FAISS if available; falls back to numpy dot-product.
	"""
	p = Path(docs_path)
	if not p.exists():
		return []
	docs = [line.strip() for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
	if not docs:
		return []
	qv = _embed_stub([query])
	dv = _embed_stub(docs)

	if faiss is not None:
		index = faiss.IndexFlatIP(dv.shape[1])
		index.add(dv)
		scores, idxs = index.search(qv, min(k, len(docs)))
		hits: List[RagHit] = []
		for score, j in zip(scores[0].tolist(), idxs[0].tolist()):
			hits.append(RagHit(doc_id=str(j), text=docs[j], score=float(score)))
		return hits

	# fallback
	sims = (dv @ qv[0]).tolist()
	top = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[: min(k, len(docs))]
	return [RagHit(doc_id=str(j), text=docs[j], score=float(s)) for j, s in top]
