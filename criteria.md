# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Some of my questions require information from multiple documents, and I noticed that retrieval can prioritize one location over 
another. For example, my question comparing Thornby Wells and Elder Ness initially missed important information because it 
appeared in the sixth retrieved chunk. I want my system to consistently retrieve the information needed to answer most 
questions, even when that information is spread across different documents.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
My chunking strategy preserves the original document titles and source filenames, which allows the system to identify where its 
information came from. Since my goal is to keep answers grounded in the documents, I expect every answer to include a source so 
I can verify the information myself.
---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
When I tested my five answerable questions, their best distances ranged from 0.212 to 0.520, while my five out-of-scope 
questions ranged from 0.8026 to 0.9753. Since there was a clear gap between the two groups, I chose a relevance cutoff of 0.66. 
I want my system to consistently refuse questions outside the corpus, although I recognize that some unrelated questions could 
still retrieve seemingly relevant information and fall below my cutoff.

---

## 4. Chunks preserve useful information
For at least 4 of my 5 sampled chunks, each chunk must contain between 100 and 800 characters and enough context to answer a 
question independently, rather than containing only a heading or an incomplete thought.

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->



**Why this target:**

My initial paragraph-based approach produced 213 chunks, many of which lacked context or contained only headings. After 
experimenting with different approaches, I decided to use Markdown sections with an 800-character limit to keep related 
information together. I want to measure whether this approach produces chunks that contain enough useful information without 
splitting important context across multiple chunks.

---

## 5. Answers contain the information requested
For at least 4 of my 5 test questions, the system's answer must include all the specific facts requested in the question, 
rather than providing only a general or partial answer.


**Why this target:**

Some of my questions require multiple pieces of information, such as comparing the walking times in Thornby Wells and Elder 
Ness or identifying the populations of two different villages. I want my system to retrieve and use all the necessary 
information rather than returning an answer that only addresses part of the question. This would also allow me to evaluate 
whether increasing TOP_K to 8 actually helps the system produce more complete answers.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
