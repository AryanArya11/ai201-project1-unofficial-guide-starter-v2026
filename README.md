# The Unofficial Guide

Aryan Arya - "city_guides"

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

I tweaked a retrieval-augmented generation (RAG) system using the city_guides corpus to answer questions more effectively on
information across the region about transportation and accommodations. The system works by splitting documents into sections
based on Markdown headings and sentence boundaries, with an 800-character limit, and retrieves relevant information. With that 
information, the system generates answers with citations and actual references to the original documents. Changes I
specifically made include implementing a relevance cutoff of 0.66 to prevent the system from answering questions that fall
outside the corpus. I also increased the number of retrieved chunks from 5 to 8 to improve answers that require information
from multiple documents. My goal was to make the answers useful while ensuring they remain grounded in the information provided.


## Chunking Strategy

**Chunk size:** 800 characters
**Overlap:** 0 characters

I initially split the documents by paragraphs, but this produced 213 chunks, many of which lacked context or contained only headings.
I shared these results with AI and asked it to help me develop a better strategy for my city guides. After discussing the issues, 
I prompted it to implement section-aware chunking that preserves document titles and headings, with an 800-character limit that prioritizes sentence boundaries.

This brought the total down to 94 chunks. Of the five samples I inspected, four contained enough information to answer a question independently.
The accessibility introduction still lacked useful details, but this approach keeps related information together more effectively.

## Sample Chunks


======================================================================
Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents
======================================================================
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are difficult and it is better to know in advance.

======================================================================
Chunk 2  |  source: guide_corry_vale.md#5  |  produced by: chunker.py::split_documents
======================================================================
# Corry Vale
## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.

======================================================================
Chunk 3  |  source: guide_givens_mill.md#2  |  produced by: chunker.py::split_documents
======================================================================
# Givens Mill
## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.

======================================================================
Chunk 4  |  source: guide_kestrelford.md#4  |  produced by: chunker.py::split_documents
======================================================================
# Kestrelford
## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.

======================================================================
Chunk 5  |  source: guide_pellew_sands.md#6  |  produced by: chunker.py::split_documents
======================================================================
# Pellew Sands
## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.

## Sample Answer


**Question:** How can I get to the airport from Marchwood?

**Answer:**

```text
You can get to the airport from Marchwood by taking a dedicated bus that runs every 15 minutes.

Source: guide_marchwood.md
```

**My relevance cutoff:** 0.66

My five answerable questions had best distances between 0.212 and 0.520, while the five out-of-scope questions ranged from 0.8026 to 0.9753.
I chose 0.66 because it falls within the gap between these two groups, allowing my system to answer relevant questions while
refusing ones outside the corpus.


I initially used TOP_K = 5, but noticed that my question comparing Thornby Wells and Elder Ness was missing information about 
Thornby Wells. After I increased TOP_K to 8, the missing information appeared in the sixth retrieved chunk, allowing the system 
to finally answer both parts of the question.

I also adjusted my grounding instructions after noticing that some questions were being interpreted too strictly. I then 
drafted up ideas to polish the rules added GROUNDING_INSTRUCTIIONS of mine and stress-tested them with Claude and implemented them.
After testing again, the system correctly answered my questions about Halden Bay and cited the relevant documents.


| Question | In corpus? | Best distance |
|---|---|---|
| What are the populations of the largest and smallest villages in Corry Vale? | Yes | 0.212 |
| How can I get to the airport from Marchwood? | Yes | 0.4471 |
| How easy is it to get around Thornby Wells on foot, and what should visitors know about walking to the lighthouse at Elder Ness? | Yes | 0.2917 |
| When is Halden Bay busiest during the year? | Yes | 0.293 |
| Which town in the region is known for seafood? | Yes | 0.520 |
| What is the capital of Mongolia? | No | 0.8026 |
| How do I change the oil in a diesel engine? | No | 0.8881 |
| Who won the 1994 World Cup? | No | 0.9753 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8350 |
| How do I write a for loop in Rust? | No | 0.8365 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1. My Chunking Strategy** 

I initially split my documents by paragraphs, but this produced 213 chunks, many of which lacked context or contained only 
headings. I shared these results with AI and asked it to help me understand the different approaches I could take to improve my
chunking strategy. After discussing the limitations of my approach, I decided to use Markdown headings to keep related 
information together. I then prompted AI to help implement this strategy with an 800-character limit, prioritizing sentence 
boundaries. This brought the total down to 94 chunks, and after inspecting five samples, I found that four contained enough 
information to answer a question independently. I also chose to set my chunk overlap to zero because my chunker already repeats 
the document title and relevant section headings, which helps preserve context without duplicating the actual information 
between chunks.


**2. Fixing Retrieval & Grounding** 

After getting some idea of retrieval through the README, this marked my first usecase of AI in which I used AI to help me understand how retrieval settings and grounding instructions could affect the answers my system generates. After testing my 
questions, I noticed that TOP_K = 5 was missing information from Thornby Wells, which appeared in the sixth retrieved chunk. I 
decided to increase TOP_K to 8 and tested the question again, allowing the system to retrieve the information needed to answer 
both parts.

I experimented a bit with the relevance cutoffs and I also shared my retrieval distances with Claude to help determine a reasonable relevance cutoff. Based on my results, I chose 0.66 to separate answerable questions from those outside the corpus; 
I was able to reason for this cutoff so specifically since I graphed a series of cutoffs with Claude in which I tested testable 
questions and out-of-scope questions to determine a suitable number. Also, I started noticing that my grounding instructions 
were interpreting certain questions too strictly, I asked AI to help clarify how the model could combine supported facts 
without introducing unsupported information. I adjusted the instructions and tested the questions again to confirm that the 
answers remained grounded in the documents.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
