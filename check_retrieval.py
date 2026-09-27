import config
import questions as qs
from store import search
from scorer import retrieval_hits

passed = 0

for item in qs.answered():
    results = search(
        item["question"],
        top_k=config.TOP_K,
        corpus=config.CORPUS,
        variant="default",
    )

    hit = retrieval_hits(item["expects"], results)

    print(f"{'PASS' if hit else 'FAIL'} | {item['question']}")

    if hit:
        passed += 1

print(f"\nRetrieved answer evidence for {passed} of {len(qs.answered())} questions.")