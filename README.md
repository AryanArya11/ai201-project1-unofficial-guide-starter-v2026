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


## Run Log — Before


| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks preserve useful information | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. Answers contain the information requested | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |


### Criterion 1 evidence

Produced by: `check_retrieval.py`
Checked by: `scorer.py::retrieval_hits`

```text
PASS | What are the population of the largest and smallest villages in Corry Vale?
PASS | How can I get to the airport from Marchwood?
PASS | When is Halden Bay busiest during the year?
FAIL | How easy is it to get around Thornby Wells on foot, and what should visitors know about walking to the lighthouse at Elder Ness?
PASS | Which town in the region is known for seafood?

```

### Criterion 2 evidence

Produced by: `run_eval.py::main`

```text
To get to the airport from Marchwood, you can take a dedicated bus that
is 20 minutes out and runs every 15 minutes (guide_marchwood.md).
```

### Criterion 3 evidence

Produced by: `run_eval.py::check_out_of_scope`

```text
refused  (best distance 0.803)  What is the capital of Mongolia?
refused  (best distance 0.888)  How do I change the oil in a diesel engine?
refused  (best distance 0.975)  Who won the 1994 World Cup?
refused  (best distance 0.835)  What is the recommended dosage of ibuprofen for a headache?
refused  (best distance 0.836)  How do I write a for loop in Rust?
-> gate refused 5 of 5
```

### Criterion 4 evidence

Produced by: `chunker.py::split_documents`
Printed by: `app.py chunks -n 5`


***Note***: 4 of 5 chunks met the criterion. All five were between 100 and 800 characters, but Chunk 1 was too general to independently answer a specific question.

Chunk 1  |  source: guide_accessibility.md#0  |  produced by: chunker.py::split_documents

# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are difficult and it is better to know in advance.


Chunk 2  |  source: guide_corry_vale.md#5  |  produced by: chunker.py::split_documents

# Corry Vale
## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.


Chunk 3  |  source: guide_givens_mill.md#2  |  produced by: chunker.py::split_documents

# Givens Mill
## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.


Chunk 4  |  source: guide_kestrelford.md#4  |  produced by: chunker.py::split_documents
# Kestrelford
## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.

Chunk 5  |  source: guide_pellew_sands.md#6  |  produced by: chunker.py::split_documents
# Pellew Sands
## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.


### Criterion 5 evidence

Produced by: `run_eval.py::main`

```text
Thornby Wells is flat and compact, taking 15 minutes to get around from
end to end, with the pump room, gardens, and main shopping street all
within three minutes of each other (guide_thornby_wells.md).

For Elder Ness, visitors should know that the walk to the lighthouse takes
25 minutes along the shingle, which is harder going than the distance
suggests (guide_elder_ness.md, guide_walking.md).
```


## Verdicts


| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | My retrieval hits recorded a 4/5 in all three runs, which meets my criteria of at least 4 out 5. The only miss was the question comparing Thornby Wells and Elder Ness |
| 2 | Every answer names a source | MET | All 5 answers named at least one source in all three runs, this meets my target for 5/5 |
| 3 | The relevance gate stops out-of-corpus questions | MET | The relevance gate stopped all 5 out-of-scope questions, meeting my 4/5 target |
| 4 | Chunks preserve useful info | MET | 4/5 of my sample chunks met the sizing and context requirements I set. The only sample that didn't have enough info to independently answer a question was the accessibility intro |
| 5 | Answers contain the info requested | MET | All 5 answers contained the specific facts requested in the questions in all 3 runs, this met my 4/5 target |

## Diagnoses

I didn't miss any of the criteria during the baseline tests. However, criterion 1 was the closest to missing since retrieval only succeeded for exactly 4 out 5 questions, which met my target of 4/5, but still one missed.

The question comparing Thornby Wells and Elder Ness was the only retrieval miss because my system successfully handled the other 4 questions just fine and I already was retrieving up to 8 chunks.
I think my original target of 4/5 might have been a little low for this criterion. If I were to tighten this criterion, I would change the target to 5/5 questions having the the necessary info somewhere in the retrieved chunks.



## The Improvement

**What I changed:**


What I ended up doing was adding BM25 keyword reranking after my existing semantic search. So originally, my system relied only on embedding similarity to rank the retrieved chunks. I kept semantic retrieval as the first stage, then ranked those retrieved chunks using both their semantic rank and BM25 keyword rank. I added the two rank positions together, and chunks with the lowest combined rank were returned.


**Why I picked it:**

I picked it because my Criterion 1 was closest to missing, although the runs hit the 4/5 target, I wanted to prioritize getting all runs to pass (5/5) since I believe that in all of the retrieved chunks gathered at least one of them contains the answer per question.

The question comparing Thornby Wells and Elder Ness was really the only miss, so I wanted to test whether combining semantic similarity with exact keyword matching would make questions dealing with more than one location more reliable.


### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks preserve useful information | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. Answers contain the information requested | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |


**Did it help?**

The BM25 reranking unfortunately didn't improve my Criterion 1, which remained at 4/5 questions. The Thornby Wells and Elder Ness question was still being marked as a retrieval miss. Interestingly enough, the actual generated answer still included both reqeusted pieces of information: Thornby Wells being a 15-minute walk end to end and the Elder Ness lighthouse being a 25-minute walk over difficult shingle. This suggests that BM25 reranking did not improve the measured retrieval score, even though the retrieved context was still sufficient for the model to answer the question correctly.



## What's Still Broken


As of now, all five of my original criteria still met their targets after my improvement, so I did not have a criterion that completely failed.

I would say the main issue that's still left is Criterion 1. Unforntunately, it stayed at 4/5 before and after adding BM25 reranking 😔. The Thornby Wells and Elder Ness question was still marked as a retrieval miss even though the retrieved sources included both `guide_thornby_wells.md` and `guide_elder_ness.md`, and the generated answer correctly included both the 15-minute walk through Thornby Wells and the 25-minute lighthouse walk over difficult shingle at Elder Ness.

If I continued working on this, I think I would look wayy more closely at how my retrieval scorer handles multi-part expected answers. I would also experiment with letting BM25 search a bigger candidate pool instead of only reranking the chunks already returned by the semantic search.

I stopped here because my original criteria were still being met and Milestone 4 asked me to make and measure one focused improvement rather than continue changing multiple parts of the pipeline.






## What I'd Do Differently

Knowing what I know now, I would definitely make Criterion 1 stricter. Instead of requiring retrieval evidence for 4/5 questions, I would require all questions to succeed since this criterion honestly matters a lot for the system otherwise answers might not be properly backed by the system.

The 4/5 target allowed the criterion to pass even though the same multi-part question consistently remained a retrieval miss. I would also think on rewriting the criterion to check whether the full retrieved set contains all of the info needed to answer every part of a question, rather than only checking for a single expected match.

This would likely make the criterion better at testing questions like the Thornby Wells and Elder Ness example, where the information has to come from more than one document and the system has to account for multiple parts of the question.
<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->


## How I used AI

For Unit 2, I mainly used AI to help me understand and compare different evaluation and retrieval approaches. I specifically used it while experimenting with different fuzzy-matching methods for my scorer after lecture, and learning how BM25 could be combined with my existing semantic retrieval.

I also found myself using AI to help reason through the Criterion 1 retrieval issue and identify possible stages of the pipeline that could be responsible. I still made the final decisions on my scorer threshold, criteria, BM25 implementation, and what improvement to test, then measured those changes using my own evaluation runs.