"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document
import re 


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


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks. ⚠️ REPLACE THE BODY OF THIS IN MILESTONE 3.

    Right now it just calls the fallback. That is the plain, generic behaviour
    the brief is talking about.

    When you write your own strategy, set `produced_by` to
    "chunker.py::split_documents" so your README's Sample Chunks section names
    the right function. `app.py chunks` prints that string for you.

    Things worth thinking about before you write any code:
      - Are your documents short posts or long guides?
      - Is the useful information in one sentence, or spread over a paragraph?
      - Would splitting on paragraph breaks keep more thoughts intact than
        splitting on a character count?
    """

    MAX_CHARS = 800
    chunks: list[Chunk] = []

    for doc in documents:
        title = f"# {doc.source}"
        headings = []
        content = []
        index = 0

        def save_section():
            nonlocal index

            # Ignore sections without meaningful content.
            if not content:
                return

            # Normalize whitespace, including unexpected blank lines
            # inside sentences.
            body = " ".join(" ".join(content).split())

            if not body:
                return

            # Include the document title and active section headings.
            prefix_parts = [title]
            prefix_parts.extend(text for _, text in headings)
            prefix = "\n".join(prefix_parts)

            # Reserve space for the headings in every chunk.
            available = max(1, MAX_CHARS - len(prefix) - 2)

            remaining = body

            while remaining:

                # Keep the whole section when it fits.
                if len(remaining) <= available:
                    piece = remaining
                    remaining = ""

                else:
                    # Prefer ending at a sentence boundary.
                    cut = max(
                        remaining.rfind(mark, 0, available + 1) + 1
                        for mark in (". ", "? ", "! ")
                    )

                    # If no useful sentence boundary exists,
                    # split at the nearest preceding word boundary.
                    if cut < available // 2:
                        cut = remaining.rfind(" ", 0, available + 1)

                    # Handle an exceptionally long unbroken word.
                    if cut <= 0:
                        cut = available

                    piece = remaining[:cut].strip()
                    remaining = remaining[cut:].strip()

                if not piece:
                    continue

                chunk_text = f"{prefix}\n\n{piece}"

                chunks.append(
                    Chunk(
                        text=chunk_text,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )

                index += 1

        # Read the document line by line.
        for line in doc.text.splitlines():
            line = line.strip()

            if not line:
                continue

            # Identify Markdown headings.
            match = re.match(r"^(#{1,6})\s+(.+)$", line)

            if match:
                level = len(match.group(1))

                # Finish the previous section before changing headings.
                save_section()
                content = []

                if level == 1:
                    # Store the document title.
                    title = line
                    headings = []

                else:
                    # Remove headings at the same or deeper level.
                    while headings and headings[-1][0] >= level:
                        headings.pop()

                    headings.append((level, line))

            else:
                # Collect the content belonging to this section.
                content.append(line)

        # Save the final section of the document.
        save_section()

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
