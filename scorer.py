import re
from rapidfuzz import fuzz

MATCH_THRESHOLD = 90

def matches_expected(expects: str, text: str) -> bool:
    expected = expects.strip().lower()
    text = text.strip().lower()

    # Always accept exact matches
    if expected in text:
        return True

    # otherwise we should use fuzzy matching to check similarity
    expected_nums = re.findall(r"\d+", expected)
    text_nums = re.findall(r"\d+", text)

    if expected_nums:
        if not all(number in text_nums for number in expected_nums):
            return False

        
    score = fuzz.partial_ratio(expected, text)
    return score >= MATCH_THRESHOLD

def judge(question, expects, answer, results) -> bool:
    """
    With this judge function, I can determine whether the generated answer matches the expected info.

    - Expected facts can be seperated by some form of punctuation.
    - All the expected facts must be supported by the answer.
    """

    expected_parts = [ part.strip() for part in expects.split(';') if part.strip() ]

    return all(
        matches_expected(part, answer)
        for part in expected_parts
    )


def retrieval_hits(expects, results) -> bool:
    """
    With this function, I can check whether the any of the expected info appears in the retrieved chunks.
    """
    expected_parts = [
        part.strip()
        for part in expects.split(";")
        if part.strip()
    ]

    retrieved_text = "\n".join(
        chunk.text
        for chunk in results
    )

    return all(
        matches_expected(part, retrieved_text)
        for part in expected_parts
    )