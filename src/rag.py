from __future__ import annotations

from pathlib import Path
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_documents(docs_dir: Path) -> list[dict]:
    documents: list[dict] = []
    if not docs_dir.exists():
        return documents

    for path in sorted(docs_dir.rglob("*.md")):
        relative_path = path.relative_to(docs_dir)
        process = (
            relative_path.parts[0]
            if len(relative_path.parts) > 1
            else "common"
        )
        documents.append(
            {
                "text": path.read_text(encoding="utf-8").strip(),
                "source": relative_path.as_posix(),
                "process": process,
            }
        )
    return documents


def split_documents(
    documents: list[dict],
    chunk_size: int = 1200,
    overlap: int = 150,
) -> list[dict]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size.")

    chunks: list[dict] = []
    for document in documents:
        text = str(document.get("text", "")).strip()
        if not text:
            continue

        start = 0
        chunk_index = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            if end < len(text):
                paragraph_break = text.rfind("\n\n", start, end)
                if paragraph_break > start:
                    end = paragraph_break

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    {
                        **document,
                        "text": chunk_text,
                        "chunk_index": chunk_index,
                    }
                )
                chunk_index += 1

            if end >= len(text):
                break
            next_start = end - overlap
            start = next_start if next_start > start else end

    return chunks


def _alert_text(alert: dict[str, Any]) -> str:
    parts = [
        str(alert.get("metric", "")),
        str(alert.get("alert_type", "")),
        str(alert.get("business_zone", "")),
        str(alert.get("python_description", "")),
    ]
    return " ".join(part for part in parts if part)


def build_rag_query(alert_group: dict) -> str:
    event_type = str(alert_group.get("event_type", ""))
    process = str(alert_group.get("process", ""))
    parts = [
        " ".join([event_type] * 12),
        " ".join([process] * 2),
        str(alert_group.get("event_classification", "")),
        " ".join(map(str, alert_group.get("metrics", []))),
        " ".join(map(str, alert_group.get("business_zones", []))),
        _alert_text(alert_group.get("main_alert", {})),
        " ".join(
            _alert_text(alert)
            for alert in alert_group.get("related_alerts", [])
        ),
    ]
    return " ".join(part.strip() for part in parts if part and part.strip())


def retrieve_context(
    alert_group: dict,
    docs_dir: Path,
    top_k: int = 3,
) -> dict:
    if top_k <= 0:
        raise ValueError("top_k must be positive.")

    process = str(alert_group.get("process", ""))
    documents = load_documents(docs_dir)
    scoped_documents = [
        document
        for document in documents
        if document["process"] in {"common", process}
    ]
    chunks = split_documents(scoped_documents)
    query = build_rag_query(alert_group)

    if not chunks or not query:
        return {"query": query, "chunks": [], "context_text": ""}

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b[\w_-]+\b",
    )
    matrix = vectorizer.fit_transform(
        [chunk["text"] for chunk in chunks] + [query]
    )
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    ranked_indices = scores.argsort()[::-1][: min(top_k, len(chunks))]

    retrieved_chunks = [
        {
            "text": chunks[index]["text"],
            "source": chunks[index]["source"],
            "process": chunks[index]["process"],
            "score": round(float(scores[index]), 4),
        }
        for index in ranked_indices
    ]
    context_text = "\n\n".join(
        (
            f"[Источник: {chunk['source']}; relevance={chunk['score']:.4f}]\n"
            f"{chunk['text']}"
        )
        for chunk in retrieved_chunks
    )
    return {
        "query": query,
        "chunks": retrieved_chunks,
        "context_text": context_text,
    }
