"""
Stage 2 of the pipeline: splitting documents into chunks.

The campus_life corpus is made of short student advice posts, so the best
chunking strategy is paragraph-aware rather than fixed-width. Most documents are
already one complete thought, and if a post is longer than a single idea the
split falls on paragraph boundaries before it ever falls on a character count.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _split_long_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Break a piece that is too long into sentence-based chunks."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if not sentences:
        return [text.strip()]

    pieces: list[str] = []
    current = ""

    for sentence in sentences:
        candidate = sentence if not current else f"{current} {sentence}"
        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            pieces.append(current.strip())
            current = sentence
            continue

        words = sentence.split()
        mini = ""
        for word in words:
            test = word if not mini else f"{mini} {word}"
            if len(test) <= chunk_size:
                mini = test
            else:
                if mini:
                    pieces.append(mini.strip())
                mini = word
        if mini:
            current = mini

    if current:
        pieces.append(current.strip())

    if overlap <= 0 or len(pieces) < 2:
        return pieces

    overlapped: list[str] = []
    for i, piece in enumerate(pieces):
        if i == 0:
            overlapped.append(piece)
            continue

        previous = overlapped[-1]
        tail = previous[-overlap:] if overlap < len(previous) else previous
        overlap_text = piece
        if tail and overlap_text.startswith(tail):
            overlap_text = overlap_text[len(tail):].lstrip()
        merged = f"{tail} {overlap_text}".strip()
        overlapped.append(merged if len(merged) <= chunk_size else piece)

    return overlapped


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Chunk short advice posts by paragraph and keep complete thoughts intact."""
    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP
    chunks: list[Chunk] = []

    for doc in documents:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", doc.text.strip()) if p.strip()]
        if not paragraphs:
            paragraphs = [doc.text.strip()]

        current = ""
        for paragraph in paragraphs:
            candidate = paragraph if not current else f"{current}\n\n{paragraph}"
            if len(candidate) <= chunk_size:
                current = candidate
                continue

            if current:
                chunks.append(
                    Chunk(
                        text=current.strip(),
                        source=doc.source,
                        index=len([c for c in chunks if c.source == doc.source]),
                        produced_by="chunker.py::split_documents",
                    )
                )
                current = paragraph
            else:
                overflow = _split_long_text(paragraph, chunk_size, overlap)
                for piece in overflow[:-1]:
                    chunks.append(
                        Chunk(
                            text=piece.strip(),
                            source=doc.source,
                            index=len([c for c in chunks if c.source == doc.source]),
                            produced_by="chunker.py::split_documents",
                        )
                    )
                current = overflow[-1] if overflow else paragraph

        if current:
            chunks.append(
                Chunk(
                    text=current.strip(),
                    source=doc.source,
                    index=len([c for c in chunks if c.source == doc.source]),
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
